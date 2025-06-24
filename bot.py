import requests
import os

# Load your bot credentials from environment variables (Render will provide these)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        print(f"[✔] Sent: {message}")
        return response.json()
    except Exception as e:
        print(f"[❌] Error: {e}")
        return None

# 📊 Mock data — simulate a trending stock scan
mock_stock_data = {
    "TATAMOTORS": {"price": 984, "vwap": 972, "volume_x": 2.1, "oi_change": 12},
    "SBIN": {"price": 585, "vwap": 584.5, "volume_x": 0.8, "oi_change": 5},
    "ICICIBANK": {"price": 1020, "vwap": 1011, "volume_x": 1.7, "oi_change": 15}
}

def scan_and_alert():
    for stock, data in mock_stock_data.items():
        if (
            data["price"] > data["vwap"] and
            data["volume_x"] > 1.5 and
            data["oi_change"] > 10
        ):
            message = (
                f"🚀 <b>{stock}</b> Trending Up!\n"
                f"CMP: ₹{data['price']} | VWAP: ₹{data['vwap']}\n"
                f"Volume Surge ✅ ({data['volume_x']}x) | OI: +{data['oi_change']}%\n\n"
                f"📈 Clean trend forming. Consider 1 OTM CE 🚀"
            )
            send_telegram_message(message)

# 🔁 Run once (Render will restart the container or you can cron it)
if __name__ == "__main__":
    scan_and_alert()
