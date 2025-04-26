import streamlit as st

import locale
locale.setlocale(locale.LC_ALL, '')

def calculate_house_price(monthly_payment, annual_rate, years, ltv):
    monthly_rate = annual_rate / 12 / 100
    total_months = years * 12
    loan_amount = monthly_payment * (1 - (1 + monthly_rate) ** (-total_months)) / monthly_rate
    house_price = loan_amount / (ltv / 100)
    return loan_amount, house_price

st.title("🏡 아파트 구매 가능 가격 계산기 by NOWKO")

formatted_default = locale.format_string("%d", 1800000, grouping=True)
monthly_payment_input = st.text_input("월 상환 가능액 (₩)", value=formatted_default)

# 숫자 추출
monthly_payment = int(monthly_payment_input.replace(',', '').replace(' ', '')) if monthly_payment_input else 0

annual_rate = st.number_input("연 이자율 (%)", min_value=0.0, value=5.0)
years = st.number_input("대출 기간 (년)", min_value=1, value=30)
ltv = st.number_input("LTV 비율 (%)", min_value=1.0, max_value=100.0, value=80.0)

if st.button("계산하기"):
    loan_amount, house_price = calculate_house_price(monthly_payment, annual_rate, years, ltv)
    st.success(f"📌 대출 가능 금액: {loan_amount:,.0f} 원")
    st.success(f"📌 구매 가능한 아파트 가격: {house_price:,.0f} 원")

st.caption("※ 월 상환 가능액 기준으로 대출 및 구매 가능한 아파트 가격을 계산합니다.")
