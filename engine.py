from news_ai import get_news_score
import yfinance as yf

def get_data(ticker):
    df = yf.Ticker(ticker).history(period="3mo")
    price = df['Close'].iloc[-1]
    high = df['Close'].max()
    diff = (price - high) / high * 100
    return price, diff, df


def score(price, diff, df, name):  # 🔥 name 추가됨
    s = 0

    # 📉 고점 대비
    if diff < -40:
        s += 30
    elif diff < -20:
        s += 20

    # 📈 단기 상승
    if df['Close'].iloc[-1] > df['Close'].iloc[-5]:
        s += 20

    # 📊 이동평균
    ma20 = df['Close'].rolling(20).mean().iloc[-1]
    ma60 = df['Close'].rolling(60).mean().iloc[-1]

    if price > ma20:
        s += 20
    if ma20 > ma60:
        s += 20

    # 🔊 거래량
    vol = df['Volume'].iloc[-1]
    vol_avg = df['Volume'].rolling(20).mean().iloc[-1]

    if vol > vol_avg * 1.5:
        s += 20

    # 🧠🔥 뉴스 점수 (핵심 추가)
    try:
        news_score, headlines = get_news_score(name)
        s += news_score * 2   # 뉴스 영향력 강화
    except:
        news_score = 0

    return s