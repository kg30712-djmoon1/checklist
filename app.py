import streamlit as st
from logic import check_final_diagnosis

st.set_page_config(page_title="광주특구 통합 정밀 진단", layout="wide")

st.markdown("""
    <style>
    .big-font { font-size:18px !important; font-weight: bold; }
    .success-box { padding:15px; background-color:#d4edda; color:#155724; border-radius:5px; }
    .fail-box { padding:15px; background-color:#f8d7da; color:#721c24; border-radius:5px; }
    .warn-box { padding:15px; background-color:#fff3cd; color:#856404; border-radius:5px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ AI 글로벌 빅테크 육성사업 통합 사전검토")
st.caption("공고 적합성, 차별성, 제재조치, 재무현황을 종합적으로 진단합니다.")

# 탭 구성 (카테고리별 분리)
tab1, tab2, tab3 = st.tabs(["① 공고 적합성", "② 차별성 및 제재", "③ 재무현황(정밀)"])

# --- Tab 1: 공고 적합성 ---
with tab1:
    st.markdown("#### 🏢 공고 신청자격 확인")
    is_suitability = st.radio(
        "Q1. 공고문에 명시된 신청 자격(소재지, 업력, 기업유형 등)을 충족합니까?",
        ("적합", "부적합"), help="지침 제2호 및 공고문 참조"
    )

# --- Tab 2: 차별성 및 제재 ---
with tab2:
    st.markdown("#### 🚫 제재조치 및 중복성 확인")
    col_a, col_b = st.columns(2)
    with col_a:
        is_duplicated = st.radio("Q2. 기개발/기지원 과제와 중복됩니까?", ("중복없음", "중복됨"))
        is_restricted = st.radio("Q3. 국가연구개발사업 참여제한 중입니까?", ("해당없음", "해당함"))
    with col_b:
        is_tax_default = st.radio("Q4. 국세/지방세 체납 또는 채무불이행 상태입니까?", ("해당없음", "해당함"))

# --- Tab 3: 재무현황 ---
with tab3:
    st.markdown("#### 💰 재무제표 정밀 입력 (24년도 결산 기준)")
    st.info("※ 엑셀 파일의 [사전지원제외] 및 [사후관리] 세부 기준이 적용됩니다.")
    
    with st.expander("📝 재무 수치 입력 (클릭)", expanded=True):
        c1, c2, c3 = st.columns(3)
        cap_total = c1.number_input("자본총계", value=100000000, step=1000000)
        cap_stock = c1.number_input("자본금", value=50000000, step=1000000)
        
        liab_total = c2.number_input("부채총계", value=150000000, step=1000000)
        curr_asset = c3.number_input("유동자산", value=200000000, step=1000000)
        curr_liab = c3.number_input("유동부채", value=100000000, step=1000000)
        
        c4, c5 = st.columns(2)
        op_income = c4.number_input("영업이익", value=10000000)
        int_exp = c5.number_input("이자비용", value=5000000)

    with st.expander("🕰️ 과거 이력 확인 (연속성 체크)", expanded=True):
        chk1, chk2 = st.columns(2)
        prev_debt_500 = chk1.checkbox("작년(23년) 부채비율 500% 이상")
        prev_curr_50 = chk1.checkbox("작년(23년) 유동비율 50% 이하")
        loss_3yrs = chk2.checkbox("최근 3년 연속 영업적자")
        audit_opinion = chk2.selectbox("감사의견", ["적정", "한정", "부적정", "의견거절"])

st.markdown("---")
# 진단 실행
if st.button("📊 통합 검토 리포트 생성", use_container_width=True):
    report = check_final_diagnosis(
        is_suitability, is_duplicated, is_restricted, is_tax_default,
        cap_total, cap_stock, liab_total, curr_asset, curr_liab, 
        op_income, int_exp, prev_debt_500, prev_curr_50, loss_3yrs, audit_opinion
    )

    # 결과 출력
    st.subheader(f"종합 판정 결과: [{report['summary']}]")
    
    # 카테고리별 카드 출력
    cols = st.columns(3)
    
    # 1. 공고 적합성 결과
    with cols[0]:
        st.markdown("**① 공고 적합성**")
        if report["1_eligibility"]["status"] == "PASS":
            st.markdown('<div class="success-box">✅ 적합</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fail-box">❌ 부적합</div>', unsafe_allow_html=True)
            for msg in report["1_eligibility"]["msgs"]:
                st.caption(f"- {msg['text']}")

    # 2. 제재 및 차별성 결과
    with cols[1]:
        st.markdown("**② 차별성/제재**")
        if report["2_sanction"]["status"] == "PASS":
            st.markdown('<div class="success-box">✅ 해당 없음</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fail-box">❌ 제재 대상</div>', unsafe_allow_html=True)
            for msg in report["2_sanction"]["msgs"]:
                st.caption(f"- {msg['text']}")

    # 3. 재무현황 결과 (가장 중요)
    with cols[2]:
        st.markdown("**③ 재무현황**")
        status = report["3_financial"]["status"]
        if status == "PASS":
            st.markdown('<div class="success-box">✅ 재무 건전</div>', unsafe_allow_html=True)
        elif status == "WARN":
            st.markdown('<div class="warn-box">⚠️ 사후관리 대상</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fail-box">❌ 지원 제외</div>', unsafe_allow_html=True)
        
        for msg in report["3_financial"]["msgs"]:
            icon = "🔴" if msg['type'] == "RED" else "🟡"
            st.caption(f"{icon} {msg['text']}")
