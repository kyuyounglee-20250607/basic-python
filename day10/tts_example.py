#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS 프로그램 사용 예시
간단한 텍스트를 음성으로 변환하는 예시입니다.
"""

def simple_google_tts_example():
    """Google TTS 간단 사용 예시"""
    try:
        from gtts import gTTS
        from playsound import playsound
        import time
        
        # 텍스트 정의
        text = "안녕하세요! 이것은 Google TTS 예시입니다."
        
        # TTS 객체 생성
        tts = gTTS(text=text, lang='ko', slow=False)
        
        # MP3 파일로 저장
        filename = "hello_google.mp3"
        tts.save(filename)
        print(f"✅ 음성이 '{filename}' 파일로 저장되었습니다.")
        
        # 음성 재생
        print("🔊 음성을 재생합니다...")
        playsound(filename, block=True)
        # 재생 완료 후 잠시 대기
        time.sleep(0.5)
        
    except ImportError:
        print("❌ 필요한 라이브러리가 설치되지 않았습니다.")
        print("pip install gtts playsound 명령어로 설치하세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def simple_windows_tts_example():
    """Windows TTS 간단 사용 예시"""
    try:
        import pyttsx3
        
        # TTS 엔진 초기화
        engine = pyttsx3.init()
        
        # 음성 속도 설정
        engine.setProperty('rate', 150)
        
        # 텍스트 정의
        text = "안녕하세요! 이것은 Windows TTS 예시입니다."
        
        # 음성 변환 및 재생
        print("🔊 음성을 재생합니다...")
        engine.say(text)
        engine.runAndWait()
        
    except ImportError:
        print("❌ pyttsx3 라이브러리가 설치되지 않았습니다.")
        print("pip install pyttsx3 명령어로 설치하세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def batch_text_to_speech():
    """여러 문장을 한 번에 음성으로 변환하는 예시"""
    try:
        from gtts import gTTS
        from playsound import playsound
        import time
        
        # 여러 문장 정의
        sentences = [
            "첫 번째 문장입니다.",
            "두 번째 문장입니다.",
            "세 번째 문장입니다."
        ]
        
        for i, sentence in enumerate(sentences, 1):
            print(f"처리 중: {sentence}")
            
            # TTS 객체 생성
            tts = gTTS(text=sentence, lang='ko', slow=False)
            
            # 파일명 생성
            filename = f"sentence_{i}.mp3"
            
            # MP3 파일로 저장
            tts.save(filename)
            print(f"✅ '{filename}' 파일로 저장되었습니다.")
            
            # 음성 재생
            playsound(filename, block=True)
            
            # 재생 완료 후 잠시 대기
            time.sleep(1.5)
            
    except ImportError:
        print("❌ 필요한 라이브러리가 설치되지 않았습니다.")
        print("pip install gtts playsound 명령어로 설치하세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🎵 TTS 프로그램 사용 예시")
    print("=" * 50)
    
    print("\n1. Google TTS 예시 실행")
    simple_google_tts_example()
    
    print("\n" + "-" * 30)
    
    print("\n2. Windows TTS 예시 실행")
    simple_windows_tts_example()
    
    print("\n" + "-" * 30)
    
    print("\n3. 여러 문장 일괄 처리 예시")
    choice = input("여러 문장을 처리하시겠습니까? (y/n): ").strip().lower()
    if choice == 'y':
        batch_text_to_speech()
    
    print("\n👋 예시 실행 완료!") 