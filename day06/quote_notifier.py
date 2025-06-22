import requests
from plyer import notification
import schedule
import time

def get_quote():
    try:
        response = requests.get("https://korean-advice-open-api.vercel.app/api/advice")
        if response.status_code == 200:
            data = response.json()
            return f'"{data["message"]}"\n- {data["author"]}'
        else:
            return "명언을 가져오지 못했습니다."
    except Exception as e:
        return f"오류 발생: {e}"

def show_notification(message):
    notification.notify(
        title="오늘의 명언 😊",
        message=message,
        timeout=10
    )

def job():
    message = get_quote()
    show_notification(message)

# 매일 오전 9시 알림
schedule.every().day.at("09:00").do(job)

print("⏰ 알림 대기 중... (Ctrl+C로 종료)")
while True:
    schedule.run_pending()
    time.sleep(1)
