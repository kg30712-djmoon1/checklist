import streamlit as st
from logic import check_and_guide

# 페이지 레이아웃 설정
st.set_page_config(page_title="광주특구 사전검토 시스템", layout="wide")

st.title("🛡️ AI 글로벌 빅테크 육성사업 사전검토 자가진단")
st.caption("본 시스템은 [연구개발특구육성사업 운영관리지침] 별표 2 기준을 바탕으로 작동합니다.")

# 입력 섹션
with st.container():
    st.subheader("1. 기업 정보 및 재무 수치 입력")
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("기관명", value="에이아이씨엔티(주)")
        cap = st.number_input("자본총계 (원)", value=1000000)
    with c2:
        db = st.number_input("부채총계 (원)", value=1500000)
        curr_a = st.number_input("유동자산 (원)", value=2000000)
    with c3:
        curr_d = st.number_input("유동부채 (원)", value=1000000)
        proj = st.number_input("연구책임자 동시수행 과제 수", value=1)

# 진단 로직 실행
if st.button("📊 상세 진단 결과 리포트 생성", use_container_width=True):
    guides = check_and_guide(cap, db, proj) # 기존 logic.py 활용
    
    st.divider()
    
    # 결과 요약 대시보드
    col_a, col_b, col_c = st.columns(3)
    debt_ratio = (db/cap*100) if cap > 0 else 999
    col_a.metric("부채비율", f"{debt_ratio:.1f}%", delta="-500%" if debt_ratio > 500 else "정상", delta_color="inverse")
    col_b.metric("연구과제 수", f"{proj}건", delta="-3건 초과" if proj > 3 else "정상", delta_color="inverse")
    
    if not guides:
        st.balloons()
        st.success("### ✅ 진단 결과: 사업 신청 적격")
        st.write("귀 기관은 지침상 모든 사전지원제외 기준을 충족하지 않습니다. 정상적으로 사업 신청이 가능합니다.")
    else:
        st.error("### ⚠️ 진단 결과: 부적격 사유 발견")
        st.write("아래의 지침 위반 사항을 확인하시고, 공고문에 명시된 기한 내에 조치하시기 바랍니다.")
        
        for g in guides:
            with st.expander(f"📌 {g['항목']} 검토 결과 안내", expanded=True):
                st.markdown(f"**[현황 및 원인]**")
                st.write(g['원인'])
                st.markdown(f"**[지침 근거 및 사후 조치 가이드]**")
                st.info(g['해결책'])
                st.caption("※ 근거: 운영관리지침 별표 2 사전지원제외 대상여부 검토 세부기준") [cite: 46]
