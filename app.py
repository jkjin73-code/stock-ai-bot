import streamlit as st

# 👉 종목 이름 ↔ 코드 매핑
stock_map = {
    "삼성전자": "005930.KS",
    "하이닉스": "000660.KS",
    "네이버": "035420.KS",
    "카카오": "035720.KS"
}

# 👉 코드 → 이름 변환용
reverse_map = {v: k for k, v in stock_map.items()}

# ------------------------
# 파일 로드
# ------------------------
def load_stocks():
    try:
        with open("stocks.txt") as f:
            return [line.strip().replace(" ", "") for line in f if line.strip()]
    except:
        return []

# ------------------------
# 파일 저장
# ------------------------
def save_stocks(stocks):
    with open("stocks.txt", "w") as f:
        for s in stocks:
            f.write(s + "\n")

st.title("📈 주식 관리 UI")

stocks = load_stocks()

# ------------------------
# 현재 종목 + 삭제
# ------------------------
st.subheader("현재 종목")

if not stocks:
    st.write("종목 없음")
else:
    for i, stock in enumerate(stocks):
        name = reverse_map.get(stock, "알수없음")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"{name} ({stock})")

        with col2:
            if st.button("삭제", key=f"del_{stock}_{i}"):
                new_stocks = [s for s in stocks if s != stock]
                save_stocks(new_stocks)
                st.rerun()

# ------------------------
# 종목 검색 (자동 추천)
# ------------------------
st.subheader("종목 검색")

search = st.text_input("종목 이름 입력 (예: 삼, 네, 카)", key="search_box").strip()

filtered = []

if search:
    for name in stock_map.keys():
        if search in name:
            filtered.append(name)

# 추천 리스트
if filtered:
    st.write("추천 종목:")
    for i, name in enumerate(filtered):
        if st.button(name, key=f"add_{name}_{i}"):
            code = stock_map[name]
            if code not in stocks:
                stocks.append(code)
                save_stocks(stocks)
                st.success(f"{name} 추가됨!")
                st.rerun()
            else:
                st.warning("이미 있는 종목")

# ------------------------
# 직접 코드 추가
# ------------------------
st.subheader("직접 코드 추가")

code_input = st.text_input("코드 입력 (예: 005930.KS)", key="code_box").strip()

if st.button("코드로 추가"):
    if code_input:
        if code_input not in stocks:
            stocks.append(code_input)
            save_stocks(stocks)
            st.success(f"{code_input} 추가됨!")
            st.rerun()
        else:
            st.warning("이미 있는 종목")
    else:
        st.warning("코드를 입력하세요")
