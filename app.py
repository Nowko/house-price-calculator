import streamlit as st

def calculate_house_price(monthly_payment, annual_rate, years, ltv):
    monthly_rate = annual_rate / 12 / 100
    total_months = years * 12
    loan_amount = monthly_payment * (1 - (1 + monthly_rate) ** (-total_months)) / monthly_rate
    house_price = loan_amount / (ltv / 100)
    return loan_amount, house_price

st.title("🏡 아파트 구매 가능 가격 계산기 by NOWKO")

# 월 상환 가능액을 number_input으로 설정 (조정 단위: 10,000원)
monthly_payment = st.number_input(
    "월 상환 가능액 (₩)", 
    min_value=0, 
    value=1800000, 
    step=10000, 
    format="%d"
)

annual_rate = st.number_input("연 이자율 (%)", min_value=0.0, value=5.0)
years = st.number_input("대출 기간 (년)", min_value=1, value=30)
ltv = st.number_input("LTV 비율 (%)", min_value=1.0, max_value=100.0, value=80.0)

if st.button("계산하기"):
    loan_amount, house_price = calculate_house_price(monthly_payment, annual_rate, years, ltv)
    st.success(f"📌 대출 가능 금액: {loan_amount:,.0f} 원")
    st.success(f"📌 구매 가능한 아파트 가격: {house_price:,.0f} 원")

st.caption("※ 월 상환 가능액 기준으로 대출 및 구매 가능한 아파트 가격을 계산합니다.")
