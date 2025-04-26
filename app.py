import streamlit as st

def calculate_house_price(monthly_payment, annual_rate, years, ltv):
    monthly_rate = annual_rate / 12 / 100
    total_months = years * 12
    loan_amount = monthly_payment * (1 - (1 + monthly_rate) ** (-total_months)) / monthly_rate
    house_price = loan_amount / (ltv / 100)
    return loan_amount, house_price

st.title("🏡 내가 살 수 있는 집은 얼마?")
st.caption("made by NOWKO on Brunch")

# 월 상환 가능액 입력
monthly_payment = st.number_input(
    "월 원리금이자 가능액 (₩)",
    min_value=0,
    value=1800000,
    step=10000
)
# 입력 금액을 '만 원' 단위로 보조 표시
monthly_payment_million = monthly_payment / 10000
st.caption(f"현재 입력된 월 상환 가능액: {monthly_payment_million:,.0f}만 원")

# 이자율, 기간, LTV
annual_rate = st.number_input("연 이자율 (%)", min_value=0.0, value=5.0)
years = st.number_input("대출 기간 (년)", min_value=1, value=30)
ltv = st.number_input( "LTV 비율 (%)",
    min_value=1,
    max_value=100,
    value=80,
    step=1,
    format="%d" )

# 전세금 입력: 100만 원 단위 조정
jeonse = st.number_input(
    "보유 중인 전세금 (₩)",
    min_value=0,
    value=30000000,
    step=1000000
)
jeonse_million = jeonse / 10000
st.caption(f"현재 입력된 전세금: {jeonse_million:,.0f}만 원")

# 계산
if st.button("🧮 계산하기"):
    loan_amount, house_price = calculate_house_price(monthly_payment, annual_rate, years, ltv)
    my_cash = house_price - loan_amount
    my_cash_ratio = my_cash / house_price * 100
    additional_needed = my_cash - jeonse

    st.success(f"📌 대출 가능 금액: {loan_amount:,.0f} 원")
    st.success(f"📌 구매 가능한 아파트 가격: {house_price:,.0f} 원")
    st.info(f"💰 내가 준비해야 할 현금: {my_cash:,.0f} 원 ({my_cash_ratio:.1f}%)")

    if jeonse > 0:
        if additional_needed > 0:
            st.warning(f"📉 전세금을 제외하고 추가로 더 필요한 금액: {additional_needed:,.0f} 원")
        else:
            st.success(f"✅ 전세금으로 충분합니다! 여유 금액: {abs(additional_needed):,.0f} 원")

    # 🆕 추가된 문구
    st.info(f"📢 현재 {monthly_payment_million:,.0f}만 원으로 월세를 살고 있다면,\n {house_price:,.0f} 원 수준의 아파트 구매를 고려해 볼 수 있습니다.")
