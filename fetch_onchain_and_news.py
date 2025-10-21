from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree

import requests

HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "30"))
DEFAULT_OUTPUT = Path("global_onchain_news_snapshot.json")

# Cache for previous snapshot
_prev_snapshot_cache: Optional[Dict[str, Any]] = None

def _load_previous_snapshot() -> Optional[Dict[str, Any]]:
    global _prev_snapshot_cache
    if _prev_snapshot_cache is not None:
        return _prev_snapshot_cache
    try:
        if DEFAULT_OUTPUT.exists():
            with DEFAULT_OUTPUT.open("r", encoding="utf-8") as f:
                _prev_snapshot_cache = json.load(f)
                return _prev_snapshot_cache
    except Exception:
        return None
    return None

BRIDGES_DATASET_URLS = [
    "https://bridges.llama.fi/bridges",
    "https://api.llama.fi/bridges",
    "https://datasets.llama.fi/bridges_v2/data.json",
]

STABLECOIN_CHAIN_DATASET_URLS = [
    "https://datasets.llama.fi/stablecoin_chains/latest.json",
    "https://defillama-datasets.llama.fi/stablecoin_chains/latest.json",
]


def _resolve_proxy() -> Optional[str]:
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if proxy:
        return proxy.strip() or None
    use_local_proxy = os.environ.get("USE_LOCAL_PROXY", "1").lower()
    if use_local_proxy in {"1", "true", "yes"}:
        return "http://127.0.0.1:7890"
    return None


def _build_session() -> requests.Session:
    session = requests.Session()
    proxy = _resolve_proxy()
    if proxy:
        session.proxies.update({"http": proxy, "https": proxy})
    session.headers.update(
        {
            "User-Agent": os.environ.get(
                "HTTP_USER_AGENT",
                "CodexDataFetcher/1.0 (+https://defillama.com)",
            )
        }
    )
    return session


def _fetch_json(
    session: requests.Session, url: str, params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    try:
        resp = session.get(url, params=params, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return {"error": str(exc), "url": url, "params": params}
    try:
        return resp.json()
    except ValueError:
        preview = resp.text[:400]
        return {"error": "invalid_json", "url": url, "params": params, "preview": preview}


def _fetch_rss_items(session: requests.Session, url: str, limit: int = 5) -> Dict[str, Any]:
    try:
        resp = session.get(url, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return {"error": str(exc), "url": url}
    try:
        root = ElementTree.fromstring(resp.content)
    except ElementTree.ParseError as exc:
        preview = resp.text[:400]
        return {"error": f"rss_parse_error: {exc}", "url": url, "preview": preview}

    items: List[Dict[str, Any]] = []
    for item in root.findall(".//item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or item.findtext("{http://purl.org/dc/elements/1.1/}date") or "").strip()
        summary = (item.findtext("description") or "").strip()
        items.append(
            {
                "title": title,
                "link": link,
                "published": pub_date,
                "summary": summary,
            }
        )
    return {"items": items, "source": url}


def _fetch_cryptocompare_news(
    session: requests.Session,
    categories: str = "BTC,ETH",
    lang: str = "EN",
    limit: int = 20,
) -> Dict[str, Any]:
    params = {
        "categories": categories,
        "lang": lang.upper(),
        "sortOrder": "latest",
        "lTs": "",
    }
    data = _fetch_json(session, "https://min-api.cryptocompare.com/data/v2/news/", params)
    if isinstance(data, dict) and data.get("error"):
        return {"error": data.get("error"), "url": "cryptocompare", "params": params}
    items: List[Dict[str, Any]] = []
    entries = []
    if isinstance(data, dict):
        if isinstance(data.get("Data"), list):
            entries = data.get("Data")
        elif isinstance(data.get("data"), list):
            entries = data.get("data")
    for entry in entries[:limit]:
        if not isinstance(entry, dict):
            continue
        ts = entry.get("published_on")
        if ts:
            try:
                published = datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat()
            except (ValueError, TypeError):
                published = ts
        else:
            published = None
        items.append(
            {
                "title": entry.get("title"),
                "link": entry.get("url"),
                "published": published,
                "source": entry.get("source"),
                "tags": entry.get("categories"),
                "summary": entry.get("body"),
            }
        )
    if not items:
        return {
            "items": items,
            "source": "CryptoCompare",
            "params": params,
            "note": "No news items returned; may be rate limited or category empty.",
            "raw": data,
        }
    return {"items": items, "source": "CryptoCompare", "params": params}


def _numeric_change(current: Optional[float], previous: Optional[float]) -> Dict[str, Optional[float]]:
    if current is None or previous is None:
        return {"current": current, "previous": previous, "abs_change": None, "pct_change": None}
    abs_change = current - previous
    pct_change = (abs_change / previous * 100) if previous else None
    return {
        "current": round(current, 2),
        "previous": round(previous, 2),
        "abs_change": round(abs_change, 2),
        "pct_change": round(pct_change, 2) if pct_change is not None else None,
    }


def _extract_series_value(entry: Dict[str, Any]) -> Optional[float]:
    for key in ("totalCirculating", "totalCirculatingUSD", "totalLiquidityUSD", "totalLiquidity", "value"):
        if key in entry:
            try:
                return float(entry[key])
            except (TypeError, ValueError):
                continue
    return None


def _safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _match_stablecoin_chain_entry(data: Dict[str, Any], chain_cap: str) -> Optional[Dict[str, Any]]:
    chain_lower = chain_cap.lower()
    candidates: List[Dict[str, Any]] = []
    for key in ("chains", "data", "entries", "list"):
        val = data.get(key)
        if isinstance(val, dict):
            for name, entry in val.items():
                if isinstance(entry, dict):
                    entry_copy = dict(entry)
                    entry_copy.setdefault("name", name)
                    candidates.append(entry_copy)
        elif isinstance(val, list):
            for entry in val:
                if isinstance(entry, dict):
                    candidates.append(entry)
    if not candidates and all(isinstance(k, str) for k in data.keys()):
        for name, entry in data.items():
            if isinstance(entry, dict):
                entry_copy = dict(entry)
                entry_copy.setdefault("name", name)
                candidates.append(entry_copy)
    for entry in candidates:
        name = str(entry.get("name") or entry.get("chain") or "").lower()
        if not name:
            continue
        if name == chain_lower:
            return entry
        if name.replace(" ", "") == chain_lower.replace(" ", ""):
            return entry
    return None


def _normalize_bridge_protocol(entry: Dict[str, Any]) -> Dict[str, Any]:
    net_field = entry.get("netflow") or entry.get("netFlow") or {}
    if not isinstance(net_field, dict):
        net_field = {}
    return {
        "name": entry.get("displayName") or entry.get("name"),
        "category": entry.get("category"),
        "tvl": entry.get("totalLiquidity") or entry.get("tvl"),
        "net_flow_1d": net_field.get("1d"),
        "net_flow_7d": net_field.get("7d"),
        "net_flow_1m": net_field.get("1m"),
        "raw": entry,
    }


def _fallback_bridge_protocols(session: requests.Session, chain_param: str) -> Dict[str, Any]:
    errors: List[Dict[str, Any]] = []
    collected: List[Dict[str, Any]] = []

    for url in BRIDGES_DATASET_URLS:
        data = _fetch_json(session, url)
        if isinstance(data, dict) and data.get("error"):
            errors.append({"url": url, "detail": data["error"]})
            continue
        candidates: List[Dict[str, Any]] = []
        if isinstance(data, list):
            candidates = [d for d in data if isinstance(d, dict)]
        elif isinstance(data, dict):
            for key in ("bridges", "data", "protocols"):
                val = data.get(key)
                if isinstance(val, list):
                    candidates = [d for d in val if isinstance(d, dict)]
                    break
        if not candidates:
            errors.append({"url": url, "detail": "no_candidates"})
            continue
        filtered = []
        for c in candidates:
            chains_field = c.get("chains")
            matches_chain = False
            if isinstance(chains_field, list):
                matches_chain = chain_param in chains_field or chain_param.lower() in [str(x).lower() for x in chains_field]
            elif isinstance(chains_field, dict):
                key_list = list(chains_field.keys())
                matches_chain = chain_param in key_list or chain_param.lower() in [str(k).lower() for k in key_list]
            dest_chain = c.get("destinationChain") or c.get("chain")
            if not matches_chain and isinstance(dest_chain, str):
                matches_chain = dest_chain.lower() == chain_param.lower()
            if not matches_chain and isinstance(c.get("name"), str):
                matches_chain = chain_param.lower() in c["name"].lower()
            if matches_chain:
                metrics_source = c.get("stats") or c
                filtered.append(
                    {
                        "name": c.get("displayName") or c.get("name"),
                        "category": c.get("category"),
                        "tvl": c.get("tvl") or c.get("totalLiquidity"),
                        "chains": c.get("chains"),
                        "destination": dest_chain,
                        "volume_1d": _safe_float(
                            metrics_source.get("volumePrevDay")
                            or metrics_source.get("volume_1d")
                            or metrics_source.get("last24hVolume")
                            or metrics_source.get("dailyVolume")
                        ),
                        "volume_7d": _safe_float(
                            metrics_source.get("volume_7d") or metrics_source.get("weeklyVolume")
                        ),
                        "volume_30d": _safe_float(
                            metrics_source.get("volume_30d") or metrics_source.get("monthlyVolume")
                        ),
                        "net_flow": metrics_source.get("netFlow") or metrics_source.get("netflow"),
                        "raw": c,
                    }
                )
        if filtered:
            collected.extend(filtered)
        else:
            errors.append({"url": url, "detail": "no_matching_chain"})
    collected.sort(key=lambda x: (x.get("volume_1d") or 0), reverse=True)
    top = collected[:10]
    summary: Dict[str, Any] = {}
    if collected:
        for key in ("volume_1d", "volume_7d", "volume_30d"):
            vals = [item.get(key) for item in collected if isinstance(item.get(key), (int, float))]
            if vals:
                summary[key] = sum(vals)
        nets: Dict[str, float] = {}
        for item in collected:
            net = item.get("net_flow")
            if isinstance(net, dict):
                for period, value in net.items():
                    fv = _safe_float(value)
                    if fv is None:
                        continue
                    nets[period] = nets.get(period, 0.0) + fv
        if nets:
            summary["net_flow"] = nets
    return {"protocols": top, "errors": errors, "summary": summary if summary else None}


def _extract_series_from_payload(payload: Any) -> Optional[List[Dict[str, Any]]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return None
    for key in ("data", "chainBalances", "chart", "series"):
        val = payload.get(key)
        if isinstance(val, list):
            return [item for item in val if isinstance(item, dict)]
    return None


def _summarize_stablecoin_series(series: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []
    for entry in series:
        value = _extract_series_value(entry)
        if value is None:
            continue
        ts = (
            entry.get("date")
            or entry.get("timestamp")
            or entry.get("time")
            or entry.get("ts")
            or entry.get("dateUTC")
        )
        cleaned.append({"timestamp": ts, "value": float(value)})
    if not cleaned:
        return None
    latest = cleaned[-1]
    previous = cleaned[-2] if len(cleaned) > 1 else None
    summary: Dict[str, Any] = {
        "latest": {
            "timestamp": latest["timestamp"],
            "value": round(latest["value"], 2),
        },
        "previous": None,
        "change": None,
    }
    if previous:
        summary["previous"] = {
            "timestamp": previous["timestamp"],
            "value": round(previous["value"], 2),
        }
        summary["change"] = _numeric_change(latest["value"], previous["value"])
    return summary


def _fill_stablecoin_change_from_previous(chain_key: str, summary: Optional[Dict[str, Any]], prev_snapshot: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not isinstance(summary, dict):
        return summary
    if not prev_snapshot or not isinstance(prev_snapshot, dict):
        return summary
    try:
        prev_defi = prev_snapshot.get("defillama") or {}
        prev_chain = prev_defi.get(chain_key) or {}
        prev_stable = prev_chain.get("stablecoin") or {}
        prev_summary = prev_stable.get("summary") or {}
        prev_latest = prev_summary.get("latest") or {}
        prev_val = prev_latest.get("value")
        cur_latest = summary.get("latest") or {}
        cur_val = cur_latest.get("value")
        if isinstance(cur_val, (int, float)) and isinstance(prev_val, (int, float)):
            # attach previous and change if missing
            if not summary.get("previous"):
                summary["previous"] = {"timestamp": prev_latest.get("timestamp"), "value": prev_val}
            if not summary.get("change"):
                summary["change"] = _numeric_change(cur_val, prev_val)
    except Exception:
        return summary
    return summary


def _fetch_stablecoin_history(session: requests.Session, chain: str, prev_snapshot: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    chain_slug = chain.lower()
    chain_cap = chain.capitalize()
    endpoints = [
        (f"https://stablecoins.llama.fi/stablecoincharts/{chain_cap}", None),
        (f"https://stablecoins.llama.fi/stablecoincharts/{chain_slug}", None),
        (f"https://stablecoins.llama.fi/api/historicalChain/{chain_slug}", None),
        (f"https://stablecoins.llama.fi/api/chain/{chain_slug}", None),
        ("https://stablecoins.llama.fi/api/stablecoins", {"includeChains": "true"}),
    ]
    attempts: List[Dict[str, Any]] = []
    for url, params in endpoints:
        data = _fetch_json(session, url, params)
        if isinstance(data, dict) and data.get("error"):
            attempts.append({"url": url, "params": params, "detail": data.get("error")})
            continue
        if url.endswith("/stablecoins") and params and params.get("includeChains") == "true":
            stablecoins = data.get("stablecoins") or data.get("data")
            if isinstance(stablecoins, list):
                total = 0.0
                for coin in stablecoins:
                    chains = coin.get("chains")
                    if isinstance(chains, dict):
                        try:
                            total += float(
                                chains.get(chain.capitalize())
                                or chains.get(chain)
                                or chains.get(chain_slug)
                                or 0.0
                            )
                        except (TypeError, ValueError):
                            continue
                summary = {
                    "latest": {"value": round(total, 2), "timestamp": None},
                    "previous": None,
                    "change": None,
                }
                # fill change from previous snapshot if available
                summary = _fill_stablecoin_change_from_previous(chain_slug, summary, prev_snapshot)
                return {
                    "source": url,
                    "params": params,
                    "raw": data,
                    "summary": summary,
                }
            attempts.append({"url": url, "params": params, "detail": "no_stablecoins_list"})
            continue
        series = _extract_series_from_payload(data)
        if not series and isinstance(data, list):
            series = [d for d in data if isinstance(d, dict)]
        if series:
            summary = _summarize_stablecoin_series(series)
            if summary:
                summary = _fill_stablecoin_change_from_previous(chain_slug, summary, prev_snapshot)
                return {
                    "source": url,
                    "params": params,
                    "raw": data,
                    "summary": summary,
                }
            else:
                attempts.append({"url": url, "params": params, "detail": "no_summary"})
                continue
        attempts.append({"url": url, "params": params, "detail": "no_series"})
    chains_snapshot = _fetch_json(session, "https://stablecoins.llama.fi/api/stablecoinchains")
    if isinstance(chains_snapshot.get("data"), list):
        match = next(
            (
                item
                for item in chains_snapshot["data"]
                if isinstance(item, dict)
                and (
                    item.get("name") == chain_cap
                    or item.get("chain") == chain_cap
                    or item.get("name") == chain_slug.capitalize()
                )
            ),
            None,
        )
        if match:
            value = match.get("value") or match.get("totalCirculating") or match.get("total")
            try:
                latest_value = round(float(value), 2)
            except (TypeError, ValueError):
                latest_value = value
            summary = {
                "latest": {"value": latest_value, "timestamp": datetime.now(timezone.utc).isoformat()},
                "previous": None,
                "change": None,
                "note": "Fell back to stablecoincharts; change metrics unavailable.",
            }
            summary = _fill_stablecoin_change_from_previous(chain_slug, summary, prev_snapshot)
            return {
                "source": "https://stablecoins.llama.fi/api/stablecoinchains",
                "raw": chains_snapshot,
                "summary": summary,
                "attempts": attempts,
            }
    for url in STABLECOIN_CHAIN_DATASET_URLS:
        dataset = _fetch_json(session, url)
        if not isinstance(dataset, dict) or dataset.get("error"):
            attempts.append({"url": url, "detail": dataset.get("error") if isinstance(dataset, dict) else "invalid"})
            continue
        match = _match_stablecoin_chain_entry(dataset, chain_cap)
        if match:
            latest_value = _safe_float(match.get("latestValue") or match.get("value") or match.get("total"))
            change_24h = _safe_float(match.get("change_24h") or match.get("change24h") or match.get("change1d"))
            timestamp = match.get("timestamp") or dataset.get("timestamp")
            summary = {
                "latest": {
                    "value": round(latest_value, 2) if isinstance(latest_value, float) else latest_value,
                    "timestamp": timestamp,
                },
                "previous": None,
                "change": change_24h,
            }
            if change_24h is None:
                summary["note"] = "Dataset snapshot provided without change metrics."
            summary = _fill_stablecoin_change_from_previous(chain_slug, summary, prev_snapshot)
            return {
                "source": url,
                "raw": dataset,
                "summary": summary,
                "attempts": attempts,
            }
        attempts.append({"url": url, "detail": "chain_not_found"})

    # Additional fallback: use stablecoins aggregated endpoint to compute chain totalCirculatingUSD
    sc_fallback = _fetch_json(session, "https://stablecoins.llama.fi/stablecoins")
    if isinstance(sc_fallback.get("chains"), list):
        # try exact name match (case-insensitive)
        entry = None
        for e in sc_fallback["chains"]:
            name = (e.get("name") or "").strip()
            if name.lower() == chain_slug:
                entry = e
                break
        if entry:
            tc = entry.get("totalCirculatingUSD")
            total = None
            if isinstance(tc, dict):
                nums = [v for v in tc.values() if isinstance(v, (int, float))]
                if nums:
                    total = sum(nums)
            if total is not None:
                summary = {
                    "latest": {"value": round(float(total), 2), "timestamp": datetime.now(timezone.utc).isoformat()},
                    "previous": None,
                    "change": None,
                    "note": "Computed from stablecoins.llama.fi/stablecoins (chain-level totalCirculatingUSD).",
                }
                summary = _fill_stablecoin_change_from_previous(chain_slug, summary, prev_snapshot)
                attempts.append({"url": "https://stablecoins.llama.fi/stablecoins", "detail": "used_chain_total"})
                return {
                    "source": "https://stablecoins.llama.fi/stablecoins",
                    "raw": sc_fallback,
                    "summary": summary,
                    "attempts": attempts,
                }
        else:
            attempts.append({"url": "https://stablecoins.llama.fi/stablecoins", "detail": "chain_not_found"})

    return {"error": "stablecoin_series_not_found", "attempts": attempts, "chains_snapshot": chains_snapshot}


def fetch_defillama_flows(session: requests.Session, chain: str = "Ethereum") -> Dict[str, Any]:
    chain_param = chain.capitalize()

    # Load previous snapshot once and pass into stablecoin to compute change if needed
    prev_snapshot = _load_previous_snapshot()

    overview = _fetch_json(
        session,
        "https://api.llama.fi/overview/bridges",
        params={
            "chains": chain_param,
            "excludeTotalDataChart": "true",
            "excludeTotalDataChartBreakdown": "true",
        },
    )

    highlights: List[Dict[str, Any]] = []
    chain_protocols = None
    if isinstance(overview.get("chainProtocols"), dict):
        chain_protocols = overview["chainProtocols"].get(chain_param)
    # Fallback: refetch without chain filter if empty or unavailable
    if not isinstance(chain_protocols, list) or len(chain_protocols) == 0:
        overview_no_filter = _fetch_json(
            session,
            "https://api.llama.fi/overview/bridges",
            params={
                "excludeTotalDataChart": "true",
                "excludeTotalDataChartBreakdown": "true",
            },
        )
        if isinstance(overview_no_filter.get("chainProtocols"), dict):
            chain_protocols = overview_no_filter["chainProtocols"].get(chain_param)
    if isinstance(chain_protocols, list):
        for entry in chain_protocols[:10]:
            highlights.append(_normalize_bridge_protocol(entry))
    fallback_protocols = None
    if not highlights:
        fallback_protocols = _fallback_bridge_protocols(session, chain_param)

    stablecoin_info = _fetch_stablecoin_history(session, chain_param, prev_snapshot=prev_snapshot)

    notes: List[str] = []
    if isinstance(overview, dict) and overview.get("error"):
        notes.append("overview endpoint returned error; fallback data may be limited.")
    if not highlights and fallback_protocols and not fallback_protocols.get("protocols"):
        notes.append("No bridge protocols matched the requested chain in fallback sources.")
    if isinstance(stablecoin_info, dict) and stablecoin_info.get("error"):
        notes.append("Stablecoin history unavailable; see attempts for details.")

    # Ensure bridge_summary exists by synthesizing from fallback protocols when summary empty
    bridge_summary = None
    if fallback_protocols:
        bridge_summary = fallback_protocols.get("summary")
        if not bridge_summary and isinstance(fallback_protocols.get("protocols"), list):
            # compute minimal summary from top protocols
            protos = fallback_protocols["protocols"]
            totals: Dict[str, float] = {}
            for key in ("volume_1d", "volume_7d", "volume_30d"):
                vals = [p.get(key) for p in protos if isinstance(p.get(key), (int, float))]
                if vals:
                    totals[key] = sum(vals)
            if totals:
                bridge_summary = totals

    return {
        "chain": chain_param,
        "bridge_overview_raw": overview,
        "bridge_top_protocols": highlights,
        "bridge_fallback": fallback_protocols,
        "bridge_summary": bridge_summary,
        "stablecoin": stablecoin_info,
        "notes": notes,
    }


def fetch_blockchair_metrics(session: requests.Session, chain: str) -> Dict[str, Any]:
    chain_slug = chain.lower()
    stats = _fetch_json(session, f"https://api.blockchair.com/{chain_slug}/stats")

    gas_snapshot: Optional[Dict[str, Optional[float]]] = None
    suggested_fee = None
    mempool_summary: Optional[Dict[str, Any]] = None
    if isinstance(stats.get("data"), dict):
        data = stats["data"]
        gas_fields = [
            "suggested_transaction_fee_per_gas_wei",
            "gas_price",
            "avg_gas_price_10m",
            "avg_gas_price_24h",
            "mempool_median_gas_price_wei",
            "mempool_median_gas_price",
        ]
        gas_price_raw = None
        for field in gas_fields:
            if data.get(field) is not None:
                gas_price_raw = data[field]
                break
        base_fields = [
            "suggested_base_fee_per_gas_wei",
            "base_fee_per_gas_wei",
            "base_fee_24h",
            "avg_base_fee_24h",
        ]
        base_fee_raw = None
        for field in base_fields:
            if data.get(field) is not None:
                base_fee_raw = data[field]
                break
        if gas_price_raw is not None or base_fee_raw is not None:
            try:
                gas_price_gwei = float(gas_price_raw) / 1e9 if gas_price_raw is not None else None
            except (TypeError, ValueError):
                gas_price_gwei = None
            try:
                base_fee_gwei = float(base_fee_raw) / 1e9 if base_fee_raw is not None else None
            except (TypeError, ValueError):
                base_fee_gwei = None
            gas_snapshot = {
                "suggested_gas_price_gwei": round(gas_price_gwei, 4) if gas_price_gwei is not None else None,
                "base_fee_gwei": round(base_fee_gwei, 4) if base_fee_gwei is not None else None,
            }
        suggested_fee_fields = [
            "suggested_transaction_fee_per_byte_sat",
            "suggested_transaction_fee_per_byte_wei",
            "mempool_median_transaction_fee_sat",
            "median_transaction_fee_24h",
        ]
        for field in suggested_fee_fields:
            if data.get(field) is not None:
                suggested_fee = data[field]
                break
        mempool_fields = {
            "transactions": [
                "mempool_txs",
                "mempool_transactions",
                "mempool_total_transactions",
            ],
            "size_kb": [
                "mempool_total_size_kb",
                "mempool_size_kb",
            ],
            "size_bytes": [
                "mempool_total_size",
                "mempool_size",
            ],
            "unconfirmed_value_usd": [
                "mempool_outputs_total_value_usd",
                "mempool_total_value_usd",
            ],
        }
        mempool_summary = {}
        for key, candidates in mempool_fields.items():
            for field in candidates:
                if data.get(field) is not None:
                    mempool_summary[key] = data[field]
                    break
        if not mempool_summary:
            mempool_summary = None

    return {
        "chain": chain_slug,
        "stats": stats,
        "gas_snapshot": gas_snapshot,
        "suggested_fee_rate": suggested_fee,
        "mempool_summary": mempool_summary,
        "notes": [
            f"Blockchair /{chain_slug}/mempool endpoint currently 404; stats-based summary provided instead."
        ],
    }


def fetch_bitcoin_mempool(session: requests.Session) -> Dict[str, Any]:
    """
    汇总 mempool.space 的 BTC 排队情况与建议手续费。
    """
    overview = _fetch_json(session, "https://mempool.space/api/mempool")
    recommended = _fetch_json(session, "https://mempool.space/api/v1/fees/recommended")
    queue_metrics = None
    if isinstance(overview, dict) and not overview.get("error"):
        queue_metrics = {
            "count": overview.get("count"),
            "vsize": overview.get("vsize"),
            "total_fee": overview.get("total_fee"),
        }
    combined = {
        "overview": overview,
        "recommended_fees": recommended,
        "queue_metrics": queue_metrics,
    }
    return combined


def fetch_eth_gas_etherscan(session: requests.Session, api_key: Optional[str]) -> Dict[str, Any]:
    """
    使用 Etherscan 免费 API 获取 ETH Gas 速率与历史。
    如果缺少 API Key，则只返回错误提示。
    """
    base_params = {"module": "gastracker"}
    if not api_key:
        return {"error": "missing_api_key", "detail": "ETHERSCAN_API_KEY 未设置"}

    gas_oracle = _fetch_json(
        session,
        "https://api.etherscan.io/api",
        params={
            **base_params,
            "action": "gasoracle",
            "apikey": api_key,
        },
    )

    fee_history = _fetch_json(
        session,
        "https://api.etherscan.io/api",
        params={
            **base_params,
            "action": "gasfeeHistory",
            "blockCount": "12",
            "rewardPercentiles": "10,50,90",
            "apikey": api_key,
        },
    )

    gas_summary: Optional[Dict[str, Any]] = None
    if isinstance(gas_oracle.get("result"), dict):
        result = gas_oracle["result"]
        try:
            gas_summary = {
                "safe_gwei": float(result.get("SafeGasPrice")),
                "propose_gwei": float(result.get("ProposeGasPrice")),
                "fast_gwei": float(result.get("FastGasPrice")),
                "suggest_base_fee": float(result.get("suggestBaseFee")),
                "gas_used_ratio": float(result.get("gasUsedRatio")),
            }
        except (TypeError, ValueError):
            gas_summary = {
                "safe_gwei": result.get("SafeGasPrice"),
                "propose_gwei": result.get("ProposeGasPrice"),
                "fast_gwei": result.get("FastGasPrice"),
                "suggest_base_fee": result.get("suggestBaseFee"),
                "gas_used_ratio": result.get("gasUsedRatio"),
            }

    fee_points: List[Dict[str, Any]] = []
    if isinstance(fee_history.get("result"), dict):
        fh = fee_history["result"]
        base_fees = fh.get("baseFeePerGas", [])
        gas_ratios = fh.get("gasUsedRatio", [])
        rewards = fh.get("reward", [])
        newest_block = fh.get("latestBlock")
        for idx, base_fee in enumerate(base_fees):
            try:
                base_fee_gwei = int(base_fee, 16) / 1e9
            except (TypeError, ValueError):
                base_fee_gwei = base_fee
            reward_set = rewards[idx] if idx < len(rewards) else []
            fee_points.append(
                {
                    "base_fee_gwei": round(base_fee_gwei, 4) if isinstance(base_fee_gwei, float) else base_fee_gwei,
                    "gas_used_ratio": gas_ratios[idx] if idx < len(gas_ratios) else None,
                    "priority_fee_percentiles": reward_set,
                }
            )
        history_meta = {
            "block_count": fh.get("blockCount"),
            "last_block": newest_block,
            "points": fee_points,
        }
    else:
        history_meta = {"error": fee_history.get("error"), "raw": fee_history}

    return {
        "gas_oracle_raw": gas_oracle,
        "gas_oracle_summary": gas_summary,
        "fee_history_raw": fee_history,
        "fee_history_summary": history_meta,
    }


def gather_news(session: requests.Session) -> Dict[str, Any]:
    feeds = {
        "bitcoin": [
            "https://www.coindesk.com/tag/bitcoin/rss/",
            "https://cointelegraph.com/rss/tag/bitcoin",
        ],
        "ethereum": [
            "https://www.coindesk.com/tag/ethereum/rss/",
            "https://cointelegraph.com/rss/tag/ethereum",
        ],
        "general": [
            "https://decrypt.co/feed",
            "https://news.bitcoin.com/feed/",
        ],
    }
    news: Dict[str, Any] = {}
    crypto_compare_cache = _fetch_cryptocompare_news(session, categories="BTC,ETH", lang="EN", limit=30)
    for topic, urls in feeds.items():
        topic_items: List[Dict[str, Any]] = []
        errors: List[Dict[str, Any]] = []
        for url in urls:
            result = _fetch_rss_items(session, url, limit=5)
            if "items" in result:
                topic_items.extend(result["items"])
            else:
                errors.append(result)
        topic_items.sort(key=lambda x: x.get("published", ""), reverse=True)
        if topic == "general" and "items" in crypto_compare_cache:
            topic_items.extend(crypto_compare_cache["items"])
        topic_items.sort(key=lambda x: x.get("published", ""), reverse=True)
        note = None
        if not topic_items and errors:
            note = "所有新闻源均拉取失败，可能需要代理或额外认证。"
        extra_errors: List[Dict[str, Any]] = []
        if topic == "general" and crypto_compare_cache.get("error"):
            extra_errors.append(crypto_compare_cache)
        news[topic] = {
            "items": topic_items[:10],
            "errors": errors + extra_errors,
            "note": note,
        }
    if "items" in crypto_compare_cache and crypto_compare_cache["items"]:
        news["cryptocompare"] = crypto_compare_cache
    else:
        news["cryptocompare"] = crypto_compare_cache
    return news


def fetch_fear_greed_index(session: requests.Session, limit: int = 15) -> Dict[str, Any]:
    resp = _fetch_json(session, "https://api.alternative.me/fng/", params={"limit": str(limit)})
    series: List[Dict[str, Any]] = []
    data = resp.get("data") if isinstance(resp, dict) else None
    if isinstance(data, list):
        for item in data:
            val = item.get("value")
            try:
                val_f = float(val) if val is not None else None
            except (TypeError, ValueError):
                val_f = None
            series.append({
                "timestamp": item.get("timestamp"),
                "value": val_f,
                "classification": item.get("value_classification"),
            })
    latest = series[0] if series else None
    return {"source": "https://api.alternative.me/fng/", "raw": resp, "latest": latest, "series": series}


def _bridge_topN(flows: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
    protos: List[Dict[str, Any]] = []
    if isinstance(flows.get("bridge_top_protocols"), list) and flows["bridge_top_protocols"]:
        protos = flows["bridge_top_protocols"]
    elif isinstance(flows.get("bridge_fallback"), dict) and isinstance(flows["bridge_fallback"].get("protocols"), list):
        protos = flows["bridge_fallback"]["protocols"]
    def vol1d(p: Dict[str, Any]) -> float:
        v = p.get("volume_1d")
        return float(v) if isinstance(v, (int, float)) else 0.0
    protos_sorted = sorted(protos, key=vol1d, reverse=True)
    return [{
        "name": p.get("name"),
        "volume_1d": p.get("volume_1d"),
        "volume_7d": p.get("volume_7d"),
        "volume_30d": p.get("volume_30d"),
    } for p in protos_sorted[:top_n]]


def build_daily_report(defi_eth: Dict[str, Any], defi_btc: Dict[str, Any], fear: Dict[str, Any], top_n: int = 5) -> Dict[str, Any]:
    def fmt_sc(sc: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        summ = sc.get("summary") if isinstance(sc, dict) else None
        latest = summ.get("latest") if isinstance(summ, dict) else None
        change = summ.get("change") if isinstance(summ, dict) else None
        previous = summ.get("previous") if isinstance(summ, dict) else None
        note = summ.get("note") if isinstance(summ, dict) else None
        return {"latest": latest, "previous": previous, "change": change, "note": note}
    eth_sc = fmt_sc(defi_eth.get("stablecoin"))
    btc_sc = fmt_sc(defi_btc.get("stablecoin"))
    eth_top = _bridge_topN(defi_eth, top_n)
    btc_top = _bridge_topN(defi_btc, top_n)
    eth_sum = defi_eth.get("bridge_summary")
    btc_sum = defi_btc.get("bridge_summary")
    fear_latest = fear.get("latest")
    eth_latest_val = eth_sc.get('latest')
    eth_latest_val = eth_latest_val.get('value') if isinstance(eth_latest_val, dict) else None
    btc_latest_val = btc_sc.get('latest')
    btc_latest_val = btc_latest_val.get('value') if isinstance(btc_latest_val, dict) else None
    sc_para = (
        f"稳定币 — ETH 最新: {eth_latest_val}, 环比: {eth_sc.get('change')}; "
        f"BTC 最新: {btc_latest_val}, 环比: {btc_sc.get('change')}。"
    )
    eth_top_str = ", ".join([f"{p.get('name')}: {p.get('volume_1d')}" for p in eth_top])
    btc_top_str = ", ".join([f"{p.get('name')}: {p.get('volume_1d')}" for p in btc_top])
    bridges_para = (
        f"桥接 — ETH 量 (1d/7d/30d): {tuple((eth_sum or {}).get(k) for k in ('volume_1d','volume_7d','volume_30d'))}; "
        f"Top {top_n}: {eth_top_str}。 "
        f"BTC 量 (1d/7d/30d): {tuple((btc_sum or {}).get(k) for k in ('volume_1d','volume_7d','volume_30d'))}; "
        f"Top {top_n}: {btc_top_str}."
    )
    fear_para = (
        f"BTC 恐慌指数 — 最新值: {fear_latest.get('value') if isinstance(fear_latest, dict) else None}, "
        f"分类: {fear_latest.get('classification') if isinstance(fear_latest, dict) else None} (近 {len(fear.get('series') or [])} 天)。"
    )
    return {
        "stablecoins": {"ethereum": eth_sc, "bitcoin": btc_sc, "paragraph": sc_para},
        "bridges": {
            "ethereum": {"summary": eth_sum, "top": eth_top},
            "bitcoin": {"summary": btc_sum, "top": btc_top},
            "paragraph": bridges_para,
        },
        "fear_greed": {"series": fear.get("series"), "latest": fear_latest, "paragraph": fear_para},
    }


def aggregate_snapshot(session: requests.Session) -> Dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat()
    ethereum_flows = fetch_defillama_flows(session, "Ethereum")
    bitcoin_flows = fetch_defillama_flows(session, "Bitcoin")
    ethereum_metrics = fetch_blockchair_metrics(session, "ethereum")
    bitcoin_metrics = fetch_blockchair_metrics(session, "bitcoin")
    btc_mempool = fetch_bitcoin_mempool(session)
    eth_gas = fetch_eth_gas_etherscan(session, os.environ.get("ETHERSCAN_API_KEY"))
    news = gather_news(session)
    fear_greed = fetch_fear_greed_index(session, limit=15)
    bridge_top_n = int(os.getenv("BRIDGE_TOP_N", "5"))
    daily_report = build_daily_report(ethereum_flows, bitcoin_flows, fear_greed, top_n=bridge_top_n)

    return {
        "generated_at": timestamp,
        "defillama": {
            "ethereum": ethereum_flows,
            "bitcoin": bitcoin_flows,
        },
        "blockchair": {
            "ethereum": ethereum_metrics,
            "bitcoin": bitcoin_metrics,
        },
        "btc_mempool": btc_mempool,
        "eth_gas": eth_gas,
        "news": news,
        "fear_greed": fear_greed,
        "daily_report": daily_report,
    }


def save_snapshot(data: Dict[str, Any], output_path: Path = DEFAULT_OUTPUT) -> Path:
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def main() -> None:
    session = _build_session()
    snapshot = aggregate_snapshot(session)
    path = save_snapshot(snapshot, DEFAULT_OUTPUT)
    print(f"快照已生成：{path}（UTC {snapshot['generated_at']}）")


if __name__ == "__main__":
    main()


def fetch_fear_greed_index(session: requests.Session, limit: int = 15) -> Dict[str, Any]:
    resp = _fetch_json(session, "https://api.alternative.me/fng/", params={"limit": str(limit)})
    series: List[Dict[str, Any]] = []
    data = resp.get("data") if isinstance(resp, dict) else None
    if isinstance(data, list):
        for item in data:
            val = item.get("value")
            try:
                val_f = float(val) if val is not None else None
            except (TypeError, ValueError):
                val_f = None
            series.append({
                "timestamp": item.get("timestamp"),
                "value": val_f,
                "classification": item.get("value_classification"),
            })
    latest = series[0] if series else None
    return {"source": "https://api.alternative.me/fng/", "raw": resp, "latest": latest, "series": series}


def _bridge_topN(flows: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
    protos: List[Dict[str, Any]] = []
    if isinstance(flows.get("bridge_top_protocols"), list) and flows["bridge_top_protocols"]:
        protos = flows["bridge_top_protocols"]
    elif isinstance(flows.get("bridge_fallback"), dict) and isinstance(flows["bridge_fallback"].get("protocols"), list):
        protos = flows["bridge_fallback"]["protocols"]
    def vol1d(p: Dict[str, Any]) -> float:
        v = p.get("volume_1d")
        return float(v) if isinstance(v, (int, float)) else 0.0
    protos_sorted = sorted(protos, key=vol1d, reverse=True)
    return [{
        "name": p.get("name"),
        "volume_1d": p.get("volume_1d"),
        "volume_7d": p.get("volume_7d"),
        "volume_30d": p.get("volume_30d"),
    } for p in protos_sorted[:top_n]]


def build_daily_report(defi_eth: Dict[str, Any], defi_btc: Dict[str, Any], fear: Dict[str, Any], top_n: int = 5) -> Dict[str, Any]:
    def fmt_sc(sc: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        summ = sc.get("summary") if isinstance(sc, dict) else None
        latest = summ.get("latest") if isinstance(summ, dict) else None
        change = summ.get("change") if isinstance(summ, dict) else None
        previous = summ.get("previous") if isinstance(summ, dict) else None
        note = summ.get("note") if isinstance(summ, dict) else None
        return {"latest": latest, "previous": previous, "change": change, "note": note}
    eth_sc = fmt_sc(defi_eth.get("stablecoin"))
    btc_sc = fmt_sc(defi_btc.get("stablecoin"))
    eth_top = _bridge_topN(defi_eth, top_n)
    btc_top = _bridge_topN(defi_btc, top_n)
    eth_sum = defi_eth.get("bridge_summary")
    btc_sum = defi_btc.get("bridge_summary")
    fear_latest = fear.get("latest")
    sc_para = (
        f"稳定币 — ETH 最新: {eth_sc.get('latest', {}).get('value')}, 环比: {eth_sc.get('change')}; "
        f"BTC 最新: {btc_sc.get('latest', {}).get('value')}, 环比: {btc_sc.get('change')}。"
    )
    eth_top_str = ", ".join([f"{p.get('name')}: {p.get('volume_1d')}" for p in eth_top])
    btc_top_str = ", ".join([f"{p.get('name')}: {p.get('volume_1d')}" for p in btc_top])
    bridges_para = (
        f"桥接 — ETH 量 (1d/7d/30d): {tuple((eth_sum or {}).get(k) for k in ('volume_1d','volume_7d','volume_30d'))}; "
        f"Top {top_n}: {eth_top_str}。 "
        f"BTC 量 (1d/7d/30d): {tuple((btc_sum or {}).get(k) for k in ('volume_1d','volume_7d','volume_30d'))}; "
        f"Top {top_n}: {btc_top_str}."
    )
    fear_para = (
        f"BTC 恐慌指数 — 最新值: {fear_latest.get('value') if isinstance(fear_latest, dict) else None}, "
        f"分类: {fear_latest.get('classification') if isinstance(fear_latest, dict) else None} (近 {len(fear.get('series') or [])} 天)。"
    )
    return {
        "stablecoins": {"ethereum": eth_sc, "bitcoin": btc_sc, "paragraph": sc_para},
        "bridges": {
            "ethereum": {"summary": eth_sum, "top": eth_top},
            "bitcoin": {"summary": btc_sum, "top": btc_top},
            "paragraph": bridges_para,
        },
        "fear_greed": {"series": fear.get("series"), "latest": fear_latest, "paragraph": fear_para},
    }
