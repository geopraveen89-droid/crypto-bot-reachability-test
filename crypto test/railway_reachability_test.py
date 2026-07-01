"""
railway_reachability_test.py
------------------------------
A minimal, throwaway script to check whether Railway's servers can reach
the two data sources the live crypto alert bot will depend on:

1. Yahoo Finance (yfinance) - for live daily price data (BTC, ETH, SOL)
2. Binance Futures API - for live funding rate data (the crowding filter)

Deploy this as its own small Railway service, let it run once, and check
the deployment logs. It prints clear PASS/FAIL for each source so we know
before building the real bot whether either data source needs a fallback.

This does NOT need to keep running - it checks both sources once and exits.
"""

import sys
import requests

print("=" * 50)
print("RAILWAY DATA SOURCE REACHABILITY TEST")
print("=" * 50)

# --- Test 1: Yahoo Finance via yfinance ---
print("\n[1/2] Testing Yahoo Finance (yfinance)...")
try:
    import yfinance as yf
    df = yf.download("BTC-USD", period="5d", interval="1d", progress=False)
    if df.empty:
        print("FAIL: yfinance returned no data (empty DataFrame)")
    else:
        print(f"PASS: yfinance reachable. Got {len(df)} rows. "
              f"Latest close: {df['Close'].iloc[-1].item():.2f}")
except Exception as e:
    print(f"FAIL: yfinance raised an exception: {type(e).__name__}: {e}")

# --- Test 2: Binance Futures API (funding rate) ---
print("\n[2/2] Testing Binance Futures API (fapi.binance.com)...")
try:
    resp = requests.get(
        "https://fapi.binance.com/fapi/v1/fundingRate",
        params={"symbol": "BTCUSDT", "limit": 5},
        timeout=10,
    )
    if resp.status_code == 200:
        data = resp.json()
        print(f"PASS: Binance Futures API reachable. Got {len(data)} rows. "
              f"Most recent funding rate: {data[-1]['fundingRate']}")
    else:
        print(f"FAIL: Binance Futures API returned HTTP {resp.status_code}: {resp.text[:200]}")
except Exception as e:
    print(f"FAIL: Binance Futures API raised an exception: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("TEST COMPLETE. Check PASS/FAIL above for each source.")
print("=" * 50)

sys.exit(0)
