#!/usr/bin/env python3
"""
AI Spend Tracker — Usage Fetcher
Pulls real usage data from APIs and merges with manual subscription costs.
Outputs public/spend_data.json for the dashboard.
"""

import json, os, re, sys, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "config.json")
OUT_PATH = os.path.join(ROOT, "public", "spend_data.json")
HISTORY_PATH = os.path.join(ROOT, "data", "history.json")

# ── Pricing reference (USD per 1M tokens) ─────────────────────────────────
OPENAI_PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o-mini-2024-07-18": {"input": 0.15, "output": 0.60},
    "gpt-4o-2024-08-06": {"input": 2.50, "output": 10.00},
    "gpt-4o-2024-11-20": {"input": 2.50, "output": 10.00},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "o1": {"input": 15.00, "output": 60.00},
    "o1-mini": {"input": 3.00, "output": 12.00},
    "o3": {"input": 10.00, "output": 40.00},
    "o4-mini": {"input": 1.10, "output": 4.40},
    "gpt-4.1": {"input": 2.00, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
}

ANTHROPIC_PRICING = {
    "claude-opus-4": {"input": 15.00, "output": 75.00},
    "claude-opus-4-5": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
    "claude-sonnet-3-5": {"input": 3.00, "output": 15.00},
    "claude-haiku-3-5": {"input": 0.80, "output": 4.00},
    "claude-haiku-4-5": {"input": 0.80, "output": 4.00},
}


def get_openai_key():
    try:
        cfg = open(os.path.expanduser("~/.openclaw/openclaw.json")).read()
        keys = re.findall(r'sk-proj-[A-Za-z0-9_\-]+', cfg)
        return keys[0] if keys else None
    except:
        return os.environ.get("OPENAI_API_KEY")


def get_elevenlabs_key():
    try:
        cfg = open(os.path.expanduser("~/.openclaw/openclaw.json")).read()
        # ElevenLabs keys start with sk_ 
        keys = re.findall(r'sk_[a-f0-9]{48}', cfg)
        return keys[0] if keys else None
    except:
        return os.environ.get("ELEVENLABS_API_KEY")


def fetch_openai_usage(key, days=30):
    """Fetch OpenAI token usage for the last N days."""
    if not key:
        return []

    results = []
    today = datetime.now(timezone.utc).date()

    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        try:
            req = urllib.request.Request(
                f"https://api.openai.com/v1/usage?date={date_str}",
                headers={"Authorization": f"Bearer {key}"}
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())

            day_cost = 0
            day_tokens_in = 0
            day_tokens_out = 0
            model_breakdown = defaultdict(lambda: {"input": 0, "output": 0, "cost": 0})

            for entry in data.get("data", []):
                model = entry.get("snapshot_id", "unknown")
                n_in = entry.get("n_context_tokens_total", 0)
                n_out = entry.get("n_generated_tokens_total", 0)
                pricing = OPENAI_PRICING.get(model, {"input": 2.50, "output": 10.00})
                cost = (n_in / 1_000_000 * pricing["input"]) + (n_out / 1_000_000 * pricing["output"])
                day_cost += cost
                day_tokens_in += n_in
                day_tokens_out += n_out
                model_breakdown[model]["input"] += n_in
                model_breakdown[model]["output"] += n_out
                model_breakdown[model]["cost"] += cost

            if day_tokens_in > 0 or day_tokens_out > 0:
                results.append({
                    "date": date_str,
                    "provider": "OpenAI",
                    "cost": round(day_cost, 4),
                    "tokens_in": day_tokens_in,
                    "tokens_out": day_tokens_out,
                    "models": dict(model_breakdown),
                })
        except Exception as e:
            pass  # skip days with no data

    return results


def fetch_elevenlabs_usage(key):
    """Fetch ElevenLabs character usage for current billing period."""
    if not key:
        return None
    try:
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/user/subscription",
            headers={"xi-api-key": key}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        chars_used = data.get("character_count", 0)
        chars_limit = data.get("character_limit", 0)
        tier = data.get("tier", "unknown")
        # Rough cost estimate — starter is ~$5/mo, creator $22/mo
        tier_costs = {"free": 0, "starter": 5, "creator": 22, "pro": 99, "scale": 330}
        monthly_cost = tier_costs.get(tier.lower(), 0)
        return {
            "provider": "ElevenLabs",
            "tier": tier,
            "chars_used": chars_used,
            "chars_limit": chars_limit,
            "chars_pct": round(chars_used / chars_limit * 100, 1) if chars_limit else 0,
            "monthly_cost": monthly_cost,
        }
    except Exception as e:
        print(f"  ElevenLabs: {e}")
        return None


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH) as f:
            return json.load(f)
    return {"openai_daily": []}


def save_history(history):
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def build_monthly_totals(daily_usage, config):
    """Build month-by-month totals combining API + subscription costs."""
    now = datetime.now(timezone.utc)
    current_month = now.strftime("%Y-%m")

    # Group API costs by month
    monthly_api = defaultdict(lambda: defaultdict(float))
    for day in daily_usage:
        month = day["date"][:7]
        monthly_api[month][day["provider"]] += day["cost"]

    # Add subscription costs
    months = sorted(set(list(monthly_api.keys()) + [current_month]))
    monthly_totals = []
    for month in months[-6:]:  # last 6 months
        total = 0
        breakdown = {}
        # API costs
        for provider, cost in monthly_api.get(month, {}).items():
            breakdown[provider + " API"] = round(cost, 2)
            total += cost
        # Subscription costs (add for current month and past months)
        for sub in config.get("subscriptions", []):
            if sub.get("active"):
                breakdown[sub["name"]] = sub["cost_monthly"]
                total += sub["cost_monthly"]
        monthly_totals.append({
            "month": month,
            "total": round(total, 2),
            "breakdown": breakdown,
        })

    return monthly_totals


def build_today_stats(daily_usage):
    today = datetime.now(timezone.utc).date().isoformat()
    today_data = [d for d in daily_usage if d["date"] == today]
    return {
        "cost": round(sum(d["cost"] for d in today_data), 4),
        "tokens_in": sum(d["tokens_in"] for d in today_data),
        "tokens_out": sum(d["tokens_out"] for d in today_data),
    }


def build_model_breakdown(daily_usage):
    """Aggregate usage by model across all time."""
    models = defaultdict(lambda: {"tokens_in": 0, "tokens_out": 0, "cost": 0, "provider": "OpenAI"})
    for day in daily_usage:
        for model, stats in day.get("models", {}).items():
            models[model]["tokens_in"] += stats.get("input", 0)
            models[model]["tokens_out"] += stats.get("output", 0)
            models[model]["cost"] += stats.get("cost", 0)
    return [{"model": k, **v} for k, v in sorted(models.items(), key=lambda x: -x[1]["cost"])]


def main():
    print("=== AI Spend Tracker — Fetching Usage ===\n")
    config = load_config()
    history = load_history()

    # Fetch OpenAI
    print("Fetching OpenAI usage...")
    openai_key = get_openai_key()
    openai_daily = fetch_openai_usage(openai_key, days=30)
    if openai_daily:
        print(f"  Got {len(openai_daily)} days of data")
        history["openai_daily"] = openai_daily
    else:
        print("  No OpenAI data (key missing or no usage)")

    # Fetch ElevenLabs
    print("Fetching ElevenLabs usage...")
    eleven_key = get_elevenlabs_key()
    eleven_data = fetch_elevenlabs_usage(eleven_key)
    if eleven_data:
        print(f"  {eleven_data['chars_used']:,} / {eleven_data['chars_limit']:,} chars ({eleven_data['chars_pct']}%)")
        history["elevenlabs"] = eleven_data
    else:
        print("  No ElevenLabs data")

    save_history(history)

    # Build output
    all_daily = history.get("openai_daily", [])
    monthly = build_monthly_totals(all_daily, config)
    today_stats = build_today_stats(all_daily)
    model_breakdown = build_model_breakdown(all_daily)

    # Current month spend
    current_month = datetime.now(timezone.utc).strftime("%Y-%m")
    current_month_data = next((m for m in monthly if m["month"] == current_month), {"total": 0, "breakdown": {}})
    
    # Add subscription costs to current month if not in API data
    sub_total = sum(s["cost_monthly"] for s in config.get("subscriptions", []) if s.get("active"))
    api_total_month = sum(v for k,v in current_month_data["breakdown"].items() if "API" in k)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "budget_monthly": config.get("budget_monthly_usd", 100),
        "current_month": current_month,
        "current_month_total": round(current_month_data["total"], 2),
        "current_month_api": round(api_total_month, 2),
        "current_month_subs": round(sub_total, 2),
        "today": today_stats,
        "monthly_history": monthly,
        "daily_history": sorted(all_daily, key=lambda x: x["date"]),
        "model_breakdown": model_breakdown[:15],
        "subscriptions": config.get("subscriptions", []),
        "elevenlabs": history.get("elevenlabs"),
        "providers": list(set(
            [s["provider"] for s in config.get("subscriptions", [])] +
            [s["provider"] for s in config.get("apis", [])]
        )),
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Output: {OUT_PATH}")
    print(f"   This month: ${output['current_month_total']} (${output['current_month_api']} API + ${output['current_month_subs']} subs)")
    print(f"   Today: ${today_stats['cost']}")


def check_elevenlabs_alert(eleven_data, token):
    """Send Telegram alert if ElevenLabs usage exceeds 80%."""
    if not eleven_data:
        return
    pct = eleven_data.get("chars_pct", 0)
    if pct >= 80:
        chars_used = eleven_data.get("chars_used", 0)
        chars_limit = eleven_data.get("chars_limit", 0)
        msg = f"⚠️ ElevenLabs usage at {pct}% ({chars_used:,}/{chars_limit:,} chars). Consider switching to local TTS or upgrading."
        try:
            payload = json.dumps({"chat_id": "171832539", "text": msg}).encode()
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data=payload, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=10)
            print(f"  ⚠️ Alert sent — ElevenLabs at {pct}%")
        except Exception as e:
            print(f"  Alert failed: {e}")


def get_telegram_token():
    try:
        cfg = json.load(open(os.path.expanduser("~/.openclaw/openclaw.json")))
        tg = cfg.get("channels", {}).get("telegram", {})
        return tg.get("botToken", tg.get("token", ""))
    except:
        return ""


if __name__ == "__main__":
    main()
    # Run alert check after main
    try:
        history = json.load(open(HISTORY_PATH))
        eleven_data = history.get("elevenlabs")
        token = get_telegram_token()
        if token:
            check_elevenlabs_alert(eleven_data, token)
    except Exception as e:
        print(f"Alert check failed: {e}")
