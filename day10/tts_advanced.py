#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고급 TTS 프로그램 - 안정적인 음성 재생
playsound의 자원 해제 문제를 해결하기 위해 pygame을 대안으로 제공합니다.
"""

import os
import sys
import time
from pathlib import Path

def install_advanced_requirements():
    """고급 기능을 위한 라이브러리 설치 안내"""
    print("=== 고급 TTS 프로그램 라이브러리 설치 안내 ===")
    print("안정적인 음성 재생을 위해 다음 라이브러리를 설치하세요:")
    print("pip install gtts pyttsx3 pygame")
    print()

def check_advanced_libraries():
    """고급 라이브러리 설치 확인"""
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
        import pygame
    except ImportError:
        missing_libs.append("pygame")
    
    if missing_libs:
        print(f"❌ 다음 라이브러리가 설치되지 않았습니다: {', '.join(missing_libs)}")
        install_advanced_requirements()
        return False
    
    print("✅ 모든 필요한 라이브러리가 설치되어 있습니다.")
    return True

class AdvancedGoogleTTS:
    """고급 Google TTS - pygame을 사용한 안정적인 음성 재생"""
    
    def __init__(self, lang='ko'):
        try:
            from gtts import gTTS
            self.gTTS = gTTS
            self.lang = lang
            self.available = True
            self.setup_pygame()
        except ImportError:
            print("❌ gTTS 라이브러리가 설치되지 않았습니다.")
            self.available = False
    
    def setup_pygame(self):
        """pygame 초기화"""
        try:
            import pygame
            pygame.mixer.init()
            self.pygame = pygame
            self.pygame_available = True
        except Exception as e:
            print(f"⚠️ pygame 초기화 실패: {e}")
            self.pygame_available = False
    
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
                self.play_audio_pygame(filename)
            
            return True
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False
    
    def play_audio_pygame(self, filename):
        """pygame을 사용한 안정적인 음성 재생"""
        if not self.pygame_available:
            print("❌ pygame을 사용할 수 없습니다.")
            return False
        
        try:
            print("🔊 음성을 재생합니다... (pygame 사용)")
            
            # pygame으로 음성 재생
            self.pygame.mixer.music.load(filename)
            self.pygame.mixer.music.play()
            
            # 재생이 끝날 때까지 대기
            while self.pygame.mixer.music.get_busy():
                self.pygame.time.Clock().tick(10)
            
            # 재생 완료 후 자원 정리
            self.pygame.mixer.music.unload()
            
            print("✅ 음성 재생 완료!")
            return True
            
        except Exception as e:
            print(f"❌ pygame 음성 재생 중 오류: {e}")
            return False
    
    def play_audio_playsound(self, filename):
        """playsound를 사용한 음성 재생 (대안)"""
        try:
            from playsound import playsound
            print("🔊 음성을 재생합니다... (playsound 사용)")
            playsound(filename, block=True)
            time.sleep(0.5)  # 자원 해제를 위한 대기
            return True
        except Exception as e:
            print(f"❌ playsound 음성 재생 중 오류: {e}")
            return False

class AdvancedWindowsTTS:
    """고급 Windows TTS"""
    
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
            voices = self.engine.getProperty('voices')
            
            # 한국어 음성 찾기
            korean_voice = None
            for voice in voices:
                if 'korean' in voice.name.lower() or 'ko' in voice.id.lower():
                    korean_voice = voice
                    break
            
            if korean_voice:
                self.engine.setProperty('voice', korean_voice.id)
                print(f"✅ 한국어 음성 설정: {korean_voice.name}")
            else:
                print("⚠️ 한국어 음성을 찾을 수 없어 기본 음성을 사용합니다.")
                if voices:
                    self.engine.setProperty('voice', voices[0].id)
            
            # 음성 속도 설정
            self.engine.setProperty('rate', 150)
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
            
            print("✅ 음성 변환 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False

def batch_convert_with_delay():
    """지연 시간을 두고 여러 파일을 변환하는 예시"""
    try:
        from gtts import gTTS
        import pygame
        
        # pygame 초기화
        pygame.mixer.init()
        
        sentences = [
            "첫 번째 문장입니다.",
            "두 번째 문장입니다.",
            "세 번째 문장입니다.",
            "네 번째 문장입니다."
        ]
        
        print("🔄 여러 문장을 안정적으로 변환 중...")
        
        for i, sentence in enumerate(sentences, 1):
            print(f"\n처리 중 ({i}/{len(sentences)}): {sentence}")
            
            # TTS 객체 생성
            tts = gTTS(text=sentence, lang='ko', slow=False)
            
            # 파일명 생성
            filename = f"advanced_sentence_{i}.mp3"
            
            # MP3 파일로 저장
            tts.save(filename)
            print(f"✅ '{filename}' 파일로 저장되었습니다.")
            
            # pygame으로 안정적 재생
            try:
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                
                # 재생 완료 대기
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # 자원 정리
                pygame.mixer.music.unload()
                
                print(f"✅ '{filename}' 재생 완료")
                
                # 다음 파일 처리 전 대기
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ 재생 중 오류: {e}")
        
        print("\n🎉 모든 문장 처리 완료!")
        
    except ImportError:
        print("❌ 필요한 라이브러리가 설치되지 않았습니다.")
        print("pip install gtts pygame 명령어로 설치하세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def main():
    """메인 프로그램"""
    print("=" * 60)
    print("🎵 고급 텍스트 음성 변환 (TTS) 프로그램")
    print("=" * 60)
    
    # 라이브러리 확인
    if not check_advanced_libraries():
        return
    
    # TTS 엔진 초기화
    google_tts = AdvancedGoogleTTS()
    windows_tts = AdvancedWindowsTTS()
    
    # 예시 텍스트
    example_texts = [
        "안녕하세요! 이것은 고급 TTS 프로그램입니다.",
        "Hello! This is an advanced text-to-speech program.",
        "오늘 날씨가 정말 좋네요. 산책하기 딱 좋은 날씨입니다.",
        "파이썬으로 만든 고급 TTS 프로그램이 정말 유용합니다."
    ]
    
    while True:
        print("\n" + "=" * 60)
        print("📋 메뉴 선택:")
        print("1. Google TTS 사용 (pygame 재생)")
        print("2. Google TTS 사용 (playsound 재생)")
        print("3. Windows TTS 사용")
        print("4. 여러 문장 안정적 변환 (pygame)")
        print("5. 예시 문장으로 테스트")
        print("6. 종료")
        print("=" * 60)
        
        choice = input("선택하세요 (1-6): ").strip()
        
        if choice == "1":
            if not google_tts.available:
                print("❌ Google TTS를 사용할 수 없습니다.")
                continue
            
            print("\n🌐 Google TTS 모드 (pygame 재생)")
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
            if not google_tts.available:
                print("❌ Google TTS를 사용할 수 없습니다.")
                continue
            
            print("\n🌐 Google TTS 모드 (playsound 재생)")
            text = input("음성으로 변환할 텍스트를 입력하세요: ").strip()
            
            if text:
                filename = input("저장할 파일명을 입력하세요 (기본: output.mp3): ").strip()
                if not filename:
                    filename = "output.mp3"
                if not filename.endswith('.mp3'):
                    filename += '.mp3'
                
                # TTS 변환
                tts = google_tts.gTTS(text=text, lang=google_tts.lang, slow=False)
                tts.save(filename)
                print(f"✅ 음성이 '{filename}' 파일로 저장되었습니다.")
                
                # playsound로 재생
                google_tts.play_audio_playsound(filename)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "3":
            if not windows_tts.available:
                print("❌ Windows TTS를 사용할 수 없습니다.")
                continue
            
            print("\n🖥️ Windows TTS 모드")
            text = input("음성으로 변환할 텍스트를 입력하세요: ").strip()
            
            if text:
                windows_tts.text_to_speech(text)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "4":
            print("\n🔄 여러 문장 안정적 변환 (pygame 사용)")
            batch_convert_with_delay()
        
        elif choice == "5":
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
                        google_tts.text_to_speech(test_text, "test_advanced.mp3")
                    elif tts_choice == "2" and windows_tts.available:
                        windows_tts.text_to_speech(test_text)
                    else:
                        print("❌ 잘못된 선택이거나 해당 TTS를 사용할 수 없습니다.")
                else:
                    print("❌ 잘못된 번호입니다.")
            except ValueError:
                print("❌ 숫자를 입력해주세요.")
        
        elif choice == "6":
            print("\n👋 프로그램을 종료합니다. 감사합니다!")
            break
        
        else:
            print("❌ 잘못된 선택입니다. 1-6 중에서 선택해주세요.")

if __name__ == "__main__":
    main() 