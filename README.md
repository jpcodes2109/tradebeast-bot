# TradeBeast Telegram Bot 🚀

A cloud-deployed Python bot that sends Telegram alerts when trending stocks are detected based on:
- Price > VWAP & EMA
- Volume surge
- Increasing Open Interest (OI)

## How it works
Currently uses mock data — can be connected to NSE/Chartink APIs easily.

## Deployment
Use [Render](https://render.com) to deploy this bot with the following environment variables:

- `BOT_TOKEN`: Your Telegram bot token
- `CHAT_ID`: Your Telegram numeric user ID

## Future upgrades
- Real-time data feed
- Chartink integration
- Options recommendation
