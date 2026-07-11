import time
from engine import get_data, score
from trader import signal, action
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
import requests

stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "네이버": "035420.KS",
    "카카오": "035720.KS"
}

def send(msg):
    if TELEGRAM_TOKEN == "":
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

def run_once():
    results = []

    for name, ticker in stocks.items():
        try:
            price, diff, df = get_data(ticker)
            s = score(price, diff, df)
            results.append((name, s))
        except:
            continue

    results.sort(key=lambda x: x[1], reverse=True)

    msg = "📊 자동 분석 결과\n\n"
    for name, s in results:
        msg += f"{name} → {s}점\n"

    send(msg)

# ⏰ 무한 반복 (1시간마다 실행)
while True:
    print("분석 실행중...")
    run_once()
    print("1시간 대기...")
    time.sleep(3600)