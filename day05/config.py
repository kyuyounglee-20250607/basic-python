import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    # Alpha Vantage API 설정
    ALPHA_VANTAGE_API_KEY = "3JQCLXOAZI6WRNV2"
    
    # IEX Cloud API 설정
    IEX_CLOUD_API_KEY = "your_api_key_here"
    
    # 기본 데이터 소스 (alpha_vantage, iex_cloud, yahoo_finance)
    DEFAULT_DATA_SOURCE = os.getenv('DEFAULT_DATA_SOURCE', 'alpha_vantage')
    
    # API 호출 제한 (무료 티어 고려)
    MAX_REQUESTS_PER_MINUTE = 5
    
    @classmethod
    def is_api_available(cls, source):
        """API 키가 설정되어 있는지 확인"""
        if source == 'alpha_vantage':
            return bool(cls.ALPHA_VANTAGE_API_KEY)
        elif source == 'iex_cloud':
            return bool(cls.IEX_CLOUD_API_KEY)
        elif source == 'yahoo_finance':
            return True  # API 키 불필요
        return False 