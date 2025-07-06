import pandas as pd

try:
    # 엑셀 파일 읽기
    xl = pd.ExcelFile('매출_분석_대시보드.xlsx')
    print("시트 목록:", xl.sheet_names)
    
    # 각 시트 확인
    for sheet_name in xl.sheet_names:
        print(f"\n=== {sheet_name} 시트 ===")
        df = pd.read_excel('매출_분석_대시보드.xlsx', sheet_name=sheet_name)
        print(f"행 수: {len(df)}")
        print(f"열 수: {len(df.columns)}")
        print("컬럼명:", list(df.columns))
        print("첫 3행:")
        print(df.head(3))
        
except Exception as e:
    print(f"오류 발생: {e}") 