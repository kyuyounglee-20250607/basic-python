import requests
from plyer import notification
import schedule
import time
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quote_notification.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class QuoteNotification:
    """명언 알림 클래스"""
    
    def __init__(self, config_file: str = "quote_config.json"):
        """
        QuoteNotification 초기화
        
        Args:
            config_file: 설정 파일 경로
        """
        self.config = self.load_config(config_file)
        self.quote_cache = []
        self.max_cache_size = 10
        
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """설정 파일을 로드합니다."""
        default_config = {
            "notification_time": "09:00",
            "notification_timeout": 10,
            "notification_title": "오늘의 명언 😊",
            "api_url": "https://api.quotable.io/random",
            "max_retries": 3,
            "retry_delay": 5,
            "enable_logging": True
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    logger.info("설정 파일을 성공적으로 로드했습니다.")
            else:
                # 기본 설정 파일 생성
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, ensure_ascii=False, indent=2)
                logger.info("기본 설정 파일을 생성했습니다.")
                
        except Exception as e:
            logger.error(f"설정 파일 로드 오류: {e}")
            
        return default_config
    
    def get_quote(self) -> Optional[str]:
        """
        API에서 명언을 가져옵니다.
        
        Returns:
            포맷팅된 명언 문자열 또는 None (오류 시)
        """
        for attempt in range(self.config["max_retries"]):
            try:
                logger.info(f"명언 요청 시도 {attempt + 1}/{self.config['max_retries']}")
                
                response = requests.get(
                    self.config["api_url"], 
                    timeout=10,
                    headers={'User-Agent': 'QuoteNotification/1.0'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 캐시에 추가
                    quote_text = f'"{data["content"]}"\n- {data["author"]}'
                    self.add_to_cache(quote_text)
                    
                    logger.info(f"명언을 성공적으로 가져왔습니다: {data['author']}")
                    return quote_text
                    
                else:
                    logger.warning(f"API 응답 오류: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                logger.error(f"요청 시간 초과 (시도 {attempt + 1})")
            except requests.exceptions.RequestException as e:
                logger.error(f"네트워크 오류 (시도 {attempt + 1}): {e}")
            except json.JSONDecodeError as e:
                logger.error(f"JSON 파싱 오류 (시도 {attempt + 1}): {e}")
            except Exception as e:
                logger.error(f"예상치 못한 오류 (시도 {attempt + 1}): {e}")
            
            # 재시도 전 대기
            if attempt < self.config["max_retries"] - 1:
                logger.info(f"{self.config['retry_delay']}초 후 재시도합니다...")
                time.sleep(self.config["retry_delay"])
        
        # 모든 시도 실패 시 캐시에서 랜덤 선택
        if self.quote_cache:
            logger.warning("API 요청 실패, 캐시된 명언을 사용합니다.")
            import random
            return random.choice(self.quote_cache)
        
        return "오늘의 명언을 가져오지 못했습니다. 😔"
    
    def add_to_cache(self, quote: str):
        """명언을 캐시에 추가합니다."""
        if quote not in self.quote_cache:
            self.quote_cache.append(quote)
            if len(self.quote_cache) > self.max_cache_size:
                self.quote_cache.pop(0)  # 가장 오래된 명언 제거
    
    def show_notification(self, message: str):
        """
        윈도우 알림을 표시합니다.
        
        Args:
            message: 표시할 메시지
        """
        try:
            notification.notify(
                title=self.config["notification_title"],
                message=message,
                timeout=self.config["notification_timeout"]
            )
            logger.info("알림을 성공적으로 표시했습니다.")
            
        except Exception as e:
            logger.error(f"알림 표시 오류: {e}")
            # 알림 실패 시 콘솔에 출력
            print(f"\n{'='*50}")
            print(f"📝 {self.config['notification_title']}")
            print(f"{'='*50}")
            print(message)
            print(f"{'='*50}\n")
    
    def job(self):
        """스케줄된 작업을 실행합니다."""
        logger.info("명언 알림 작업을 시작합니다.")
        
        message = self.get_quote()
        if message:
            self.show_notification(message)
        else:
            logger.error("명언을 가져오지 못했습니다.")
    
    def start_scheduler(self):
        """스케줄러를 시작합니다."""
        try:
            # 스케줄 설정
            schedule.every().day.at(self.config["notification_time"]).do(self.job)
            
            logger.info(f"스케줄러가 시작되었습니다. 알림 시간: {self.config['notification_time']}")
            print(f"⏰ 알림 대기 중... (매일 {self.config['notification_time']})")
            print("📝 Ctrl+C로 종료")
            print("🔧 설정 변경 시 quote_config.json 파일을 수정하세요")
            
            # 즉시 한 번 실행 (테스트용)
            print("\n🧪 테스트 알림을 보내시겠습니까? (y/n): ", end="")
            if input().lower() == 'y':
                self.job()
            
            # 스케줄러 루프
            while True:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("사용자에 의해 프로그램이 종료되었습니다.")
            print("\n👋 프로그램을 종료합니다.")
        except Exception as e:
            logger.error(f"스케줄러 오류: {e}")
            print(f"❌ 오류가 발생했습니다: {e}")

def main():
    """메인 함수"""
    try:
        quote_notifier = QuoteNotification()
        quote_notifier.start_scheduler()
        
    except Exception as e:
        logger.error(f"프로그램 실행 오류: {e}")
        print(f"❌ 프로그램 실행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main() 