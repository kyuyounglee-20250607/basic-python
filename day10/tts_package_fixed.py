#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고성능 TTS 패키지 - 남자/여자 음성 선택 가능
가장 안정적이고 자연스러운 음성을 제공합니다.

사용 가능한 음성:
- Google TTS (인터넷 필요, 매우 자연스러운 음성)
- Windows TTS (오프라인 가능, 시스템 음성 사용)

설치: pip install gtts pyttsx3 pygame
"""

import os
import sys
import time
import threading
from pathlib import Path
from typing import Optional, Dict, List, Tuple

class VoiceGender:
    """음성 성별 상수"""
    MALE = "male"
    FEMALE = "female"
    AUTO = "auto"

class VoiceLanguage:
    """지원 언어 상수"""
    KOREAN = "ko"
    ENGLISH = "en"
    JAPANESE = "ja"
    CHINESE = "zh"

class GoogleTTS:
    """Google TTS 엔진"""
    
    def __init__(self):
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Google TTS 사용 가능 여부 확인"""
        try:
            from gtts import gTTS
            return True
        except ImportError:
            print("❌ gTTS 라이브러리가 설치되지 않았습니다.")
            return False
    
    def is_available(self) -> bool:
        return self.available
    
    def convert_to_speech(self, text: str, language: str, gender: str, 
                         filename: Optional[str] = None) -> bool:
        """
        텍스트를 음성으로 변환
        
        Args:
            text: 변환할 텍스트
            language: 언어 코드
            gender: 성별 (Google TTS는 성별 구분이 제한적)
            filename: 저장할 파일명
        
        Returns:
            bool: 성공 여부
        """
        if not self.available:
            return False
        
        try:
            from gtts import gTTS
            
            # Google TTS 객체 생성
            tts = gTTS(text=text, lang=language, slow=False)
            
            # 파일로 저장
            if filename:
                tts.save(filename)
                print(f"✅ 음성이 '{filename}' 파일로 저장되었습니다.")
            
            return True
            
        except Exception as e:
            print(f"❌ Google TTS 변환 오류: {e}")
            return False

class WindowsTTS:
    """Windows TTS 엔진"""
    
    def __init__(self):
        self.engine = None
        self.voices = []
        self.available = self._initialize()
    
    def _initialize(self) -> bool:
        """Windows TTS 초기화"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.voices = self.engine.getProperty('voices')
            
            # 기본 설정
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
            
            return True
            
        except ImportError:
            print("❌ pyttsx3 라이브러리가 설치되지 않았습니다.")
            return False
        except Exception as e:
            print(f"❌ Windows TTS 초기화 실패: {e}")
            return False
    
    def is_available(self) -> bool:
        return self.available and self.engine is not None
    
    def get_available_voices(self) -> List[str]:
        """사용 가능한 음성 목록 반환"""
        if not self.is_available():
            return []
        
        voice_names = []
        for voice in self.voices:
            voice_names.append(voice.name)
        
        return voice_names
    
    def _select_voice_by_gender(self, gender: str) -> bool:
        """성별에 따른 음성 선택"""
        if not self.is_available() or not self.voices:
            return False
        
        if gender == VoiceGender.AUTO:
            return True
        
        # 성별에 따른 음성 선택 (Windows TTS는 성별 구분이 제한적)
        # 실제로는 음성 이름에서 성별을 추측해야 함
        selected_voice = None
        
        for voice in self.voices:
            voice_name_lower = voice.name.lower()
            
            if gender == VoiceGender.MALE:
                if any(keyword in voice_name_lower for keyword in ['male', '남성', '남자', 'david', 'james']):
                    selected_voice = voice
                    break
            elif gender == VoiceGender.FEMALE:
                if any(keyword in voice_name_lower for keyword in ['female', '여성', '여자', 'zira', 'hazel']):
                    selected_voice = voice
                    break
        
        # 적절한 음성을 찾지 못한 경우 기본 음성 사용
        if selected_voice is None and self.voices:
            selected_voice = self.voices[0]
        
        if selected_voice and self.engine:
            self.engine.setProperty('voice', selected_voice.id)
            print(f"✅ 선택된 음성: {selected_voice.name}")
            return True
        
        return False
    
    def speak(self, text: str, gender: str, language: str, play_audio: bool = True) -> bool:
        """
        텍스트를 음성으로 변환하고 재생
        
        Args:
            text: 변환할 텍스트
            gender: 성별
            language: 언어 (Windows TTS는 제한적)
            play_audio: 음성 재생 여부
        
        Returns:
            bool: 성공 여부
        """
        if not self.is_available():
            return False
        
        try:
            # 성별에 따른 음성 선택
            self._select_voice_by_gender(gender)
            
            # 음성 변환 및 재생
            if play_audio and self.engine:
                print("🔊 음성을 재생합니다...")
                self.engine.say(text)
                self.engine.runAndWait()
            
            print("✅ Windows TTS 변환 완료!")
            return True
            
        except Exception as e:
            print(f"❌ Windows TTS 오류: {e}")
            return False

class AudioPlayer:
    """안정적인 음성 재생 클래스"""
    
    def __init__(self):
        self.pygame_available = self._check_pygame()
        self.playsound_available = self._check_playsound()
    
    def _check_pygame(self) -> bool:
        """pygame 사용 가능 여부 확인"""
        try:
            import pygame
            pygame.mixer.init()
            return True
        except ImportError:
            print("⚠️ pygame이 설치되지 않았습니다. playsound를 사용합니다.")
            return False
        except Exception:
            return False
    
    def _check_playsound(self) -> bool:
        """playsound 사용 가능 여부 확인"""
        try:
            from playsound import playsound
            return True
        except ImportError:
            print("❌ playsound가 설치되지 않았습니다.")
            return False
    
    def play_audio(self, filename: str) -> bool:
        """
        음성 파일 재생
        
        Args:
            filename: 재생할 파일명
        
        Returns:
            bool: 성공 여부
        """
        if not os.path.exists(filename):
            print(f"❌ 파일을 찾을 수 없습니다: {filename}")
            return False
        
        # pygame 우선 사용 (더 안정적)
        if self.pygame_available:
            return self._play_with_pygame(filename)
        elif self.playsound_available:
            return self._play_with_playsound(filename)
        else:
            print("❌ 사용 가능한 음성 재생 라이브러리가 없습니다.")
            return False
    
    def _play_with_pygame(self, filename: str) -> bool:
        """pygame을 사용한 안정적인 음성 재생"""
        try:
            import pygame
            
            print("🔊 음성을 재생합니다... (pygame 사용)")
            
            # 음성 재생
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # 재생 완료 대기
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # 자원 정리
            pygame.mixer.music.unload()
            
            print("✅ 음성 재생 완료!")
            return True
            
        except Exception as e:
            print(f"❌ pygame 재생 오류: {e}")
            return False
    
    def _play_with_playsound(self, filename: str) -> bool:
        """playsound를 사용한 음성 재생"""
        try:
            from playsound import playsound
            
            print("🔊 음성을 재생합니다... (playsound 사용)")
            playsound(filename, block=True)
            time.sleep(0.5)  # 자원 해제 대기
            
            print("✅ 음성 재생 완료!")
            return True
            
        except Exception as e:
            print(f"❌ playsound 재생 오류: {e}")
            return False

class TTSPackage:
    """고성능 TTS 패키지 메인 클래스"""
    
    def __init__(self, default_language: str = VoiceLanguage.KOREAN):
        """
        TTS 패키지 초기화
        
        Args:
            default_language: 기본 언어 (ko, en, ja, zh)
        """
        self.default_language = default_language
        self.google_tts = GoogleTTS()
        self.windows_tts = WindowsTTS()
        self.audio_player = AudioPlayer()
        
        # 음성 설정
        self.voice_settings = {
            VoiceLanguage.KOREAN: {
                VoiceGender.MALE: {"lang": "ko", "tld": "com"},
                VoiceGender.FEMALE: {"lang": "ko", "tld": "com"}
            },
            VoiceLanguage.ENGLISH: {
                VoiceGender.MALE: {"lang": "en", "tld": "com"},
                VoiceGender.FEMALE: {"lang": "en", "tld": "com"}
            },
            VoiceLanguage.JAPANESE: {
                VoiceGender.MALE: {"lang": "ja", "tld": "com"},
                VoiceGender.FEMALE: {"lang": "ja", "tld": "com"}
            },
            VoiceLanguage.CHINESE: {
                VoiceGender.MALE: {"lang": "zh", "tld": "com"},
                VoiceGender.FEMALE: {"lang": "zh", "tld": "com"}
            }
        }
    
    def speak(self, 
              text: str, 
              gender: str = VoiceGender.AUTO,
              language: Optional[str] = None,
              save_to_file: bool = False,
              filename: Optional[str] = None,
              play_audio: bool = True,
              use_google: bool = True) -> bool:
        """
        텍스트를 음성으로 변환하고 재생
        
        Args:
            text: 변환할 텍스트
            gender: 음성 성별 (male, female, auto)
            language: 언어 (ko, en, ja, zh)
            save_to_file: MP3 파일로 저장 여부
            filename: 저장할 파일명
            play_audio: 음성 재생 여부
            use_google: Google TTS 사용 여부 (False면 Windows TTS 사용)
        
        Returns:
            bool: 성공 여부
        """
        if not text.strip():
            print("❌ 텍스트가 비어있습니다.")
            return False
        
        language = language or self.default_language
        
        if use_google and self.google_tts.is_available():
            return self._speak_with_google(text, gender, language, save_to_file, filename, play_audio)
        elif self.windows_tts.is_available():
            return self._speak_with_windows(text, gender, language, save_to_file, filename, play_audio)
        else:
            print("❌ 사용 가능한 TTS 엔진이 없습니다.")
            return False
    
    def _speak_with_google(self, text: str, gender: str, language: str, 
                          save_to_file: bool, filename: Optional[str], play_audio: bool) -> bool:
        """Google TTS를 사용한 음성 변환"""
        try:
            print(f"🎤 Google TTS로 음성 변환 중... (언어: {language}, 성별: {gender})")
            
            # 파일명 생성
            if save_to_file and not filename:
                timestamp = int(time.time())
                filename = f"tts_output_{timestamp}.mp3"
            
            # Google TTS 변환
            success = self.google_tts.convert_to_speech(
                text=text,
                language=language,
                gender=gender,
                filename=filename if save_to_file else None
            )
            
            if success and play_audio and filename:
                return self.audio_player.play_audio(filename)
            
            return success
            
        except Exception as e:
            print(f"❌ Google TTS 오류: {e}")
            return False
    
    def _speak_with_windows(self, text: str, gender: str, language: str,
                           save_to_file: bool, filename: Optional[str], play_audio: bool) -> bool:
        """Windows TTS를 사용한 음성 변환"""
        try:
            print(f"🎤 Windows TTS로 음성 변환 중... (성별: {gender})")
            
            return self.windows_tts.speak(
                text=text,
                gender=gender,
                language=language,
                play_audio=play_audio
            )
            
        except Exception as e:
            print(f"❌ Windows TTS 오류: {e}")
            return False
    
    def batch_speak(self, texts: List[str], 
                   gender: str = VoiceGender.AUTO,
                   language: Optional[str] = None,
                   save_to_files: bool = False,
                   delay_between: float = 1.0) -> bool:
        """
        여러 텍스트를 연속으로 음성 변환
        
        Args:
            texts: 변환할 텍스트 리스트
            gender: 음성 성별
            language: 언어
            save_to_files: 각각 MP3 파일로 저장 여부
            delay_between: 문장 간 대기 시간 (초)
        
        Returns:
            bool: 성공 여부
        """
        if not texts:
            print("❌ 텍스트 리스트가 비어있습니다.")
            return False
        
        print(f"🔄 {len(texts)}개 문장을 연속으로 변환합니다...")
        
        success_count = 0
        for i, text in enumerate(texts, 1):
            print(f"\n처리 중 ({i}/{len(texts)}): {text[:50]}...")
            
            filename = f"batch_speech_{i}.mp3" if save_to_files else None
            
            success = self.speak(
                text=text,
                gender=gender,
                language=language,
                save_to_file=save_to_files,
                filename=filename,
                play_audio=True,
                use_google=True
            )
            
            if success:
                success_count += 1
            
            # 다음 문장 전 대기
            if i < len(texts):
                time.sleep(delay_between)
        
        print(f"\n✅ 완료: {success_count}/{len(texts)} 문장 변환 성공")
        return success_count == len(texts)
    
    def get_available_voices(self) -> Dict[str, List[str]]:
        """사용 가능한 음성 목록 반환"""
        voices = {
            "Google TTS": ["남성 음성", "여성 음성"],
            "Windows TTS": []
        }
        
        if self.windows_tts.is_available():
            voices["Windows TTS"] = self.windows_tts.get_available_voices()
        
        return voices
    
    def test_voices(self, test_text: str = "안녕하세요! 이것은 음성 테스트입니다."):
        """모든 음성으로 테스트"""
        print("🧪 음성 테스트를 시작합니다...")
        
        # Google TTS 테스트
        if self.google_tts.is_available():
            print("\n🌐 Google TTS 테스트:")
            for gender in [VoiceGender.MALE, VoiceGender.FEMALE]:
                print(f"  - {gender} 음성 테스트 중...")
                self.speak(test_text, gender=gender, use_google=True)
                time.sleep(1)
        
        # Windows TTS 테스트
        if self.windows_tts.is_available():
            print("\n🖥️ Windows TTS 테스트:")
            for gender in [VoiceGender.MALE, VoiceGender.FEMALE]:
                print(f"  - {gender} 음성 테스트 중...")
                self.speak(test_text, gender=gender, use_google=False)
                time.sleep(1)
        
        print("\n✅ 음성 테스트 완료!")

# 사용 예시 및 테스트 함수들
def create_tts_package() -> TTSPackage:
    """TTS 패키지 인스턴스 생성"""
    return TTSPackage()

def quick_speak(text: str, gender: str = VoiceGender.AUTO) -> bool:
    """
    빠른 음성 변환 (간단한 사용법)
    
    Args:
        text: 변환할 텍스트
        gender: 음성 성별 (male, female, auto)
    
    Returns:
        bool: 성공 여부
    """
    tts = create_tts_package()
    return tts.speak(text, gender=gender)

def demo_voices():
    """음성 데모 실행"""
    tts = create_tts_package()
    
    demo_texts = [
        "안녕하세요! 이것은 남성 음성 테스트입니다.",
        "안녕하세요! 이것은 여성 음성 테스트입니다.",
        "Hello! This is a male voice test.",
        "Hello! This is a female voice test."
    ]
    
    print("🎵 TTS 패키지 음성 데모")
    print("=" * 50)
    
    # 한국어 테스트
    print("\n🇰🇷 한국어 음성 테스트:")
    tts.speak(demo_texts[0], gender=VoiceGender.MALE, language=VoiceLanguage.KOREAN)
    time.sleep(1)
    tts.speak(demo_texts[1], gender=VoiceGender.FEMALE, language=VoiceLanguage.KOREAN)
    
    # 영어 테스트
    print("\n🇺🇸 영어 음성 테스트:")
    tts.speak(demo_texts[2], gender=VoiceGender.MALE, language=VoiceLanguage.ENGLISH)
    time.sleep(1)
    tts.speak(demo_texts[3], gender=VoiceGender.FEMALE, language=VoiceLanguage.ENGLISH)
    
    print("\n✅ 데모 완료!")

if __name__ == "__main__":
    # 패키지 테스트
    demo_voices() 