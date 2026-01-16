import streamlit as st
from logic import check_comprehensive

# 1. 페이지 디자인 설정
st.set_page_config(page_title="사전검토 통합 자가진단", layout="wide")

st.markdown("""
    <style>
    .big-font { font-size:20px !important; font-weight: 600; color: #2c3e50; }
    .tip-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 딥테크 스케일업밸리 육성사업 사전검토")
st.markdown("---")

# 2. 화면 구성 (2단 분할)
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.markdown('<p class="big-font">📑 [Step 1] 기본 자격 요건 (O/X 점검)</p>', unsafe_allow_html=True)
    st.info("💡 행정적인 결격 사유가 없는지 먼저 확인하는 단계입니다.")
    
    with st.container():
        st.write("**1. 참여제한 (NTIS 확인)**")
        is_restricted = st.radio(
            "귀 기관(또는 책임자)이 현재 국가연구개발사업 참여제한 중입니까?",
            ("아니오 (참여 가능)", "예 (참여 제한 중)"),
            index=0,
            help="NTIS 사이트에서 제재정보 조회를 통해 확인 가능합니다."
        )
        
        st.write("**2. 채무불이행 (Cretop 확인)**")
        is_default = st.radio(
            "국세/지방세 체납 또는 채무불이행자로 등재되어 있습니까?",
            ("아니오 (깨끗함)", "예 (체납/불이행 존재)"),
            index=0,
            help="신용회복지원 등 예외 사유가 없다면 부적격 처리됩니다."
        )

        st.write("**3. 과제 중복성**")
        is_duplicated = st.radio(
            "신청하려는 기술이 이미 정부 지원을 받은 적이 있습니까?",
            ("아니오 (신규 과제)", "예 (중복 과제)"),
            index=0
        )
        
        st.write("**4. 공고 자격 적합성**")
        is_suitability = st.radio(
            "공고문에 명시된 신청 자격(업력, 소재지 등)을 충족합니까?",
            ("예 (충족함)", "아니오 (미충족)"),
            index=0
        )

with col_right:
    st.markdown('<p class="big-font">📊 [Step 2] 재무 및 인력 정밀 진단</p>', unsafe_allow_html=True)
    st.warning("🧮 최근 회계연도 말 '결산 재무제표'를 보고 정확히 입력해주세요.")
    
    # 입력 필드를 카드처럼 감싸기
    with st.expander("📝 재무 데이터 입력 (클릭하여 열기)", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            cap = st.number_input("자본총계 (원)", value=100000000, format="%d")
            curr_a = st.number_input("유동자산 (원)", value=200000000, format="%d")
        with c2:
            db = st.number_input("부채총계 (원)", value=150000000, format="%d")
            curr_d = st.number_input("유동부채 (원)", value=100000000, format="%d")
            
    with st.expander("👥 연구 인력 현황 (3책 5공)", expanded=True):
        proj = st.number_input("연구책임자가 현재 수행 중인 정부 과제 수", value=1, min_value=0)
        st.caption("※ 협약 월 기준으로 6개월 이내 종료되는 과제는 제외하고 산정하세요.")

# 3. 진단 버튼 및 결과
st.markdown("---")
if st.button("🚀 통합 진단 결과 리포트 생성", use_container_width=True):
    
    # 텍스트 답변을 로직용 데이터로 변환 (매핑)
    map_restricted = "해당함" if "예" in is_restricted else "해당없음"
    map_default = "해당함" if "예" in is_default else "해당없음"
    map_duplicated = "중복됨" if "예" in is_duplicated else "중복없음"
    map_suitability = "부적합" if "아니오" in is_suitability else "적합"
    
    # 로직 실행
    results = check_comprehensive(cap, db, proj, map_restricted, map_duplicated, map_default, map_suitability)
    
    # 결과 출력 디자인
    if not results:
        st.balloons()
        st.success("### 🎉 [최종 판정: 적격]")
        st.markdown("귀 기관은 **재무 건전성** 및 **행정 자격 요건**을 모두 충족하고 있습니다.")
        st.markdown("신청서 작성 후 접수 기간 내에 제출해주시기 바랍니다.")
    else:
        st.error(f"### 🚫 [최종 판정: 부적격 위험 {len(results)}건]")
        st.write("아래 항목에 대해 사전 조치가 필요합니다.")
        
        for i, res in enumerate(results):
            with st.container():
                st.markdown(f"**{i+1}. {res['항목']}**")
                st.info(f"💡 **조치 가이드:** {res['해결책']}")
                st.caption(f"원인: {res['원인']}")
                st.divider()
