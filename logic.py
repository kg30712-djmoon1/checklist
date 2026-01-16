def check_comprehensive_score(
    # [1] 공고 적합성 & [2] 차별성/제재
    is_suitability, is_duplicated, is_restricted, is_tax_default,
    # [3] 재무 데이터
    cap_total, cap_stock, liab_total, curr_asset, curr_liab, 
    op_income, int_exp,
    # [3] 재무 이력
    prev_debt_500, prev_curr_50, loss_3yrs, audit_opinion,
    # [4] 3책 5공 상세 (New)
    cnt_pi_current, cnt_res_current, cnt_pi_applying, cnt_res_applying,
    # [5] 가점 항목 (New)
    score_loc, is_rnd_comp, is_high_tech, is_innovative, is_top100, is_ex_lab,
    # [6] 감점 항목 (New)
    is_cancel_sanction, is_giveup
):
    report = {
        "1_eligibility": {"status": "PASS", "msgs": []},
        "2_sanction": {"status": "PASS", "msgs": []},
        "3_financial": {"status": "PASS", "msgs": []},
        "4_3n5": {"status": "PASS", "msgs": []}, # 3책5공
        "5_score": {"bonus": 0, "penalty": 0, "final": 0}, # 가감점
        "summary": "적격"
    }

    # --- 1. 공고 적합성 ---
    if is_suitability == "부적합":
        report["1_eligibility"]["status"] = "FAIL"
        report["1_eligibility"]["msgs"].append("신청 자격 요건 미충족")

    # --- 2. 제재 및 차별성 ---
    if is_duplicated == "중복됨":
        report["2_sanction"]["status"] = "FAIL"
        report["2_sanction"]["msgs"].append("과제 중복성 발견")
    if is_restricted == "해당함":
        report["2_sanction"]["status"] = "FAIL"
        report["2_sanction"]["msgs"].append("참여제한 대상")
    if is_tax_default == "해당함":
        report["2_sanction"]["status"] = "FAIL"
        report["2_sanction"]["msgs"].append("채무불이행/체납 존재")

    # --- 3. 재무현황 (기존 로직 유지) ---
    debt_ratio = (liab_total / cap_total * 100) if cap_total > 0 else 9999
    curr_ratio = (curr_asset / curr_liab * 100) if curr_liab > 0 else 0
    icr = (op_income / int_exp) if int_exp > 0 else 9999
    
    fin_fail = False
    if cap_total <= 0:
        fin_fail = True
        report["3_financial"]["msgs"].append({"type": "RED", "text": "자본전액잠식"})
    if debt_ratio >= 500 and prev_debt_500:
        fin_fail = True
        report["3_financial"]["msgs"].append({"type": "RED", "text": "2년 연속 부채비율 500% 초과"})
    if curr_ratio <= 50 and prev_curr_50:
        fin_fail = True
        report["3_financial"]["msgs"].append({"type": "RED", "text": "2년 연속 유동비율 50% 이하"})
    if audit_opinion != "적정":
        fin_fail = True
        report["3_financial"]["msgs"].append({"type": "RED", "text": "감사의견 부적정"})
        
    if fin_fail:
        report["3_financial"]["status"] = "FAIL"
    else:
        # 사후관리 체크
        if debt_ratio >= 300: report["3_financial"]["msgs"].append({"type": "YELLOW", "text": "부채비율 300% 이상 (사후관리)"})
        if curr_ratio <= 100: report["3_financial"]["msgs"].append({"type": "YELLOW", "text": "유동비율 100% 이하 (사후관리)"})
        if icr < 1: report["3_financial"]["msgs"].append({"type": "YELLOW", "text": "이자보상비율 1 미만 (사후관리)"})
        if loss_3yrs: report["3_financial"]["msgs"].append({"type": "YELLOW", "text": "3년 연속 영업적자 (사후관리)"})
        if report["3_financial"]["msgs"]: report["3_financial"]["status"] = "WARN"

    # --- 4. 3책 5공 정밀 진단 (New) ---
    # 총 수행 과제 수 계산 (현재 수행중 + 신청중)
    total_pi = cnt_pi_current + cnt_pi_applying
    total_res = cnt_res_current + cnt_res_applying
    total_projects = total_pi + total_res # 본인이 참여하는 총 과제 수
    
    if total_pi > 3:
        report["4_3n5"]["status"] = "FAIL"
        report["4_3n5"]["msgs"].append(f"연구책임자 수행 과제 {total_pi}개 (3개 초과)")
    
    if total_projects > 5:
        report["4_3n5"]["status"] = "FAIL"
        report["4_3n5"]["msgs"].append(f"총 참여 과제 {total_projects}개 (5개 초과)")
        
    # --- 5. 가점 및 감점 계산 (New) ---
    bonus = 0
    # (1) 입지 요건 (최대 3점)
    bonus += score_loc 
    # (2) 기타 가점 (각 1점)
    if is_rnd_comp: bonus += 1
    if is_high_tech: bonus += 1
    if is_innovative: bonus += 1
    if is_top100: bonus += 1
    if is_ex_lab: bonus += 1
    
    # 가점 최대 5점 제한
    final_bonus = min(bonus, 5)
    
    penalty = 0
    if is_cancel_sanction: penalty += 1
    if is_giveup: penalty += 1
    
    report["5_score"]["bonus"] = final_bonus
    report["5_score"]["penalty"] = penalty
    report["5_score"]["final"] = final_bonus - penalty

    # 최종 판정
    if any(report[k]["status"] == "FAIL" for k in ["1_eligibility", "2_sanction", "3_financial", "4_3n5"]):
        report["summary"] = "부적격"
    elif report["3_financial"]["status"] == "WARN":
        report["summary"] = "사후관리"

    return report
