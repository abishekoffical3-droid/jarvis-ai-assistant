"""Voice input/output handling"""
import speech_recognition as sr
import pyttsx3
from typing import Optional, Callable
import logging
from config import (
    LISTENING_TIMEOUT, PHRASE_TIME_LIMIT, SPEAK_RATE, LISTEN_LANGUAGE, ENABLE_VOICE_OUTPUT
)

logger = logging.getLogger(__name__)


class VoiceHandler:
    """Handle speech recognition and text-to-speech"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', SPEAK_RATE)
        self.is_listening = False
        
    def listen(self, timeout: Optional[int] = None) -> Optional[str]:
        """Listen for voice input"""
        if timeout is None:
            timeout = LISTENING_TIMEOUT
        
        try:
            self.is_listening = True
            with sr.Microphone() as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=PHRASE_TIME_LIMIT
                )
            
            self.is_listening = False
            
            # Try Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio, language=LISTEN_LANGUAGE)
                logger.info(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return None
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {e}")
                return None
                
        except sr.RequestError as e:
            logger.error(f"Microphone error: {e}")
            return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return None
        finally:
            self.is_listening = False
    
    def speak(self, text: str):
        """Speak text using text-to-speech"""
        if not ENABLE_VOICE_OUTPUT:
            return
        
        try:
            logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
    
    def set_voice_speed(self, rate: int):
        """Set speech rate"""
        self.engine.setProperty('rate', rate)
    
    def list_microphones(self) -> list:
        """List available microphones"""
        mics = []
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            mics.append({"index": index, "name": name})
        return mics
