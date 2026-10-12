# Jarvis AI - Smart Voice Assistant

🎯 **Full-featured AI voice assistant** with desktop UI, Android app, and automation capabilities.

## Features

✨ **Core Features:**
- 🎤 Voice recognition (speech-to-text)
- 🔊 Text-to-speech responses
- 🧠 AI-powered responses (OpenAI/Groq API)
- 🌐 Web search integration
- 🤖 Smart commands & automation
- 💾 Command history & learning
- ⚙️ Customizable wake words
- 🎨 Beautiful dark/light UI themes

**Desktop Version:**
- PyQt5-based GUI
- Real-time voice input/output
- Command suggestions
- Settings panel
- Chat history

**Android Version:**
- Native Kivy app
- Touch-optimized UI
- Background voice listening
- Quick action buttons
- Auto APK builds via GitHub Actions

## Installation

### Desktop (Windows/Mac/Linux)

```bash
# Clone repo
git clone https://github.com/abishekoffical3-droid/jarvis-ai-assistant
cd jarvis-ai-assistant

# Install dependencies
pip install -r requirements-desktop.txt

# Run Jarvis
python jarvis_desktop.py
```

### Android

**Option 1: Direct APK Download**
- Go to [Releases](https://github.com/abishekoffical3-droid/jarvis-ai-assistant/releases)
- Download latest `jarvis-ai.apk`
- Install on Android phone

**Option 2: Build from source**
```bash
pip install buildozer cython
cd android
buildozer android release
```

## Configuration

### Setup API Keys

Create `config.py` in root:

```python
OPENAI_API_KEY = "your-openai-key"
GROQ_API_KEY = "your-groq-key"  # Optional (faster, free tier)
GOOGLE_API_KEY = "your-google-key"
GOOGLE_SEARCH_ENGINE_ID = "your-cse-id"
```

### Customize Wake Word

Edit `config.py`:
```python
WAKE_WORD = "jarvis"  # Change to your preferred word
```

## Usage

### Desktop
1. Run `python jarvis_desktop.py`
2. Click "Start Listening" or press `Spacebar`
3. Say your command: "Jarvis, what's the weather?"
4. Jarvis responds with voice + text

### Android
1. Open Jarvis app
2. Tap microphone icon
3. Speak your command
4. Get instant response

## Available Commands

```
"Jarvis, search for [query]"
"Jarvis, what time is it?"
"Jarvis, tell me a joke"
"Jarvis, open [app name]"
"Jarvis, set reminder for [time]"
"Jarvis, weather in [city]"
"Jarvis, calculate [expression]"
```

## Project Structure

```
jarvis-ai-assistant/
├── jarvis_desktop.py          # Main desktop app
├── jarvis_core.py              # Core AI logic
├── voice_handler.py            # Speech recognition/synthesis
├── web_search.py               # Web search integration
├── automation.py               # Command automation
├── config.py                   # Configuration
├── requirements-desktop.txt    # Desktop dependencies
├── requirements-android.txt    # Android dependencies
├── buildozer.spec              # Android build config
├── android/
│   ├── main.py                # Android entry point
│   ├── buildozer.spec         # Build specification
│   └── buildozer.ini          # Build settings
├── .github/workflows/
│   └── build-apk.yml          # CI/CD for APK builds
└── docs/
    ├── SETUP.md               # Detailed setup guide
    ├── API.md                 # API documentation
    └── COMMANDS.md            # Command reference
```

## Architecture

```
┌─────────────┐
│  User Input │ (Voice/Text)
└──────┬──────┘
       │
┌──────▼──────────────┐
│ Voice Recognition   │ (speech_recognition)
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Intent Detection    │ (Jarvis Core)
└──────┬──────────────┘
       │
┌──────▼──────────────────────┐
│ Action Processing           │
├─ Web Search                 │
├─ AI Response (OpenAI/Groq)  │
├─ Local Automation           │
└──────┬──────────────────────┘
       │
┌──────▼──────────────┐
│ Text-to-Speech      │ (pyttsx3/gTTS)
└──────┬──────────────┘
       │
┌──────▼──────┐
│ User Output │ (Voice/UI)
└─────────────┘
```

## Dependencies

**Desktop:**
- PyQt5 - GUI framework
- SpeechRecognition - Voice input
- pyttsx3 - Text-to-speech
- openai/groq - AI models
- requests - Web requests
- google-api-client - Google Search

**Android:**
- Kivy - UI framework
- python-for-android - Build tool
- pyjnius - Android integration

## Performance

- **Response Time:** < 1 second (local commands)
- **AI Response:** 2-5 seconds (API calls)
- **Memory Usage:** ~200MB (Desktop), ~150MB (Android)
- **Battery Impact:** Minimal (only active during listening)

## Contributing

Contributions welcome! Fork and submit PRs.

## License

MIT License - See LICENSE file

## Troubleshooting

**Microphone not detected:**
```bash
python -m speech_recognition
```

**API errors:**
- Check API keys in `config.py`
- Verify internet connection
- Check API rate limits

**APK build fails:**
- Ensure Java 11 is installed
- Update buildozer: `pip install --upgrade buildozer`
- Check Android SDK installation

## Roadmap

- [ ] Offline AI model (Llama 2)
- [ ] Multi-language support
- [ ] Custom voice training
- [ ] Smart home integration
- [ ] Calendar/email integration
- [ ] iOS version
- [ ] Cloud sync
- [ ] Plugin system

---

**Made with ❤️ by Abishek**
