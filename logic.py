def check_final_diagnosis(
    # [1] 공고 적합성 & [2] 차별성/제재 입력값
    is_suitability, is_duplicated, is_restricted, is_tax_default,
    # [3] 재무 데이터
    cap_total, cap_stock, liab_total, curr_asset, curr_liab, 
    op_income, int_exp,
    # [3] 재무 이력 데이터 (엑셀 기준)
    prev_debt_500, prev_curr_50, loss_3yrs, audit_opinion
):
    # 결과 저장소 (4개 카테고리로 분류)
    report = {
        "1_eligibility": {"status": "PASS", "msgs": []}, # 공고 적합성
        "2_sanction": {"status": "PASS", "msgs": []},    # 제재 및 차별성
        "3_financial": {"status": "PASS", "msgs": []},   # 재무 현황
        "summary": "적격"
    }

    # --- 1. 공고 적합성 검토 (지침 제2호) ---
    if is_suitability == "부적합":
        report["1_eligibility"]["status"] = "FAIL"
        report["1_eligibility"]["msgs"].append({
            "type": "RED", "text": "신청 자격 요건(업력, 소재지 등) 미충족 [지침 제2호]"
        })

    # --- 2. 차별성 및 제재조치 검토 (지침 제1,3,5호) ---
    if is_duplicated == "중복됨":
        report["2_sanction"]["status"] = "FAIL"
        report["2_sanction"]["msgs"].append({
            "type": "RED", "text": "기지원 과제와 중복성 발견 (차별성 부족) [지침 제3호]"
        })
    
    if is_restricted == "해당함":
        report["2_sanction"]["status"] = "FAIL"
        report["2_sanction"]["msgs"].append({
            "type": "RED", "text": "국가연구개발사업 참여제한 기관/책임자 포함 [지침 제1호]"
        })
        
    if is_tax_default == "해당함": # 엑셀 '채무불이행여부' 반영
        report["2_sanction"]["status"] = "FAIL"
        report["2_sanction"]["msgs"].append({
            "type": "RED", "text": "국세/지방세 체납 또는 채무불이행 등재 [지침 제5호]"
        })

    # --- 3. 재무현황 정밀 검토 (엑셀 상세 기준) ---
    # 비율 계산
    debt_ratio = (liab_total / cap_total * 100) if cap_total > 0 else 9999
    curr_ratio = (curr_asset / curr_liab * 100) if curr_liab > 0 else 0
    icr = (op_income / int_exp) if int_exp > 0 else 9999

    fin_msgs = []
    fin_status = "PASS"

    # [Red] 사전지원제외 대상
    if cap_total <= 0:
        fin_status = "FAIL"
        fin_msgs.append({"type": "RED", "text": "완전 자본잠식 (자본총계 0 이하) [지침 제5호]"})
    
    if debt_ratio >= 500 and prev_debt_500: # 2년 연속 체크
        fin_status = "FAIL"
        fin_msgs.append({"type": "RED", "text": f"2년 연속 부채비율 500% 이상 (올해 {debt_ratio:.1f}%)"})
        
    if curr_ratio <= 50 and prev_curr_50: # 2년 연속 체크
        fin_status = "FAIL"
        fin_msgs.append({"type": "RED", "text": f"2년 연속 유동비율 50% 이하 (올해 {curr_ratio:.1f}%)"})
        
    if audit_opinion != "적정":
        fin_status = "FAIL"
        fin_msgs.append({"type": "RED", "text": f"외부감사 의견 부적정 ({audit_opinion})"})

    # [Yellow] 사후관리 대상 (지원 가능하나 경고)
    if fin_status != "FAIL": # 이미 탈락이 아니면 사후관리 체크
        if debt_ratio >= 300:
            fin_status = "WARN"
            fin_msgs.append({"type": "YELLOW", "text": f"부채비율 300% 이상 ({debt_ratio:.1f}%)"})
        if curr_ratio <= 100:
            fin_status = "WARN"
            fin_msgs.append({"type": "YELLOW", "text": f"유동비율 100% 이하 ({curr_ratio:.1f}%)"})
        if cap_total < cap_stock and cap_total > 0:
            fin_status = "WARN"
            fin_msgs.append({"type": "YELLOW", "text": "부분 자본잠식 상태"})
        if icr < 1:
            fin_status = "WARN"
            fin_msgs.append({"type": "YELLOW", "text": f"이자보상비율 1 미만 ({icr:.2f}배)"})
        if loss_3yrs:
            fin_status = "WARN"
            fin_msgs.append({"type": "YELLOW", "text": "최근 3년 연속 영업이익 적자"})

    report["3_financial"]["status"] = fin_status
    report["3_financial"]["msgs"] = fin_msgs

    # 최종 요약 상태 결정
    if any(report[k]["status"] == "FAIL" for k in report if k != "summary"):
        report["summary"] = "부적격"
    elif any(report[k]["status"] == "WARN" for k in report if k != "summary"):
        report["summary"] = "사후관리"
    
    return report
