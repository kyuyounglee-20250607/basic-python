#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text-to-Speech (TTS) 프로그램
윈도우 환경에서 무료로 사용할 수 있는 TTS 기능을 제공합니다.

사용 가능한 TTS 엔진:
1. gTTS (Google Text-to-Speech) - 인터넷 연결 필요, 매우 자연스러운 음성
2. pyttsx3 - 오프라인 사용 가능, 윈도우 기본 음성 엔진 사용

필수 라이브러리 설치:
pip install gtts pyttsx3 playsound
"""

import os
import sys
import time
from pathlib import Path

def install_requirements():
    """필수 라이브러리 설치 확인 및 안내"""
    print("=== TTS 프로그램 라이브러리 설치 안내 ===")
    print("다음 명령어로 필요한 라이브러리를 설치하세요:")
    print("pip install gtts pyttsx3 playsound")
    print()

def check_libraries():
    """필요한 라이브러리가 설치되어 있는지 확인"""
    missing_libs = []
    
    try:
        import gtts
    except ImportError:
        missing_libs.append("gtts")
    
    try:
        import pyttsx3
    except ImportError:
        missing_libs.append("pyttsx3")
    
    try:
        import playsound
    except ImportError:
        missing_libs.append("playsound")
    
    if missing_libs:
        print(f"❌ 다음 라이브러리가 설치되지 않았습니다: {', '.join(missing_libs)}")
        install_requirements()
        return False
    
    print("✅ 모든 필요한 라이브러리가 설치되어 있습니다.")
    return True

class GoogleTTS:
    """Google TTS를 사용한 텍스트 음성 변환"""
    
    def __init__(self, lang='ko'):
        try:
            from gtts import gTTS
            self.gTTS = gTTS
            self.lang = lang
            self.available = True
        except ImportError:
            print("❌ gTTS 라이브러리가 설치되지 않았습니다.")
            self.available = False
    
    def text_to_speech(self, text, filename="output.mp3", play_audio=True):
        """텍스트를 음성으로 변환하고 MP3 파일로 저장"""
        if not self.available:
            print("gTTS를 사용할 수 없습니다.")
            return False
        
        try:
            print(f"🎤 Google TTS로 음성 변환 중... (언어: {self.lang})")
            
            # 텍스트를 음성으로 변환
            tts = self.gTTS(text=text, lang=self.lang, slow=False)
            
            # MP3 파일로 저장
            tts.save(filename)
            print(f"✅ 음성이 '{filename}' 파일로 저장되었습니다.")
            
            # 음성 재생
            if play_audio:
                self.play_audio(filename)
            
            return True
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False
    
    def play_audio(self, filename):
        """저장된 음성 파일 재생"""
        try:
            from playsound import playsound
            import time
            print("🔊 음성을 재생합니다...")
            playsound(filename, block=True)
            # 재생 완료 후 잠시 대기하여 자원 해제
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ 음성 재생 중 오류: {e}")
            print("💡 해결 방법: 다른 음성 재생 프로그램을 사용하거나 잠시 후 다시 시도해보세요.")

class WindowsTTS:
    """Windows 기본 TTS 엔진을 사용한 텍스트 음성 변환"""
    
    def __init__(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.available = True
            self.setup_voice()
        except ImportError:
            print("❌ pyttsx3 라이브러리가 설치되지 않았습니다.")
            self.available = False
        except Exception as e:
            print(f"❌ TTS 엔진 초기화 실패: {e}")
            self.available = False
    
    def setup_voice(self):
        """음성 설정"""
        try:
            # 사용 가능한 음성 목록 확인
            voices = self.engine.getProperty('voices')
            
            # 한국어 음성 찾기
            korean_voice = None
            for voice in voices:
                if 'korean' in voice.name.lower() or 'ko' in voice.id.lower():
                    korean_voice = voice
                    break
            
            # 한국어 음성이 있으면 설정, 없으면 기본 음성 사용
            if korean_voice:
                self.engine.setProperty('voice', korean_voice.id)
                print(f"✅ 한국어 음성 설정: {korean_voice.name}")
            else:
                print("⚠️ 한국어 음성을 찾을 수 없어 기본 음성을 사용합니다.")
                if voices:
                    self.engine.setProperty('voice', voices[0].id)
            
            # 음성 속도 설정 (기본값: 200)
            self.engine.setProperty('rate', 150)
            
            # 음량 설정 (0.0 ~ 1.0)
            self.engine.setProperty('volume', 0.9)
            
        except Exception as e:
            print(f"⚠️ 음성 설정 중 오류: {e}")
    
    def text_to_speech(self, text, play_audio=True):
        """텍스트를 음성으로 변환하고 재생"""
        if not self.available:
            print("Windows TTS를 사용할 수 없습니다.")
            return False
        
        try:
            print("🎤 Windows TTS로 음성 변환 중...")
            
            if play_audio:
                print("🔊 음성을 재생합니다...")
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                self.engine.say(text)
                self.engine.runAndWait()
            
            print("✅ 음성 변환 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False
    
    def save_to_mp3(self, text, filename="output.mp3"):
        """텍스트를 MP3 파일로 저장 (Windows TTS는 직접 MP3 저장 불가)"""
        print("⚠️ Windows TTS는 직접 MP3 저장을 지원하지 않습니다.")
        print("대신 Google TTS를 사용하거나, 음성 재생 후 녹음 프로그램을 사용하세요.")
        return False

def main():
    """메인 프로그램"""
    print("=" * 50)
    print("🎵 텍스트 음성 변환 (TTS) 프로그램")
    print("=" * 50)
    
    # 라이브러리 확인
    if not check_libraries():
        return
    
    # TTS 엔진 초기화
    google_tts = GoogleTTS()
    windows_tts = WindowsTTS()
    
    # 예시 텍스트
    example_texts = [
        "안녕하세요! 이것은 텍스트 음성 변환 프로그램입니다.",
        "Hello! This is a text-to-speech program.",
        "오늘 날씨가 정말 좋네요. 산책하기 딱 좋은 날씨입니다.",
        "파이썬으로 만든 TTS 프로그램이 정말 유용합니다."
    ]
    
    while True:
        print("\n" + "=" * 50)
        print("📋 메뉴 선택:")
        print("1. Google TTS 사용 (인터넷 필요, 매우 자연스러운 음성)")
        print("2. Windows TTS 사용 (오프라인 가능, 기본 음성)")
        print("3. 예시 문장으로 테스트")
        print("4. 종료")
        print("=" * 50)
        
        choice = input("선택하세요 (1-4): ").strip()
        
        if choice == "1":
            if not google_tts.available:
                print("❌ Google TTS를 사용할 수 없습니다.")
                continue
            
            print("\n🌐 Google TTS 모드")
            text = input("음성으로 변환할 텍스트를 입력하세요: ").strip()
            
            if text:
                filename = input("저장할 파일명을 입력하세요 (기본: output.mp3): ").strip()
                if not filename:
                    filename = "output.mp3"
                if not filename.endswith('.mp3'):
                    filename += '.mp3'
                
                google_tts.text_to_speech(text, filename)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "2":
            if not windows_tts.available:
                print("❌ Windows TTS를 사용할 수 없습니다.")
                continue
            
            print("\n🖥️ Windows TTS 모드")
            text = input("음성으로 변환할 텍스트를 입력하세요: ").strip()
            
            if text:
                windows_tts.text_to_speech(text)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "3":
            print("\n🧪 예시 문장 테스트")
            print("사용 가능한 예시:")
            for i, text in enumerate(example_texts, 1):
                print(f"{i}. {text}")
            
            try:
                test_choice = int(input("테스트할 예시 번호를 선택하세요 (1-4): ")) - 1
                if 0 <= test_choice < len(example_texts):
                    test_text = example_texts[test_choice]
                    print(f"\n선택된 텍스트: {test_text}")
                    
                    tts_choice = input("Google TTS(1) 또는 Windows TTS(2)를 선택하세요: ").strip()
                    
                    if tts_choice == "1" and google_tts.available:
                        google_tts.text_to_speech(test_text, "test_output.mp3")
                    elif tts_choice == "2" and windows_tts.available:
                        windows_tts.text_to_speech(test_text)
                    else:
                        print("❌ 잘못된 선택이거나 해당 TTS를 사용할 수 없습니다.")
                else:
                    print("❌ 잘못된 번호입니다.")
            except ValueError:
                print("❌ 숫자를 입력해주세요.")
        
        elif choice == "4":
            print("\n👋 프로그램을 종료합니다. 감사합니다!")
            break
        
        else:
            print("❌ 잘못된 선택입니다. 1-4 중에서 선택해주세요.")

if __name__ == "__main__":
    main() 