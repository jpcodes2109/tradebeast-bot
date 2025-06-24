import requests
import os

# === ENV VARS ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
UPSTOX_TOKEN = os.getenv("UPSTOX_TOKEN")

# === HEADERS for Upstox API ===
HEADERS = {
    "Authorization": f"Bearer {UPSTOX_TOKEN}",
    "Accept": "application/json"
}

# === Send Telegram Alert ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, data=payload)
        print("✅ Alert sent:", message)
    except Exception as e:
        print("❌ Telegram error:", e)

# === Get LTP (and mock VWAP/volume) ===
def fetch_equity_quote(isin):
    try:
        url = f"https://api.upstox.com/v2/market-quote/ltp?symbol=NSE_EQ|{isin}"
        r = requests.get(url, headers=HEADERS)
        print(f"[{isin}] RAW LTP RESPONSE:", r.text)
        data = r.json()
        if "data" not in data or f"NSE_EQ|{isin}" not in data["data"]:
            return None
        stock_data = data["data"][f"NSE_EQ|{isin}"]
        ltp = stock_data["last_price"]
        return {
            "ltp": ltp,
            "vwap": ltp * 0.985,       # mock vwap
            "volume": 1000000 + 50000  # mock volume
        }
    except Exception as e:
        print(f"❌ Quote fetch error for {isin}:", e)
        return None

# === Dummy OI Fetch ===
def fetch_option_oi(symbol):
    try:
        # Future: Add real OI logic here
        return 120000  # mock OI
    except Exception as e:
        print(f"❌ OI fetch error for {symbol}:", e)
        return 0

# === Scanner Logic ===
def scan_and_alert():
    symbols = {
        "TATAMOTORS": "INE155A01022",
        "SBIN": "INE062A01020",
        "ICICIBANK": "INE090A01021",
        "RELIANCE": "INE002A01018",
        "HDFCBANK": "INE040A01034",
        "INFY": "INE009A01021"
    }

    for name, isin in symbols.items():
        eq = fetch_equity_quote(isin)
        if not eq: continue

        ltp = eq["ltp"]
        vwap = eq["vwap"]
        volume_x = eq["volume"] / 1000000
        oi = fetch_option_oi(name)

        if ltp > vwap and volume_x > 1.5 and oi > 100000:
            message = (
                f"🚀 <b>{name}</b> trending breakout!\n"
                f"CMP: ₹{ltp} | VWAP: ₹{vwap:.2f}\n"
                f"Volume Surge: {volume_x:.1f}x | CE OI: {int(oi)}\n\n"
                f"📈 Consider 1 OTM CE | Trend looks strong"
            )
            send_telegram_message(message)

# === Entry Point ===
if __name__ == "__main__":
    scan_and_alert()
