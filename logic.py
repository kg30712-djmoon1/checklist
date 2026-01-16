def check_comprehensive(cap, db, proj, is_restricted, is_duplicated, is_default, is_suitability):
    # 재무 비율 계산
    debt_ratio = (db / cap * 100) if cap > 0 else 999
    results = []

    # --- [1] 비재무(자격) 요건 검토 ---
    if is_restricted == "해당함":
        results.append({
            "항목": "참여제한(제재조치)",
            "원인": "국가연구개발사업 참여제한 중인 기관/책임자 포함 [지침 제1호]",
            "해결책": "제재 기간이 종료되지 않았다면 지원 불가합니다."
        })

    if is_duplicated == "중복됨":
        results.append({
            "항목": "과제 중복성",
            "원인": "기존 과제와 동일/유사함 [지침 제3호]",
            "해결책": "차별성을 입증하거나 목표를 변경해야 합니다."
        })

    if is_default == "해당함":
        results.append({
            "항목": "채무불이행",
            "원인": "국세/지방세 체납 또는 채무불이행 등재 [지침 제5호]",
            "해결책": "체납 처분을 해소하거나 신용회복지원 여부를 확인하세요."
        })

    if is_suitability == "부적합":
        results.append({
            "항목": "공고 적합성",
            "원인": "공고 신청자격 요건 미충족 [지침 제2호]",
            "해결책": "공고문의 자격 요건을 다시 확인하십시오."
        })

    # --- [2] 재무 요건 검토 ---
    if cap <= 0:
        results.append({
            "항목": "자본전액잠식",
            "원인": "최근 결산 기준 자본총계 0 이하 [지침 제5호]",
            "해결책": "공동연구기관 제외 또는 사유 해소 증빙 필요"
        })

    if debt_ratio >= 500:
        results.append({
            "항목": "부채비율 500% 초과",
            "원인": f"부채비율 {debt_ratio:.1f}% 초과 [지침 제5호]",
            "해결책": "창업 5년 미만 등 예외 요건 확인 필요"
        })

    if proj > 3:
        results.append({
            "항목": "3책 5공 위반",
            "원인": "책임자 과제수 3개 초과 [지침 제6호]",
            "해결책": "책임자 변경 또는 참여율 조정 필요"
        })

    return results
