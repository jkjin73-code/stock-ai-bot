import yfinance as yf
import time
import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

stocks = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Nvidia": "NVDA",
    "Microsoft": "MSFT",
    "Amazon": "AMZN"
}

def get_stock_data(ticker):
    df = yf.Ticker(ticker).history(period="6mo")
    price = df['Close'].iloc[-1]
    high = df['Close'].max()
    diff = (price - high) / high * 100
    return price, diff, df

def calculate_score(price, diff, df):
    score = 0

    if diff < -40:
        score += 30
    elif diff < -20:
        score += 20

    if df['Close'].iloc[-1] > df['Close'].iloc[-5]:
        score += 20

    ma20 = df['Close'].rolling(20).mean().iloc[-1]
    ma60 = df['Close'].rolling(60).mean().iloc[-1]

    if price > ma20:
        score += 20
    if ma20 > ma60:
        score += 20

    vol_now = df['Volume'].iloc[-1]
    vol_avg = df['Volume'].rolling(20).mean().iloc[-1]

    if vol_now > vol_avg * 1.5:
        score += 20

    return score

def trading_signal(price, df):
    ma20 = df['Close'].rolling(20).mean().iloc[-1]
    support = df['Low'].rolling(10).min().iloc[-1]

    if price > ma20:
        return f"✅ 매수 가능 (지지선: {support:.2f})"
    else:
        return "❌ 아직 아님"

def send_telegram(msg):
    if TELEGRAM_TOKEN == "여기에_토큰":
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

def run():
    print("\n📈 AI 주식 분석 시작\n")

    results = []

    for name, ticker in stocks.items():
        price, diff, df = get_stock_data(ticker)
        score = calculate_score(price, diff, df)
        results.append((name, price, diff, df, score))

    results.sort(key=lambda x: x[4], reverse=True)

    msg = "🔥 TOP 종목\n\n"

    for i, (name, price, diff, df, score) in enumerate(results[:3], start=1):
        signal = trading_signal(price, df)

        line = f"{i}위 {name} ({score}점)\n가격: {price:.2f}\n{signal}\n\n"
        print(line)
        msg += line

        if score > 80:
            alert = f"🚨 강력 매수 후보: {name}"
            print(alert)
            send_telegram(alert)

    send_telegram(msg)

while True:
    run()
    print("⏳ 60초 후 다시 실행...\n")
    time.sleep(60)