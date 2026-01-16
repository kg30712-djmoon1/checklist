def check_financial_detail(
    cap_total, cap_stock,  # 자본총계, 자본금
    liab_total,            # 부채총계
    curr_asset, curr_liab, # 유동자산, 유동부채
    op_income, int_exp,    # 영업이익, 이자비용
    prev_debt_500, prev_curr_50, # 작년 부채500%이상, 작년 유동50%이하 여부
    loss_3yrs,             # 3년 연속 적자 여부
    audit_opinion,         # 감사의견
    tax_default            # 체납 여부
):
    results = {"red": [], "yellow": []} # red: 사전제외, yellow: 사후관리
    
    # 1. 비율 계산
    debt_ratio = (liab_total / cap_total * 100) if cap_total > 0 else 9999
    curr_ratio = (curr_asset / curr_liab * 100) if curr_liab > 0 else 0
    # 이자보상비율 = 영업이익 / 이자비용
    int_cov_ratio = (op_income / int_exp) if int_exp > 0 else 9999
    
    # 2. [Red] 사전지원제외 요건 정밀 검토
    
    # (1) 자본전액잠식
    if cap_total <= 0:
        results["red"].append({
            "항목": "자본전액잠식",
            "내용": "24년말 기준 자본총계가 0원 이하입니다.",
            "조치": "공동기관 제외 또는 증자 후 재무제표 확정 필요"
        })
        
    # (2) 2년 연속 부채비율 500% 이상 (엑셀 헤더 반영)
    if debt_ratio >= 500 and prev_debt_500:
        results["red"].append({
            "항목": "2년 연속 부채비율 500% 이상",
            "내용": f"23년에 이어 24년({debt_ratio:.1f}%)도 500%를 초과했습니다.",
            "조치": "창업 5년 미만 기업 등 예외 조항 확인 필요"
        })
        
    # (3) 2년 연속 유동비율 50% 이하
    if curr_ratio <= 50 and prev_curr_50:
        results["red"].append({
            "항목": "2년 연속 유동비율 50% 이하",
            "내용": f"23년에 이어 24년({curr_ratio:.1f}%)도 50% 이하입니다.",
            "조치": "재무구조 개선 필요 (지원 제외 대상)"
        })
        
    # (4) 채무불이행/체납
    if tax_default:
        results["red"].append({
            "항목": "국세/지방세 체납 및 채무불이행",
            "내용": "체납처분 또는 규제중인 채무불이행 내역 존재",
            "조치": "접수 마감 전까지 해소 필수"
        })

    # (5) 외부감사 의견
    if audit_opinion != "적정(해당없음)":
        results["red"].append({
            "항목": "외부감사 의견 부적정",
            "내용": "감사의견이 한정, 부적정, 의견거절임",
            "조치": "지원 제외 대상"
        })

    # 3. [Yellow] 사후관리 대상 요건 (엑셀 '사후관리여부' 반영)
    
    # (1) 부채비율 300% 이상
    if debt_ratio >= 300:
        results["yellow"].append(f"부채비율({debt_ratio:.1f}%) 300% 이상")
        
    # (2) 유동비율 100% 이하
    if curr_ratio <= 100:
        results["yellow"].append(f"유동비율({curr_ratio:.1f}%) 100% 이하")
        
    # (3) 부분자본잠식 (자본총계 < 자본금)
    if cap_total < cap_stock and cap_total > 0:
        ratio = (cap_stock - cap_total) / cap_stock * 100
        results["yellow"].append(f"부분자본잠식 상태 (잠식률 {ratio:.1f}%)")
        
    # (4) 이자보상비율 1 미만
    if int_cov_ratio < 1:
        results["yellow"].append(f"이자보상비율 1 미만 ({int_cov_ratio:.2f}배)")
        
    # (5) 3년 연속 영업적자
    if loss_3yrs:
        results["yellow"].append("최근 3년(22~24) 연속 영업이익 적자")

    return results, debt_ratio, curr_ratio, int_cov_ratio
