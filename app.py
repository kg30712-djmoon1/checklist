import streamlit as st
# ★ 중요: 아래 줄이 logic.py의 함수 이름과 똑같아야 합니다!
from logic import check_comprehensive 

st.set_page_config(page_title="광주특구 통합 사전검토", layout="wide")

st.title("🛡️ 딥테크 육성사업 통합 사전검토 시스템")
st.info("재무 정보뿐만 아니라 규정 위반(중복성, 제재 등) 여부까지 통합 진단합니다.")

# 탭 설정
tab1, tab2 = st.tabs(["📑 1. 자격 요건 자가진단", "📊 2. 재무 데이터 입력"])

with tab1:
    st.subheader("비재무(Qualitative) 필수 점검")
    col_a, col_b = st.columns(2)
    with col_a:
        is_restricted = st.radio("1. 국가연구개발사업 참여제한 여부", ("해당없음", "해당함"))
        is_default = st.radio("2. 채무불이행 및 체납 여부", ("해당없음", "해당함"))
    with col_b:
        is_duplicated = st.radio("3. 과제 중복성 여부", ("중복없음", "중복됨"))
        is_suitability = st.radio("4. 공고 자격 적합 여부", ("적합", "부적합"))

with tab2:
    st.subheader("재무(Quantitative) 데이터 입력")
    c1, c2, c3 = st.columns(3)
    cap = c1.number_input("자본총계 (원)", value=100000000)
    db = c2.number_input("부채총계 (원)", value=150000000)
    proj = c3.number_input("책임자 과제 수", value=1)

# 진단 실행
if st.button("🚀 통합 진단 결과 확인", use_container_width=True):
    # logic.py의 새로운 함수(check_comprehensive)를 사용합니다
    results = check_comprehensive(cap, db, proj, is_restricted, is_duplicated, is_default, is_suitability)
    
    st.divider()
    
    if not results:
        st.success("## ✅ 진단 결과: [적격]")
        st.markdown("재무 건전성 및 제반 자격 요건을 모두 충족합니다.")
    else:
        st.error(f"## 🚫 진단 결과: [부적격 요인 {len(results)}건 발견]")
        for res in results:
            with st.expander(f"⚠️ {res['항목']} 문제 발견", expanded=True):
                st.write(f"**원인:** {res['원인']}")
                st.info(f"**조치 가이드:** {res['해결책']}")
