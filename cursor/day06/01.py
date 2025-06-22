from pykrx import stock
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

# 상수 정의
MARKET_CLOSE_HOUR = 15
WEEKDAYS = [0, 1, 2, 3, 4]  # 월~금
WEEKEND = [5, 6]  # 토, 일

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 종목 코드 캐시
_stock_code_cache: Dict[str, str] = {}

def get_target_stock_date(today: datetime) -> datetime:
    """
    주어진 날짜를 기준으로 주식 데이터를 조회할 대상 날짜를 계산합니다.
    
    Args:
        today: 기준 날짜
        
    Returns:
        조회할 대상 날짜
        
    Raises:
        ValueError: 날짜 판단이 불가능한 경우
    """
    weekday = today.weekday()
    current_hour = today.hour

    if weekday == 0 and current_hour < MARKET_CLOSE_HOUR:  # 월요일 + 마감 전
        return today - timedelta(days=3)
    elif weekday in [1, 2, 3, 4] and current_hour < MARKET_CLOSE_HOUR:  # 화~금 + 마감 전
        return today - timedelta(days=1)
    elif weekday in WEEKDAYS and current_hour >= MARKET_CLOSE_HOUR:  # 월~금 + 마감 후
        return today
    elif weekday == 5:  # 토요일
        return today - timedelta(days=1)
    elif weekday == 6:  # 일요일
        return today - timedelta(days=2)
    else:
        raise ValueError("날짜 판단 오류")

def get_stock_code_by_name(name: str) -> str:
    """
    종목명으로 종목 코드를 조회합니다. 캐시를 사용하여 성능을 개선합니다.
    
    Args:
        name: 종목명
        
    Returns:
        종목 코드
        
    Raises:
        ValueError: 종목명을 찾을 수 없는 경우
    """
    # 캐시에서 먼저 확인
    if name in _stock_code_cache:
        return _stock_code_cache[name]
    
    try:
        tickers = stock.get_market_ticker_list(market="ALL")
        for ticker in tickers:
            ticker_name = stock.get_market_ticker_name(ticker)
            if ticker_name == name:
                # 캐시에 저장
                _stock_code_cache[name] = ticker
                return ticker
        raise ValueError(f"종목명 '{name}'을 찾을 수 없습니다.")
    except Exception as e:
        logger.error(f"종목 코드 조회 중 오류 발생: {e}")
        raise

def format_stock_data(row: Any, stock_name: str, target_str: str) -> str:
    """
    주식 데이터를 포맷팅하여 문자열로 반환합니다.
    
    Args:
        row: 주식 데이터 행
        stock_name: 종목명
        target_str: 대상 날짜 문자열
        
    Returns:
        포맷팅된 주식 정보 문자열
    """
    try:
        return (
            f"[{stock_name}] {target_str} 기준\n"
            f"종가: {row['종가']:,}원\n"
            f"전일대비: {row['등락률']:.2f}%\n"
            f"거래량: {row['거래량']:,}주\n"
            f"시가: {row['시가']:,}원\n"
            f"고가: {row['고가']:,}원\n"
            f"저가: {row['저가']:,}원"
        )
    except KeyError as e:
        logger.error(f"주식 데이터 포맷팅 중 누락된 컬럼: {e}")
        return f"데이터 포맷팅 오류: {e}"

def get_korean_stock_info(stock_name: str) -> Optional[str]:
    """
    한국 주식 정보를 조회합니다.
    
    Args:
        stock_name: 조회할 종목명
        
    Returns:
        포맷팅된 주식 정보 문자열 또는 None (오류 시)
    """
    try:
        # 종목 코드 조회
        code = get_stock_code_by_name(stock_name)
        
        # 대상 날짜 계산
        today = datetime.today()
        target_date = get_target_stock_date(today)
        target_str = target_date.strftime("%Y%m%d")
        
        # 주식 데이터 조회
        df = stock.get_market_ohlcv_by_date(
            fromdate=target_str, 
            todate=target_str, 
            ticker=code
        )
        
        if df.empty:
            logger.warning(f"해당 날짜({target_str})에 데이터가 없습니다.")
            return None

        # 데이터 포맷팅 및 반환
        row = df.iloc[0]
        result = format_stock_data(row, stock_name, target_str)
        print(result)
        return result
        
    except ValueError as e:
        logger.error(f"입력 오류: {e}")
        print(f"오류: {e}")
        return None
    except Exception as e:
        logger.error(f"주식 정보 조회 중 예상치 못한 오류: {e}")
        print(f"오류: {e}")
        return None

def clear_stock_cache() -> None:
    """종목 코드 캐시를 초기화합니다."""
    _stock_code_cache.clear()
    logger.info("종목 코드 캐시가 초기화되었습니다.")

# 사용 예시
if __name__ == "__main__":
    # 삼성전자 주식 정보 조회
    result = get_korean_stock_info("삼성전자")
    
    # 캐시 확인 (두 번째 호출은 캐시에서 조회됨)
    if result:
        print("\n" + "="*50)
        get_korean_stock_info("삼성전자")
