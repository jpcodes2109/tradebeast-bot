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

# === Get OI for CE Option (Next weekly expiry, ATM) ===
def fetch_option_oi(symbol):
    try:
        url = f"https://api.upstox.com/v2/option-chain/option-summaries?symbol=NSE_EQ|{symbol}"
        r = requests.get(url, headers=HEADERS)
        data = r.json()["data"]

        ce_oi_list = [entry["open_interest"] for entry in data if entry["option_type"] == "CE"]
        if not ce_oi_list:
            return 0
        avg_oi = sum(ce_oi_list[-5:]) / len(ce_oi_list[-5:])
        return avg_oi
    except Exception as e:
        print(f"❌ OI fetch error for {symbol}: {e}")
        return 0
        
def fetch_equity_quote(symbol):
    try:
        url = f"https://api.upstox.com/v2/market-quote/ltp?symbol=NSE_EQ%7C{symbol}"
        r = requests.get(url, headers=HEADERS)
        print(f"[{symbol}] RAW LTP RESPONSE:", r.text)
        data = r.json()
        stock_data = data["data"][f"NSE_EQ|{symbol}"]
        return {
            "ltp": stock_data["last_price"],
            "vwap": stock_data["last_price"] * 0.985,   # mock vwap
            "volume": 1000000 + 50000                   # mock volume
        }
    except Exception as e:
        print(f"❌ Quote fetch error for {symbol}:", e)
        return None

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

    for symbol in symbols:
        eq = fetch_equity_quote(symbol)
        if not eq: continue

        ltp = eq["ltp"]
        vwap = eq["vwap"]
        volume = eq["volume"]

        volume_x = volume / 1000000  # Dummy multiplier to simulate surge

        oi = fetch_option_oi(symbol)

        if ltp > vwap and volume_x > 1.5 and oi > 100000:
            message = (
                f"🚀 <b>{symbol}</b> trending breakout!\n"
                f"CMP: ₹{ltp} | VWAP: ₹{vwap}\n"
                f"Volume Surge: {volume_x:.1f}x | CE OI: {int(oi)}\n\n"
                f"📈 Consider 1 OTM CE | Trend looks strong"
            )
            send_telegram_message(message)

# === Entry Point ===
if __name__ == "__main__":
    scan_and_alert()
