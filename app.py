import streamlit as st
from logic import check_financial_detail

st.set_page_config(page_title="광주특구 재무 정밀 진단", layout="wide")

st.markdown("""
    <style>
    .red-box { border-left: 5px solid #ff4b4b; background-color: #ffeaea; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .yellow-box { border-left: 5px solid #ffa700; background-color: #fff9e6; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .metric-card { background-color: #f0f2f6; padding: 10px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("💰 재무제표 정밀 자가진단 (엑셀 기준)")
st.info("첨부된 '재무제표.csv' 파일의 [사전제외/사후관리] 상세 기준을 적용하여 분석합니다.")

with st.form("financial_form"):
    st.markdown("### 1️⃣ 재무상태표 정보 (2024년 말 기준)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("자본 관련")
        cap_stock = st.number_input("자본금 (원)", value=50000000, step=1000000, format="%d")
        cap_total = st.number_input("자본총계 (원)", value=80000000, step=1000000, format="%d")
    with col2:
        st.caption("부채 관련")
        liab_total = st.number_input("부채총계 (원)", value=120000000, step=1000000, format="%d")
    with col3:
        st.caption("유동성 관련")
        curr_asset = st.number_input("유동자산 (원)", value=100000000, step=1000000, format="%d")
        curr_liab = st.number_input("유동부채 (원)", value=80000000, step=1000000, format="%d")

    st.markdown("---")
    st.markdown("### 2️⃣ 손익계산서 정보 (2024년 기준)")
    c1, c2 = st.columns(2)
    with c1:
        op_income = st.number_input("영업이익 (원)", value=10000000, step=1000000, format="%d", help="손실일 경우 마이너스(-) 입력")
    with c2:
        int_exp = st.number_input("이자비용 (원)", value=5000000, step=100000, format="%d", help="이자보상비율 계산용")

    st.markdown("---")
    st.markdown("### 3️⃣ 이력 및 기타 확인 (연속성 체크)")
    st.warning("⚠️ 엑셀 기준에 따라 '연속' 여부를 판단하니 정확히 체크해주세요.")
    
    chk1, chk2 = st.columns(2)
    with chk1:
        prev_debt_500 = st.checkbox("작년(23년) 부채비율이 500% 이상이었습니까?")
        prev_curr_50 = st.checkbox("작년(23년) 유동비율이 50% 이하이었습니까?")
    with chk2:
        loss_3yrs = st.checkbox("최근 3년(22, 23, 24) 연속 영업이익 적자입니까?")
        tax_default = st.checkbox("현재 국세/지방세 체납 또는 채무불이행 상태입니까?")
        
    audit_opinion = st.selectbox("최근 재무제표 감사의견", ["적정(해당없음)", "한정", "부적정", "의견거절"])

    submit = st.form_submit_button("📋 정밀 진단 결과 확인", use_container_width=True)

if submit:
    # 로직 실행
    res, debt_r, curr_r, icr = check_financial_detail(
        cap_total, cap_stock, liab_total, curr_asset, curr_liab,
        op_income, int_exp, prev_debt_500, prev_curr_50, loss_3yrs, audit_opinion, tax_default
    )

    st.divider()
    
    # 1. 핵심 지표 대시보드
    m1, m2, m3 = st.columns(3)
    m1.metric("부채비율", f"{debt_r:.1f}%", delta="300% 이상 주의" if debt_r >= 300 else "안정", delta_color="inverse")
    m2.metric("유동비율", f"{curr_r:.1f}%", delta="100% 이하 주의" if curr_r <= 100 else "안정")
    m3.metric("이자보상비율", f"{icr:.2f}배", delta="1배 미만 주의" if icr < 1 else "양호")

    # 2. 진단 결과 출력
    if not res["red"] and not res["yellow"]:
        st.balloons()
        st.success("✅ **[진단 결과: 적격]** 모든 재무 지표가 안정권입니다.")
    
    else:
        # 사전제외 (Red)
        if res["red"]:
            st.error(f"🚫 **[사전지원 제외 대상]** {len(res['red'])}건의 중대 결격 사유가 발견되었습니다.")
            for item in res["red"]:
                st.markdown(f"""
                <div class="red-box">
                    <b>[항목] {item['항목']}</b><br>
                    • 원인: {item['내용']}<br>
                    • 💡 조치: {item['조치']}
                </div>
                """, unsafe_allow_html=True)
        
        # 사후관리 (Yellow)
        if res["yellow"]:
            st.warning(f"⚠️ **[사후관리 대상]** {len(res['yellow'])}건의 주의 지표가 있습니다. (지원 가능하나 관리 필요)")
            for msg in res["yellow"]:
                st.markdown(f"""
                <div class="yellow-box">
                    • {msg}
                </div>
                """, unsafe_allow_html=True)
            st.caption("※ 사후관리 대상은 선정 후 재무상태 개선 계획 제출이나 별도 진도 점검이 진행될 수 있습니다.")
