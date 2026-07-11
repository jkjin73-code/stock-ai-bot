import feedparser

# 간단 감정 키워드
positive_words = ["상승", "호재", "성장", "수익", "확대", "계약"]
negative_words = ["하락", "악재", "손실", "감소", "우려", "적자"]

def get_news_score(keyword):
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)

    score = 0
    headlines = []

    for entry in feed.entries[:5]:
        title = entry.title
        headlines.append(title)

        for p in positive_words:
            if p in title:
                score += 1

        for n in negative_words:
            if n in title:
                score -= 1

    return score, headlines