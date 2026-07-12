import streamlit as st

stock_map = {
    "삼성전자": "005930.KS",
    "하이닉스": "000660.KS",
    "네이버": "035420.KS",
    "카카오": "035720.KS"
}

def load_stocks():
    try:
        with open("stocks.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def save_stocks(stocks):
    with open("stocks.txt", "w") as f:
        for s in stocks:
            f.write(s + "\n")

st.title("📈 주식 관리 UI")

stocks = load_stocks()

st.subheader("현재 종목")

if not stocks:
    st.write("종목 없음")
else:
    for i, stock in enumerate(stocks):
        col1, col2 = st.columns([3,1])

        with col1:
            st.write(stock)

        with col2:
            if st.button(f"삭제_{stock}", key=f"del_{stock}_{i}"):
                new_stocks = [s for s in stocks if s != stock]
                save_stocks(new_stocks)
                st.rerun()

st.subheader("종목 추가")

user_input = st.text_input("종목 이름 또는 코드 입력").strip()

if st.button("추가"):
    if user_input:
        code = stock_map.get(user_input, user_input)

        if code not in stocks:
            stocks.append(code)
            save_stocks(stocks)
            st.success(f"{code} 추가됨!")
            st.rerun()
        else:
            st.warning("이미 있는 종목")
    else:
        st.warning("입력하세요")
