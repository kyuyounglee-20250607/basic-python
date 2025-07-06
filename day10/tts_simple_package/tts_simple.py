#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 TTS 패키지 - 한국어, 영어, 중국어, 일본어 지원
가장 자연스러운 Google TTS 엔진만 사용합니다.

설치: pip install gtts pygame
"""

import os
import time
from typing import Optional

class Language:
    """지원 언어 상수"""
    KOREAN = "ko"
    ENGLISH = "en"
    CHINESE = "zh"
    JAPANESE = "ja"

class VoiceSpeed:
    """음성 속도 상수"""
    SLOW = True      # 느린 속도 (더 자연스러운 발음)
    NORMAL = False   # 일반 속도 (기본값)

class SimpleTTS:
    """간단한 TTS 패키지 - Google TTS 기반"""
    
    def __init__(self):
        """TTS 패키지 초기화"""
        self.available = self._check_availability()
        self.audio_player = self._init_audio_player()
    
    def _check_availability(self) -> bool:
        """Google TTS 사용 가능 여부 확인"""
        try:
            from gtts import gTTS
            return True
        except ImportError:
            print("❌ gTTS 라이브러리가 설치되지 않았습니다.")
            print("설치 명령어: pip install gtts")
            return False
    
    def _init_audio_player(self):
        """음성 재생 엔진 초기화"""
        try:
            import pygame
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            return pygame
        except ImportError:
            print("⚠️ pygame이 설치되지 않았습니다.")
            print("설치 명령어: pip install pygame")
            return None
    
    def speak(self, 
              text: str, 
              language: str = Language.KOREAN,
              speed: bool = VoiceSpeed.NORMAL,
              save_to_file: bool = False,
              filename: Optional[str] = None,
              play_audio: bool = True) -> bool:
        """
        텍스트를 음성으로 변환하고 재생
        
        Args:
            text: 변환할 텍스트
            language: 언어 (ko, en, zh, ja)
            speed: 음성 속도 (True=느림/자연스러움, False=일반)
            save_to_file: MP3 파일로 저장 여부
            filename: 저장할 파일명
            play_audio: 음성 재생 여부
        
        Returns:
            bool: 성공 여부
        """
        if not self.available:
            return False
        
        if not text.strip():
            print("❌ 텍스트가 비어있습니다.")
            return False
        
        try:
            from gtts import gTTS
            
            speed_text = "자연스러운" if speed else "일반"
            print(f"🎤 음성 변환 중... (언어: {language}, 속도: {speed_text})")
            
            # 파일명 생성
            if save_to_file and not filename:
                timestamp = int(time.time())
                filename = f"tts_output_{timestamp}.mp3"
            
            # Google TTS 변환 (slow=True로 더 자연스러운 발음)
            tts = gTTS(text=text, lang=language, slow=speed)
            
            # 파일로 저장
            if save_to_file and filename:
                tts.save(filename)
                print(f"✅ 음성이 '{filename}' 파일로 저장되었습니다.")
            
            # 음성 재생
            if play_audio and filename:
                return self._play_audio(filename)
            elif play_audio:
                # 임시 파일로 저장 후 재생
                temp_file = f"temp_{int(time.time())}.mp3"
                tts.save(temp_file)
                success = self._play_audio(temp_file)
                # 임시 파일 삭제
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return success
            
            return True
            
        except Exception as e:
            print(f"❌ 음성 변환 오류: {e}")
            return False
    
    def _play_audio(self, filename: str) -> bool:
        """음성 파일 재생"""
        if not os.path.exists(filename):
            print(f"❌ 파일을 찾을 수 없습니다: {filename}")
            return False
        
        if not self.audio_player:
            print("❌ 음성 재생 엔진을 사용할 수 없습니다.")
            return False
        
        try:
            print("🔊 음성을 재생합니다...")
            
            # pygame으로 음성 재생
            self.audio_player.mixer.music.load(filename)
            self.audio_player.mixer.music.play()
            
            # 재생 완료 대기
            while self.audio_player.mixer.music.get_busy():
                self.audio_player.time.Clock().tick(10)
            
            # 자원 정리
            self.audio_player.mixer.music.unload()
            
            print("✅ 음성 재생 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 음성 재생 오류: {e}")
            return False
    
    def batch_speak(self, texts: list, 
                   language: str = Language.KOREAN,
                   speed: bool = VoiceSpeed.NORMAL,
                   save_to_files: bool = False,
                   delay_between: float = 1.0) -> bool:
        """
        여러 텍스트를 연속으로 음성 변환
        
        Args:
            texts: 변환할 텍스트 리스트
            language: 언어
            speed: 음성 속도 (True=느림/자연스러움, False=일반)
            save_to_files: 각각 MP3 파일로 저장 여부
            delay_between: 문장 간 대기 시간 (초)
        
        Returns:
            bool: 성공 여부
        """
        if not texts:
            print("❌ 텍스트 리스트가 비어있습니다.")
            return False
        
        speed_text = "자연스러운" if speed else "일반"
        print(f"🔄 {len(texts)}개 문장을 연속으로 변환합니다... (속도: {speed_text})")
        
        success_count = 0
        for i, text in enumerate(texts, 1):
            print(f"\n처리 중 ({i}/{len(texts)}): {text[:50]}...")
            
            filename = f"batch_speech_{i}.mp3" if save_to_files else None
            
            success = self.speak(
                text=text,
                language=language,
                speed=speed,
                save_to_file=save_to_files,
                filename=filename,
                play_audio=True
            )
            
            if success:
                success_count += 1
            
            # 다음 문장 전 대기
            if i < len(texts):
                time.sleep(delay_between)
        
        print(f"\n✅ 완료: {success_count}/{len(texts)} 문장 변환 성공")
        return success_count == len(texts)
    
    def get_supported_languages(self) -> dict:
        """지원 언어 목록 반환"""
        return {
            "한국어": Language.KOREAN,
            "English": Language.ENGLISH,
            "中文": Language.CHINESE,
            "日本語": Language.JAPANESE
        }

# 편의 함수들
def quick_speak(text: str, language: str = Language.KOREAN, speed: bool = VoiceSpeed.NORMAL) -> bool:
    """
    빠른 음성 변환
    
    Args:
        text: 변환할 텍스트
        language: 언어
        speed: 음성 속도 (True=느림/자연스러움, False=일반)
    
    Returns:
        bool: 성공 여부
    """
    tts = SimpleTTS()
    return tts.speak(text, language=language, speed=speed)

def speak_korean(text: str, speed: bool = VoiceSpeed.NORMAL) -> bool:
    """한국어 음성 변환"""
    return quick_speak(text, Language.KOREAN, speed)

def speak_english(text: str, speed: bool = VoiceSpeed.NORMAL) -> bool:
    """영어 음성 변환"""
    return quick_speak(text, Language.ENGLISH, speed)

def speak_chinese(text: str, speed: bool = VoiceSpeed.NORMAL) -> bool:
    """중국어 음성 변환"""
    return quick_speak(text, Language.CHINESE, speed)

def speak_japanese(text: str, speed: bool = VoiceSpeed.NORMAL) -> bool:
    """일본어 음성 변환"""
    return quick_speak(text, Language.JAPANESE, speed)

# 자연스러운 여성 음성 전용 함수들
def speak_natural_korean(text: str) -> bool:
    """자연스러운 한국어 여성 음성 변환"""
    return speak_korean(text, speed=VoiceSpeed.SLOW)

def speak_natural_english(text: str) -> bool:
    """자연스러운 영어 여성 음성 변환"""
    return speak_english(text, speed=VoiceSpeed.SLOW)

def speak_natural_chinese(text: str) -> bool:
    """자연스러운 중국어 여성 음성 변환"""
    return speak_chinese(text, speed=VoiceSpeed.SLOW)

def speak_natural_japanese(text: str) -> bool:
    """자연스러운 일본어 여성 음성 변환"""
    return speak_japanese(text, speed=VoiceSpeed.SLOW) 