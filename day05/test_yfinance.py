import yfinance as yf
import pandas as pd

def test_yfinance():
    print("=== yfinance 테스트 시작 ===")
    
    # 테스트할 종목들
    test_symbols = [
        '005930.KS',  # 삼성전자
        '000660.KS',  # SK하이닉스
        'AAPL',       # 애플 (미국 주식 - 비교용)
        'MSFT',       # 마이크로소프트 (미국 주식 - 비교용)
        '005930',     # 삼성전자 (KS 없이)
        '005930.KQ',  # 삼성전자 (KQ로)
        '005930.KR'   # 삼성전자 (KR로)
    ]
    
    for symbol in test_symbols:
        print(f"\n--- 테스트: {symbol} ---")
        try:
            stock = yf.Ticker(symbol)
            
            # 기본 정보 가져오기
            info = stock.info
            print(f"종목명: {info.get('longName', 'N/A')}")
            print(f"현재가: {info.get('currentPrice', 'N/A')}")
            print(f"시가총액: {info.get('marketCap', 'N/A')}")
            
            # 히스토리 데이터 가져오기
            hist = stock.history(period='5d')
            if not hist.empty:
                print(f"히스토리 데이터: {len(hist)}개 행")
                print(f"최근 종가: {hist['Close'].iloc[-1]}")
                print(f"거래량: {hist['Volume'].iloc[-1]}")
            else:
                print("히스토리 데이터 없음")
                
        except Exception as e:
            print(f"오류: {e}")
    
    print("\n=== 테스트 완료 ===")

if __name__ == "__main__":
    test_yfinance() 