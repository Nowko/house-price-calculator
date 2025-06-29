import streamlit as st

# 대출원리금 균등상환 계산 함수
def calculate_house_price(monthly_payment, annual_rate, years, ltv):
    monthly_rate = annual_rate / 12 / 100
    total_months = years * 12
    loan_amount = monthly_payment * (1 - (1 + monthly_rate) ** (-total_months)) / monthly_rate
    house_price = loan_amount / (ltv / 100)
    return loan_amount, house_price

# 앱 제목 및 설명
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

# 2) 계산 버튼: 입력된 값으로 결과 도출
if st.button("🧮 계산하기"):
    # 2-1) 최대 월 납입 가능액 (예시)
    max_monthly_payment = salary * (dsr / 100)

    # 2-2) 실제 월 원리금 상환액 입력 (기본: 최대 가능액)
    monthly_payment = st.number_input(
        "월 원리금 상환 가능액 (₩)",
        min_value=0,
        value=int(max_monthly_payment),
        step=10000
    )
    # 이자율, 기간, LTV, 전세금 입력
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
    jeonse = st.number_input(
        "보유 중인 전세금 (₩)",
        min_value=0,
        value=30000000,
        step=1000000
    )

    # 대출 원금 및 구매 가능 집값 계산
    loan_amount, house_price = calculate_house_price(
        monthly_payment, annual_rate, years, ltv
    )
    additional_needed = (house_price - loan_amount) - jeonse

    # 1) 구매 가능한 아파트 가격
    house_price_eok = house_price / 100000000
    st.subheader(f"🏠 구매 가능한 아파트 가격: {house_price_eok:.2f}억 원")

    # 2) 가격 준비 방법
    st.write(f"- 💰 대출: {loan_amount/10000:,.0f}만 원")
    st.write(f"- 🏦 전세금: {jeonse/10000:,.0f}만 원")
    st.write(f"- ➕ 추가로 필요한 금액: {max(0, additional_needed)/10000:,.0f}만 원")

    # 3) 참고 사항
    monthly_payment_million = monthly_payment / 10000
    st.caption(
        f"📌 현재 월 {monthly_payment_million:,.0f}만 원의 월세가 나간다면, {house_price_eok:.2f}억 원의 집 구매를 고려해볼 만합니다."
    )
