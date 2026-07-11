import streamlit as st
import requests
import os
from engine import get_data, score
from trader import signal, action
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

WATCHLIST_FILE = "watchlist.txt"

# 기본 종목
default_stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "애플": "AAPL",
    "테슬라": "TSLA",
    "엔비디아": "NVDA"
}

# 텔레그램
def send_telegram(msg):
    if TELEGRAM_TOKEN == "":
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

# 관심종목 불러오기
def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return {}
    data = {}
    with open(WATCHLIST_FILE, "r") as f:
        for line in f:
            name, ticker = line.strip().split(",")
            data[name] = ticker
    return data

# 관심종목 저장
def save_watchlist(name, ticker):
    with open(WATCHLIST_FILE, "a") as f:
        f.write(f"{name},{ticker}\n")

st.title("🚀 AI 주식 트레이딩 시스템 (완성형)")

# 👉 관심종목 추가 UI
st.header("⭐ 관심종목 추가")

col1, col2 = st.columns(2)
name = col1.text_input("종목 이름 (예: 네이버)")
ticker = col2.text_input("티커 (예: 035420.KS / AAPL)")

if st.button("➕ 관심종목 저장"):
    if name and ticker:
        save_watchlist(name, ticker)
        st.success("저장 완료!")
    else:
        st.error("이름과 티커 입력하세요")

# 👉 종목 불러오기
stocks = default_stocks.copy()
stocks.update(load_watchlist())

# 👉 분석 버튼
st.header("📊 종목 분석")

if st.button("🔥 전체 분석 실행"):

    results = []

    for name, ticker in stocks.items():
        try:
            price, diff, df = get_data(ticker)
            s = score(price, diff, df, name)
            results.append((name, price, diff, df, s))
        except:
            continue

    results.sort(key=lambda x: x[4], reverse=True)

    msg = "🔥 TOP 종목\n\n"

    for i, (name, price, diff, df, s) in enumerate(results[:5], 1):

        st.subheader(f"{i}위 {name} ({s}점)")
        st.write(f"가격: {price:.2f}")
        st.write(f"고점대비: {diff:.2f}%")

        sig = signal(price, df)
        act = action(s)

        st.write(sig)
        st.write(act)

        line = f"{i}위 {name} ({s}점)\n{sig}\n{act}\n\n"
        msg += line

        if s > 85:
            send_telegram(f"🚨 매수 신호: {name}")

    send_telegram(msg)

# 👉 추천 종목 찾기 (핵심🔥)
st.header("🧠 AI 추천 종목 찾기")

if st.button("🚀 추천 종목 스캔"):

 candidates = [
    "005930.KS",  # 삼성전자
    "000660.KS",  # SK하이닉스
    "035420.KS",  # 네이버
    "035720.KS",  # 카카오
    "051910.KS",  # LG화학
    "006400.KS",  # 삼성SDI
    "207940.KS",  # 삼성바이오
    "068270.KS"   # 셀트리온
]
    best = []

    for ticker in candidates:
        try:
            price, diff, df = get_data(ticker)
            s = score(price, diff, df)
            best.append((ticker, s))
        except:
            continue

    best.sort(key=lambda x: x[1], reverse=True)

    st.subheader("🔥 추천 TOP 3")

    for t, s in best[:3]:
        st.write(f"{t} → {s}점")