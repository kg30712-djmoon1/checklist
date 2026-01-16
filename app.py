import streamlit as st
from logic import check_and_guide # logic.py 파일이 같은 폴더에 있어야 합니다.

st.title("🔎 사전검토 자가진단 및 조치 가이드")
st.write("첨부파일 [별표 2] 기준에 따라 분석합니다.")

# 입력창 (사용자가 수치를 입력)
name = st.text_input("기관명", value="에이아이씨엔티(주)")
cap = st.number_input("자본총계 (원)", value=1000000)
db = st.number_input("부채총계 (원)", value=500000)
proj = st.number_input("연구책임자 수행 과제 수", value=1)

if st.button("진단 결과 보기"):
    # logic.py의 함수를 호출하여 분석
    guides = check_and_guide(cap, db, proj)
    
    if not guides:
        st.success("✅ 모든 기준을 충족합니다! 신청이 가능합니다.")
    else:
        for g in guides:
            # 에러가 있는 항목만 경고 메시지로 출력
            st.warning(f"⚠️ {g['항목']} 주의")
            st.write(f"**원인:** {g['원인']}")
            st.write(f"**조치 방법:** {g['해결책']}")
