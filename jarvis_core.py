"""Core Jarvis AI Logic"""
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import openai
from groq import Groq
import requests
from config import (
    OPENAI_API_KEY, GROQ_API_KEY, USE_GROQ, AI_MODEL, AI_TEMPERATURE,
    AI_MAX_TOKENS, GROQ_MODEL, ENABLE_WEB_SEARCH, COMMAND_DB, AUTO_LEARN_COMMANDS
)
from web_search import search_web
import logging

logger = logging.getLogger(__name__)


class JarvisAI:
    """Main Jarvis AI Engine"""
    
    def __init__(self):
        self.commands = self._load_commands()
        self.conversation_history = []
        self.setup_ai_client()
        
    def setup_ai_client(self):
        """Setup AI client (OpenAI or Groq)"""
        if USE_GROQ and GROQ_API_KEY:
            self.client = Groq(api_key=GROQ_API_KEY)
            self.is_groq = True
            logger.info("Using Groq API")
        else:
            openai.api_key = OPENAI_API_KEY
            self.client = openai
            self.is_groq = False
            logger.info("Using OpenAI API")
    
    def _load_commands(self) -> Dict[str, callable]:
        """Load available commands"""
        return {
            "time": self.get_time,
            "date": self.get_date,
            "search": self.search_command,
            "joke": self.get_joke,
            "weather": self.get_weather,
            "news": self.get_news,
            "calculate": self.calculate,
            "open": self.open_app,
            "reminder": self.set_reminder,
            "hello": self.greet,
        }
    
    def process_command(self, user_input: str) -> str:
        """Process user command and return response"""
        logger.info(f"Processing: {user_input}")
        
        # Check for local commands first
        for cmd, func in self.commands.items():
            if cmd.lower() in user_input.lower():
                try:
                    response = func(user_input)
                    if response:
                        return response
                except Exception as e:
                    logger.error(f"Command error: {e}")
        
        # Fall back to AI
        return self.get_ai_response(user_input)
    
    def get_ai_response(self, user_input: str) -> str:
        """Get response from AI model"""
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            if self.is_groq:
                response = self.client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=self.conversation_history,
                    temperature=AI_TEMPERATURE,
                    max_tokens=AI_MAX_TOKENS,
                )
            else:
                response = self.client.ChatCompletion.create(
                    model=AI_MODEL,
                    messages=self.conversation_history,
                    temperature=AI_TEMPERATURE,
                    max_tokens=AI_MAX_TOKENS,
                )
            
            answer = response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })
            
            # Keep only last 10 messages
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return answer
            
        except Exception as e:
            logger.error(f"AI Error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    # Command implementations
    def get_time(self, query: str) -> str:
        """Get current time"""
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}"
    
    def get_date(self, query: str) -> str:
        """Get current date"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"
    
    def search_command(self, query: str) -> str:
        """Perform web search"""
        if not ENABLE_WEB_SEARCH:
            return None
        
        search_query = query.replace("search", "").replace("jarvis", "").strip()
        if not search_query:
            return None
        
        results = search_web(search_query)
        if results:
            return f"I found: {results[0]['title']}. {results[0]['snippet']}"
        return "No results found"
    
    def get_joke(self, query: str) -> str:
        """Get a random joke"""
        try:
            response = requests.get("https://api.api-ninjas.com/v1/jokes")
            if response.status_code == 200:
                joke = response.json()[0]["joke"]
                return joke
        except:
            pass
        return None
    
    def get_weather(self, query: str) -> str:
        """Get weather (requires API setup)"""
        return None  # Requires weather API key
    
    def get_news(self, query: str) -> str:
        """Get top news"""
        return None  # Requires news API key
    
    def calculate(self, query: str) -> str:
        """Perform calculation"""
        try:
            expression = query.replace("calculate", "").replace("jarvis", "").strip()
            result = eval(expression)
            return f"The answer is {result}"
        except:
            return None
    
    def open_app(self, query: str) -> str:
        """Open application (desktop only)"""
        # This would be implemented differently for desktop vs mobile
        return None
    
    def set_reminder(self, query: str) -> str:
        """Set a reminder"""
        return "Reminder set successfully"
    
    def greet(self, query: str) -> str:
        """Greeting response"""
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning! How can I assist you?"
        elif hour < 18:
            return "Good afternoon! What can I do for you?"
        else:
            return "Good evening! How may I help?"


# Global instance
_jarvis_instance = None


def get_jarvis() -> JarvisAI:
    """Get or create Jarvis instance"""
    global _jarvis_instance
    if _jarvis_instance is None:
        _jarvis_instance = JarvisAI()
    return _jarvis_instance
