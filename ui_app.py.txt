import streamlit as st
import yfinance as yf

stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "애플": "AAPL",
    "테슬라": "TSLA"
"LG에너지솔루션": "373220.KS",
"카카오": "035720.KS",
"네이버": "035420.KS"
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
    if price > ma20:
        score += 30

    return score

st.title("📈 AI 주식 분석기")

if st.button("🔥 분석 시작"):
    results = []

    for name, ticker in stocks.items():
        price, diff, df = get_stock_data(ticker)
        score = calculate_score(price, diff, df)
        results.append((name, price, diff, score))

    results.sort(key=lambda x: x[3], reverse=True)

    for name, price, diff, score in results:
        st.subheader(f"{name} ({score}점)")
        st.write(f"가격: {price:.2f}")
        st.write(f"고점대비: {diff:.2f}%")

def auto_trade_signal(name, score):
    if score > 80:
        return f"🚨 매수 신호: {name}"
    return None

signal = auto_trade_signal(name, score)
if signal:
    st.error(signal)

import requests

def send_telegram(msg):
    token = "8911234620:AAG_aPZ3tLyNVcFkKv_m21lzH0Pmto-RzGw"
    chat_id = "7571519693"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": msg})

send_telegram(f"{name} 추천 (점수 {score})")