import streamlit as st

# 대출원리금 균등상환으로 계산하는 함수 정의
def calculate_house_price(monthly_payment, annual_rate, years, ltv):
    monthly_rate = annual_rate / 12 / 100
    total_months = years * 12
    loan_amount = monthly_payment * (1 - (1 + monthly_rate) ** (-total_months)) / monthly_rate
    house_price = loan_amount / (ltv / 100)
    return loan_amount, house_price

# 앱 타이틀 및 설명
st.title("🏡 내가 살 수 있는 집은 얼마?")
st.caption("made by NOWKO on Brunch")

# 1) 급여 및 DSR 입력
salary = st.number_input(
    "월 급여 (₩)",
    min_value=0,
    value=3500000,
    step=100000
)
dsr = st.number_input(
    "DSR (%)",
    min_value=0.0,
    max_value=100.0,
    value=40.0,
    step=0.1
)
# 최대 월 납입 가능액 예시 계산
max_monthly_payment = salary * (dsr / 100)
max_monthly_million = max_monthly_payment / 10000
st.info(f"💡 계산된 최대 월 납입 가능액: {max_monthly_payment:,.0f}원 ({max_monthly_million:,.0f}만 원)")

# 2) 실제 월 상환액 입력 (기본값: 계산된 최대 납입액)
monthly_payment = st.number_input(
    "월 원리금이자 가능액 (₩)",
    min_value=0,
    value=int(max_monthly_payment),
    step=10000
)
monthly_payment_million = monthly_payment / 10000
st.caption(f"현재 입력된 월 상환 가능액: {monthly_payment_million:,.0f}만 원")

# 3) 이자율, 기간, LTV 입력
annual_rate = st.number_input("연 이자율 (%)", min_value=0.0, value=5.0)
years = st.number_input("대출 기간 (년)", min_value=1, value=30)
ltv = st.number_input(
    "LTV 비율 (%)",
    min_value=1,
    max_value=100,
    value=80,
    step=1,
    format="%d"
)

# 4) 전세금 입력: 100만 원 단위 조정
jeonse = st.number_input(
    "보유 중인 전세금 (₩)",
    min_value=0,
    value=30000000,
    step=1000000
)
jeonse_million = jeonse / 10000
st.caption(f"현재 입력된 전세금: {jeonse_million:,.0f}만 원")

# 계산 및 결과 출력
if st.button("🧮 계산하기"):
    loan_amount, house_price = calculate_house_price(
        monthly_payment, annual_rate, years, ltv
    )
    my_cash = house_price - loan_amount
    my_cash_ratio = my_cash / house_price * 100
    additional_needed = my_cash - jeonse

    st.success(f"📌 대출 가능 금액: {loan_amount:,.0f} 원")
    st.success(f"📌 구매 가능한 아파트 가격: {house_price:,.0f} 원")
    st.info(f"💰 내가 준비해야 할 현금: {my_cash:,.0f} 원 ({my_cash_ratio:.1f}%)")

    if jeonse > 0:
        if additional_needed > 0:
            st.warning(
                f"📉 전세금을 제외하고 추가로 더 필요한 금액: {additional_needed:,.0f} 원"
            )
        else:
            st.success(
                f"✅ 전세금으로 충분합니다! 여유 금액: {abs(additional_needed):,.0f} 원"
            )

    # 추가 문구: 억 원 단위 안내
    house_price_eok = house_price / 100000000  # 억 원 단위
    st.info(
        f"📢 현재 {monthly_payment_million:,.0f}만 원으로 월세를 살고 있다면,\n"
        f"{house_price_eok:.2f}억 원 수준의 아파트 구매를 고려해 볼 수 있습니다."
    )
