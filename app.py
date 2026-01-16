import streamlit as st
from logic import check_and_guide # 아까 만든 logic.py 연결

st.title("🔎 사전검토 자가진단 시스템")
st.write("첨부파일 [별표 2] 기준에 따라 분석합니다.") [cite: 64]

# 입력창
name = st.text_input("기관명", value="에이아이씨엔티(주)") [cite: 37]
cap = st.number_input("자본총계 (원)", value=1000000)
db = st.number_input("부채총계 (원)", value=500000)
proj = st.number_input("연구책임자 수행 과제 수", value=1) [cite: 74]

if st.button("진단 결과 보기"):
    guides = check_and_guide(cap, db, proj)
    if not guides:
        st.success("✅ 모든 기준을 충족합니다!")
    else:
        for g in guides:
            st.warning(f"⚠️ {g['항목']} 주의")
            st.write(f"**원인:** {g['원인']}")
            st.write(f"**해결방안:** {g['해결책']}")
