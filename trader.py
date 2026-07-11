def signal(price, df):
    ma20 = df['Close'].rolling(20).mean().iloc[-1]
    support = df['Low'].rolling(10).min().iloc[-1]

    if price > ma20:
        return f"✅ 매수 가능 (지지선 {support:.2f})"
    else:
        return "❌ 대기"

def action(score):
    if score > 85:
        return "🔥 강력 매수"
    elif score > 65:
        return "👍 관심"
    else:
        return "⚠️ 관망"