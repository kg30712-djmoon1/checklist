import streamlit as st
from logic import check_comprehensive_score

st.set_page_config(page_title="광주특구 통합 합격 예측", layout="wide")

st.markdown("""
    <style>
    .score-card { background-color: #e3f2fd; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #90caf9; }
    .fail-card { background-color: #ffebee; padding: 10px; border-radius: 5px; color: #c62828; margin-bottom: 5px; }
    .warn-card { background-color: #fff8e1; padding: 10px; border-radius: 5px; color: #f57f17; margin-bottom: 5px; }
    .check-warning { color: red; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 AI 글로벌 빅테크 육성사업 합격 예측 시뮬레이터")
st.info("💡 상단 4개의 탭을 순서대로 모두 입력해야 최종 결과를 확인할 수 있습니다.")

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["① 기본자격", "② 재무건전성", "③ 3책5공(인력)", "④ 가점 및 감점"])

# [Tab 1] 기본 자격
with tab1:
    st.subheader("1단계: 기본 자격 및 제재 확인")
    col_a, col_b = st.columns(2)
    with col_a:
        is_suitability = st.radio("Q1. 공고 자격 충족?", ("적합", "부적합"))
        is_restricted = st.radio("Q2. 참여제한 여부?", ("해당없음", "해당함"))
    with col_b:
        is_duplicated = st.radio("Q3. 과제 중복성?", ("중복없음", "중복됨"))
        is_tax_default = st.radio("Q4. 채무불이행/체납?", ("해당없음", "해당함"))

# [Tab 2] 재무건전성
with tab2:
    st.subheader("2단계: 재무제표 정밀 입력 (단위: 원)")
    with st.expander("📝 재무 데이터 입력창 열기 (클릭)", expanded=True):
        c1, c2, c3 = st.columns(3)
        cap_total = c1.number_input("자본총계", value=100000000, step=1000000, format="%d")
        cap_stock = c1.number_input("자본금", value=50000000, step=1000000, format="%d")
        liab_total = c2.number_input("부채총계", value=150000000, step=1000000, format="%d")
        curr_asset = c3.number_input("유동자산", value=200000000, step=1000000, format="%d")
        curr_liab = c3.number_input("유동부채", value=100000000, step=1000000, format="%d")
        
        c4, c5 = st.columns(2)
        op_income = c4.number_input("영업이익", value=10000000, format="%d")
        int_exp = c5.number_input("이자비용", value=5000000, format="%d")
        
        st.markdown("---")
        st.caption("※ 엑셀 [평가지표] 기준 연속성 체크")
        chk1, chk2 = st.columns(2)
        prev_debt_500 = chk1.checkbox("작년(23년) 부채비율 500% 이상")
        prev_curr_50 = chk1.checkbox("작년(23년) 유동비율 50% 이하")
        loss_3yrs = chk2.checkbox("3년 연속 영업적자")
        audit_opinion = chk2.selectbox("감사의견", ["적정", "한정", "부적정", "의견거절"])

# [Tab 3] 3책 5공
with tab3:
    st.subheader("3단계: 인력 참여 현황 (3책 5공)")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("**[현재 수행 중]**")
        cnt_pi_current = st.number_input("연구책임자(PI)로 수행", value=1, min_value=0)
        cnt_res_current = st.number_input("참여연구원으로 수행", value=0, min_value=0)
    with col_p2:
        st.markdown("**[현재 신청 중]**")
        cnt_pi_applying = st.number_input("연구책임자(PI)로 신청", value=1, min_value=0)
        cnt_res_applying = st.number_input("참여연구원으로 신청", value=0, min_value=0)

# [Tab 4] 가점 및 감점
with tab4:
    st.subheader("4단계: 가점 및 감점 시뮬레이션")
    col_bonus, col_penalty = st.columns(2)
    
    with col_bonus:
        st.markdown("### ➕ 가점 항목 (최대 5점)")
        st.markdown("**1. 입지 및 유형 (3점)**")
        is_rnd_comp = st.checkbox("연구소기업")
        is_high_tech = st.checkbox("첨단기술기업")
        
        st.markdown("**2. 기타 우수 성과 (각 1점)**")
        is_innovative = st.checkbox("우수 혁신성과 기업")
        is_top100 = st.checkbox("국가 우수성과 100선")
        is_ex_lab = st.checkbox("우수 기업부설연구소")
        
    with col_penalty:
        st.markdown("### ➖ 감점 항목")
        is_cancel_sanction = st.checkbox("최근 협약 해약/제재 이력 (1점 감점)")
        is_giveup = st.checkbox("최근 과제 협약 포기 이력 (1점 감점)")

st.markdown("---")

# -----------------------------------------------------------
# [안전장치] 최종 확인 체크박스 (이걸 체크해야 버튼이 활성화됨)
# -----------------------------------------------------------
st.subheader("✅ 최종 제출 전 확인")
check_done = st.checkbox("위 4가지 탭(자격, 재무, 인력, 가점)의 내용을 모두 빠짐없이 확인하고 입력하였습니까?")

if st.button("🚀 종합 진단 및 점수 예측 확인", use_container_width=True):
    if not check_done:
        st.error("🚫 [경고] 위 '확인' 체크박스에 체크해주셔야 결과를 볼 수 있습니다. 모든 탭을 입력했는지 다시 확인해주세요.")
        st.stop()  # 여기서 코드 실행을 멈춤

    # 로직 실행
    report = check_comprehensive_score(
        is_suitability, is_duplicated, is_restricted, is_tax_default,
        cap_total, cap_stock, liab_total, curr_asset, curr_liab, 
        op_income, int_exp, prev_debt_500, prev_curr_50, loss_3yrs, audit_opinion,
        cnt_pi_current, cnt_res_current, cnt_pi_applying, cnt_res_applying,
        is_rnd_comp, is_high_tech, is_innovative, is_top100, is_ex_lab,
        is_cancel_sanction, is_giveup
    )
    
    final_status = report["summary"]
    if final_status == "적격":
        st.success(f"### 🎉 최종 판정: [적격]")
        st.markdown("지원 자격을 충족하며, 결격 사유가 발견되지 않았습니다.")
    elif final_status == "사후관리":
        st.warning(f"### ⚠️ 최종 판정: [사후관리 대상]")
        st.markdown("지원은 가능하나, 재무 상태에 따른 사후관리가 필요합니다.")
    else:
        st.error(f"### 🚫 최종 판정: [부적격]")
        st.markdown("사전지원제외 대상에 해당하여 지원이 불가능할 수 있습니다.")

    st.divider()

    c1, c2, c3 = st.columns([1.2, 1.2, 1])
    
    with c1:
        st.markdown("#### 1️⃣ 결격사유")
        all_fails = []
        all_fails.extend(report["1_eligibility"]["msgs"])
        all_fails.extend(report["2_sanction"]["msgs"])
        if report["3_financial"]["status"] == "FAIL":
            for m in report["3_financial"]["msgs"]:
                if m["type"] == "RED": all_fails.append(m["text"])
        all_fails.extend(report["4_3n5"]["msgs"])
        
        if not all_fails: st.info("✅ 결격 사유 없음")
        else:
            for fail in all_fails: st.markdown(f'<div class="fail-card">❌ {fail}</div>', unsafe_allow_html=True)
                
    with c2:
        st.markdown("#### 2️⃣ 사후관리")
        warns = []
        if report["3_financial"]["status"] == "WARN":
            for m in report["3_financial"]["msgs"]:
                if m["type"] == "YELLOW": warns.append(m["text"])
        
        if not warns: st.info("✅ 특이사항 없음")
        else:
            for w in warns: st.markdown(f'<div class="warn-card">⚠️ {w}</div>', unsafe_allow_html=True)
                
    with c3:
        st.markdown("#### 3️⃣ 가/감점 예측")
        score_data = report["5_score"]
        st.markdown(f"""
        <div class="score-card">
            <h3>📊 총점: +{score_data['final']}점</h3>
            <hr>
            <p>➕ 가점: {score_data['bonus']}점 (Max 5)</p>
            <p>➖ 감점: -{score_data['penalty']}점</p>
        </div>
        """, unsafe_allow_html=True)
