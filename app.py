import streamlit as st
st.title("정상 실행됨")
import streamlit as st

# 파일에서 종목 불러오기
def load_stocks():
    try:
        with open("stocks.txt") as f:
            return [line.strip() for line in f]
    except:
        return []

# 파일에 저장
def save_stock(code):
    with open("stocks.txt", "a") as f:
        f.write(code + "\n")

st.title("📈 주식 관리 UI")

# 현재 종목 표시
stocks = load_stocks()
st.subheader("현재 종목")
st.write(stocks)

# 종목 추가
st.subheader("종목 추가")

new_stock = st.text_input("종목 코드 입력 (예: 005930.KS)")

if st.button("추가"):
    if new_stock:
        save_stock(new_stock)
        st.success(f"{new_stock} 추가됨!")
        st.rerun()
    else:
        st.warning("코드를 입력하세요")
