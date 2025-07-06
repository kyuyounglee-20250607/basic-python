from pykrx import stock
from datetime import datetime
import difflib

def get_stock_info(kor_name):
    today = datetime.today().strftime("%Y%m%d")
    tickers = stock.get_market_ticker_list(today)
    
    name_dict = {}
    for ticker in tickers:
        name = stock.get_market_ticker_name(ticker)
        name_dict[name] = ticker

    # 입력 종목명 정확히 일치
    if kor_name not in name_dict:
        print(f"'{kor_name}' 종목을 정확히 찾을 수 없습니다. 유사한 종목을 출력합니다.\n")
    else:
        ticker = name_dict[kor_name]
        price = stock.get_market_ohlcv_by_date(today, today, ticker)
        price = price['종가'].iloc[0]
        print(f"📈 {kor_name} ({ticker}) 현재가: {price:,}원\n")

    # 유사 종목 추천
    all_names = list(name_dict.keys())
    similar = difflib.get_close_matches(kor_name, all_names, n=10, cutoff=0.3)
    
    if similar:
        print("🔍 유사 종목 추천:")
        for s in similar:
            print(f" - {s} ({name_dict[s]})")
    else:
        print("❌ 유사한 종목명을 찾을 수 없습니다.")

# 예시 실행
get_stock_info("삼성전자")