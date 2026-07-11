import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

from engine import get_data, score
from trader import signal, action
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
import requests
import time

stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "네이버": "035420.KS",
    "카카오": "035720.KS"
}

def send(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

def run_trade():
    for name, ticker in stocks.items():
        try:
            price, diff, df = get_data(ticker)
            s = score(price, diff, df, name)

            sig = signal(price, df)
            act = action(s)

            print(f"{name} 점수:{s} / {act}")

            # 🔥 자동매매 조건
            if s >= 80:
                msg = f"🚨 [매수 신호]\n{name}\n점수:{s}\n{act}"
                send(msg)

            elif s <= 30:
                msg = f"⚠️ [매도 고려]\n{name}\n점수:{s}"
                send(msg)

        except Exception as e:
            print("에러:", e)

# ⏰ 30분마다 실행
while True:
    print("자동매매 실행중...")
    run_trade()
    time.sleep(1800)