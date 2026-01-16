import streamlit as st
from logic import check_and_guide

# 1. 페이지 설정 (전문적인 느낌을 위해 레이아웃 확장)
st.set_page_config(page_title="광주특구 사전검토 자가진단", layout="wide")

# 헤더 부분
st.title("🛡️ AI 글로벌 빅테크 육성사업 사전검토 자가진단")
st.info("💡 본 시스템은 [연구개발특구육성사업 운영관리지침 별표 2]를 기반으로 기업의 신청 적격성을 분석합니다.")

# 2. 입력 섹션 (사이드바에 배치하여 메인 화면을 깔끔하게 유지)
with st.sidebar:
    st.header("📝 기업 데이터 입력")
    name = st.text_input("기관명", value="에이아이씨엔티(주)")
    st.divider()
    
    st.subheader("📊 재무 데이터")
    cap = st.number_input("자본총계 (원)", value=1000000, help="최근 회계연도 말 결산 재무제표 기준")
    db = st.number_input("부채총계 (원)", value=1500000)
    curr_a = st.number_input("유동자산 (원)", value=2000000)
    curr_d = st.number_input("유동부채 (원)", value=1000000)
    
    st.subheader("👥 인력 현황")
    proj = st.number_input("연구책임자 동시수행 과제 수", value=1, help="3책 5공 기준 확인")

# 3. 메인 분석 화면
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 항목별 진단 결과")
    
    # 버튼 클릭 시 진단 수행
    if st.button("실시간 검토 결과 리포트 생성", use_container_width=True):
        guides = check_and_guide(cap, db, proj)
        
        # 재무 비율 계산
        debt_ratio = (db / cap * 100) if cap > 0 else 999
        current_ratio = (curr_a / curr_d * 100) if curr_d > 0 else 0
        
        # 결과 요약 대시보드 (Metric)
        m1, m2, m3 = st.columns(3)
        m1.metric("부채비율", f"{debt_ratio:.1f}%", delta="위험" if debt_ratio >= 500 else "정상", delta_color="inverse")
        m2.metric("유동비율", f"{current_ratio:.1f}%", delta="위험" if current_ratio <= 50 else "정상")
        m3.metric("과제 수행", f"{proj}건", delta="초과" if proj > 3 else "정상", delta_color="inverse")
        
        st.divider()
        
        if not guides:
            st.balloons()
            st.success("### ✅ 진단 결과: 사업 신청 적격")
            st.markdown("""
            위 기관은 운영관리지침 [별표 2]에 따른 사전지원제외 대상에 해당하지 않습니다. 
            **안심하고 사업을 신청하셔도 좋습니다.**
            """)
        else:
            st.error("### ⚠️ 진단 결과: 부적격 사유 및 조치 필요")
            for g in guides:
                with st.expander(f"📌 {g['항목']} 검토 결과", expanded=True):
                    st.markdown(f"**[현황 및 원인]**\n\n{g['원인']}")
                    st.info(f"**[사후 조치 가이드]\n\n** {g['해결책']}")
                    st.caption("※ 근거: 운영관리지침 별표 2 사전지원제외 대상여부 검토 세부기준")

with col2:
    st.subheader("📋 지침 요약 안내")
    st.markdown("""
    **핵심 검토 항목 안내:**
    1. **자본전액잠식**: 최근 결산 기준 자본총계가 0 이하인 경우 (제외)
    2. **부채비율**: 500% 이상인 경우 (제외)
    3. **유동비율**: 50% 이하인 경우 (제외)
    4. **3책 5공**: 연구책임자 3개 초과 수행 시 (제외)
    
    *※ 단, 업력 5년 미만 기업 등 일부 예외 조항이 존재하므로 상세 지침을 반드시 확인하시기 바랍니다.*
    """)
