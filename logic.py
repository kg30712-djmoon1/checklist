def check_and_guide(cap, db, proj):
    # 부채비율 계산 [cite: 64]
    debt_ratio = (db / cap * 100) if cap > 0 else 9999
    results = []

    # 1. 자본잠식 검토 (지침 제5호 6번) [cite: 67]
    if cap <= 0:
        results.append({
            "항목": "자본 건전성",
            "원인": "최근 결산 기준 '자본전액잠식' 상태입니다.",
            "해결책": "문제가 되는 기관을 제외하고 신청하거나 사유 해소 증빙이 필요합니다. [cite: 79]"
        })

    # 2. 부채비율 검토 (지침 제5호 5번) [cite: 64]
    if debt_ratio >= 500:
        results.append({
            "항목": "부채 비율",
            "원인": f"부채비율이 {debt_ratio:.1f}%로 기준치(500%)를 초과했습니다.",
            "해결책": "업력 5년 미만 여부 등 예외 요건을 확인하시기 바랍니다. [cite: 64]"
        })

    # 3. 3책 5공 검토 (지침 제6호) [cite: 74]
    if proj > 3:
        results.append({
            "항목": "연구책임자 과제수",
            "원인": "동시수행 과제수가 3개를 초과합니다.",
            "해결책": "연구책임자를 변경하거나 종료 예정 과제를 확인하세요. [cite: 74]"
        })
    return results
