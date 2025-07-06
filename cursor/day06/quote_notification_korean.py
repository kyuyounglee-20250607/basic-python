import requests
from plyer import notification
import schedule
import time
import json
import logging
from typing import Optional
from datetime import datetime

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

# 설정
CONFIG = {
    "notification_time": "09:00",
    "notification_timeout": 10,
    "notification_title": "오늘의 명언 😊",
    "api_url": "https://korean-advice-open-api.vercel.app/api/advice",
    "max_retries": 3,
    "retry_delay": 5,
    "enable_test": True
}

# 명언 캐시
quote_cache = []
MAX_CACHE_SIZE = 10

def load_config():
    """설정 파일을 로드합니다."""
    try:
        with open('quote_config.json', 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            CONFIG.update(user_config)
            logger.info("설정 파일을 성공적으로 로드했습니다.")
    except FileNotFoundError:
        # 기본 설정 파일 생성
        with open('quote_config.json', 'w', encoding='utf-8') as f:
            json.dump(CONFIG, f, ensure_ascii=False, indent=2)
        logger.info("기본 설정 파일을 생성했습니다.")
    except Exception as e:
        logger.error(f"설정 파일 로드 오류: {e}")

def get_quote() -> str:
    """
    한국어 명언 API에서 명언을 가져옵니다.
    
    Returns:
        포맷팅된 명언 문자열
    """
    for attempt in range(CONFIG["max_retries"]):
        try:
            logger.info(f"명언 요청 시도 {attempt + 1}/{CONFIG['max_retries']}")
            
            response = requests.get(
                CONFIG["api_url"], 
                timeout=10,
                headers={
                    'User-Agent': 'QuoteNotification/1.0',
                    'Accept': 'application/json'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # API 응답 구조 확인 및 처리
                if "content" in data and "author" in data:
                    quote_text = f'"{data["content"]}"\n- {data["author"]}'
                elif "advice" in data:  # 다른 응답 구조 대응
                    quote_text = f'"{data["advice"]}"\n- 한국의 지혜'
                else:
                    # 예상치 못한 응답 구조 처리
                    quote_text = f'"{str(data)}"\n- 알 수 없는 출처'
                
                # 캐시에 추가
                add_to_cache(quote_text)
                
                logger.info(f"명언을 성공적으로 가져왔습니다: {data.get('author', '알 수 없음')}")
                return quote_text
                
            else:
                logger.warning(f"API 응답 오류: {response.status_code}")
                if response.status_code == 404:
                    return "API 엔드포인트를 찾을 수 없습니다."
                elif response.status_code == 500:
                    return "서버 오류가 발생했습니다."
                else:
                    return f"API 오류: {response.status_code}"
                
        except requests.exceptions.Timeout:
            logger.error(f"요청 시간 초과 (시도 {attempt + 1})")
        except requests.exceptions.ConnectionError:
            logger.error(f"연결 오류 (시도 {attempt + 1})")
        except requests.exceptions.RequestException as e:
            logger.error(f"네트워크 오류 (시도 {attempt + 1}): {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 오류 (시도 {attempt + 1}): {e}")
        except Exception as e:
            logger.error(f"예상치 못한 오류 (시도 {attempt + 1}): {e}")
        
        # 재시도 전 대기
        if attempt < CONFIG["max_retries"] - 1:
            logger.info(f"{CONFIG['retry_delay']}초 후 재시도합니다...")
            time.sleep(CONFIG["retry_delay"])
    
    # 모든 시도 실패 시 캐시에서 랜덤 선택
    if quote_cache:
        logger.warning("API 요청 실패, 캐시된 명언을 사용합니다.")
        import random
        return random.choice(quote_cache)
    
    # 캐시도 없으면 기본 명언 반환
    default_quotes = [
        '"오늘 하루도 힘내세요!"\n- 응원하는 마음',
        '"작은 진전도 진전입니다."\n- 격려의 말',
        '"당신은 충분히 잘하고 있습니다."\n- 따뜻한 위로',
        '"내일은 더 좋은 날이 될 거예요."\n- 희망의 메시지',
        '"한 걸음씩 천천히 나아가세요."\n- 인생의 지혜'
    ]
    import random
    return random.choice(default_quotes)

def add_to_cache(quote: str):
    """명언을 캐시에 추가합니다."""
    if quote not in quote_cache:
        quote_cache.append(quote)
        if len(quote_cache) > MAX_CACHE_SIZE:
            quote_cache.pop(0)  # 가장 오래된 명언 제거

def show_notification(message: str):
    """
    윈도우 알림을 표시합니다.
    
    Args:
        message: 표시할 메시지
    """
    try:
        notification.notify(
            title=CONFIG["notification_title"],
            message=message,
            timeout=CONFIG["notification_timeout"]
        )
        logger.info("알림을 성공적으로 표시했습니다.")
        
    except Exception as e:
        logger.error(f"알림 표시 오류: {e}")
        # 알림 실패 시 콘솔에 출력
        print(f"\n{'='*50}")
        print(f"📝 {CONFIG['notification_title']}")
        print(f"{'='*50}")
        print(message)
        print(f"{'='*50}\n")

def job():
    """스케줄된 작업을 실행합니다."""
    logger.info("명언 알림 작업을 시작합니다.")
    
    message = get_quote()
    show_notification(message)

def test_notification():
    """테스트 알림을 실행합니다."""
    print("🧪 테스트 알림을 실행합니다...")
    job()
    print("✅ 테스트 알림이 완료되었습니다.")

def main():
    """메인 함수"""
    try:
        # 설정 로드
        load_config()
        
        # 스케줄 설정
        schedule.every().day.at(CONFIG["notification_time"]).do(job)
        
        logger.info(f"스케줄러가 시작되었습니다. 알림 시간: {CONFIG['notification_time']}")
        print(f"⏰ 알림 대기 중... (매일 {CONFIG['notification_time']})")
        print("📝 Ctrl+C로 종료")
        print("🔧 설정 변경 시 quote_config.json 파일을 수정하세요")
        print(f"🌐 API: {CONFIG['api_url']}")
        
        # 즉시 한 번 실행 (테스트용)
        if CONFIG.get("enable_test", True):
            print("\n🧪 테스트 알림을 보내시겠습니까? (y/n): ", end="")
            if input().lower() == 'y':
                test_notification()
        
        # 스케줄러 루프
        print("\n⏰ 알림 대기 중... (Ctrl+C로 종료)")
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("사용자에 의해 프로그램이 종료되었습니다.")
        print("\n👋 프로그램을 종료합니다.")
    except Exception as e:
        logger.error(f"프로그램 실행 오류: {e}")
        print(f"❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main() 