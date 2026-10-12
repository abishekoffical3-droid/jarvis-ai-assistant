"""Jarvis AI Configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")

# Voice Configuration
WAKE_WORD = "jarvis"
LISTENING_TIMEOUT = 10  # seconds
PHRASE_TIME_LIMIT = 5  # seconds
SPEAK_RATE = 150  # words per minute
LISTEN_LANGUAGE = "en-US"

# AI Model Configuration
AI_MODEL = "gpt-4o-mini"  # openai model
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 500
USE_GROQ = False  # Set True for faster free responses
GROQ_MODEL = "mixtral-8x7b-32768"

# UI Configuration
THEME = "dark"  # dark or light
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
FONT_SIZE = 12

# Feature Flags
ENABLE_WEB_SEARCH = True
ENABLE_VOICE_OUTPUT = True
ENABLE_HISTORY = True
ENABLE_OFFLINE_MODE = False
ENABLE_ANIMATIONS = True

# Path Configuration
HISTORY_FILE = "data/history.json"
LOG_FILE = "logs/jarvis.log"
COMMAND_DB = "data/commands.json"

# Advanced Settings
DEBUG_MODE = False
LOG_LEVEL = "INFO"
MAX_HISTORY_SIZE = 500
AUTO_LEARN_COMMANDS = True
BACKGROUND_LISTEN = False  # Android only
