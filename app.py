import streamlit as st

# 대출원리금 균등상환 계산 함수
def calculate_house_price(monthly_payment, annual_rate, years, ltv):
    r = annual_rate / 12 / 100
    n = years * 12
    loan = monthly_payment * (1 - (1 + r) ** -n) / r
    price = loan / (ltv / 100)
    return loan, price

# 앱 제목 및 설명
st.title("🏡 내가 살 수 있는 집은 얼마?")
st.caption("made by NOWKO on Brunch")

# 1단계: 급여 및 DSR 입력
salary = st.number_input("월 급여 (₩)", min_value=0, value=3500000, step=100000)
dsr = st.number_input("DSR (%)", min_value=0.0, max_value=100.0, value=40.0, step=0.1)

# 1단계 계산 버튼
if st.button("🧮 ① 최대 월 납입 가능액 계산하기"):
    st.session_state.max_payment = salary * dsr / 100

# 1단계 완료 시: 최대 월 납입 가능액 표시 및 2단계 입력 표시
if "max_payment" in st.session_state:
    max_pay = st.session_state.max_payment
    st.success(f"💡 최대 월 납입 가능액: {max_pay:,.0f}원 ({max_pay/10000:,.0f}만 원)")

    # 2단계: 추가 입력
    monthly_payment = st.number_input(
        "월 원리금 상환액 (₩)", min_value=0,
        value=int(max_pay), step=10000
    )
    annual_rate = st.number_input("연 이자율 (%)", min_value=0.0, value=5.0)
    years = st.number_input("대출 기간 (년)", min_value=1, value=30)
    ltv = st.number_input("LTV (%)", min_value=1, max_value=100, value=80, step=1)
    jeonse = st.number_input("보유 중인 전세금 (₩)", min_value=0, value=30000000, step=1000000)

    # 2단계 계산 버튼
    if st.button("🧮 ② 구매 가능 금액 계산하기"):
        # 대출 및 집값 계산
        loan_amount, house_price = calculate_house_price(
            monthly_payment, annual_rate, years, ltv
        )
        # 추가로 필요한 현금 (전세금 제외)
        need = (house_price - loan_amount) - jeonse
        # 억 단위 변환
        house_eok = house_price / 100000000
        # 만원 단위 계산
        loan_million = loan_amount / 10000
        jeonse_million = jeonse / 10000
        need_million = max(0, need) / 10000
        monthly_rent_million = monthly_payment / 10000

        # 결과 출력
        st.subheader(f"🏠 구매 가능한 아파트 가격: {house_eok:.2f}억 원")
        st.write(f"- 💰 대출: {loan_million:,.0f}만 원")
        st.write(f"- 🏦 전세금: {jeonse_million:,.0f}만 원")
        st.write(f"- ➕ 추가로 필요한 금액: {need_million:,.0f}만 원")

        # 수정된 참고 문구
        st.caption(
            f"📌 현재 {need_million:,.0f}만 원이 있고, 월 {monthly_rent_million:,.0f}만 원의 월세가 나간다면, {house_eok:.2f}억 원의 집 구매를 고려해볼 만합니다."
        )
