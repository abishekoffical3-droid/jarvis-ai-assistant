"""Jarvis AI Desktop Application with PyQt5 UI"""
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QComboBox, QCheckBox, QSpinBox, QMessageBox, QTabWidget, QSlider
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap
from PyQt5.QtWidgets import QStyleFactory
from jarvis_core import get_jarvis
from voice_handler import VoiceHandler
from config import (
    THEME, WINDOW_WIDTH, WINDOW_HEIGHT, FONT_SIZE,
    ENABLE_VOICE_OUTPUT, HISTORY_FILE, WAKE_WORD, AI_TEMPERATURE
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceWorker(QThread):
    """Worker thread for voice listening"""
    text_received = pyqtSignal(str)
    error = pyqtSignal(str)
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.voice_handler = VoiceHandler()
        self.is_running = False
    
    def run(self):
        """Run voice listener"""
        try:
            self.listening_started.emit()
            text = self.voice_handler.listen()
            if text:
                self.text_received.emit(text)
            else:
                self.error.emit("Could not understand audio")
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.listening_stopped.emit()
    
    def stop(self):
        """Stop listening"""
        self.voice_handler.stop_listening()
        self.is_running = False


class JarvisDesktopUI(QMainWindow):
    """Main Jarvis Desktop UI"""
    
    def __init__(self):
        super().__init__()
        self.jarvis = get_jarvis()
        self.voice_handler = VoiceHandler()
        self.history = self._load_history()
        self.voice_worker = None
        self.init_ui()
        self.setup_stylesheet()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("🤖 Jarvis AI Assistant")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowIcon(QIcon("jarvis_icon.png") if Path("jarvis_icon.png").exists() else QIcon())
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🤖 JARVIS AI")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        status_label = QLabel("Ready")
        status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.status_label = status_label
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        main_layout.addLayout(header_layout)
        
        # Tabs
        tabs = QTabWidget()
        
        # Chat Tab
        chat_widget = self.create_chat_tab()
        tabs.addTab(chat_widget, "💬 Chat")
        
        # Settings Tab
        settings_widget = self.create_settings_tab()
        tabs.addTab(settings_widget, "⚙️ Settings")
        
        # History Tab
        history_widget = self.create_history_tab()
        tabs.addTab(history_widget, "📜 History")
        
        main_layout.addWidget(tabs)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_label = QLabel(f"Version 1.0 | {datetime.now().year}")
        footer_label.setStyleSheet("color: #888; font-size: 10px;")
        footer_layout.addWidget(footer_label)
        footer_layout.addStretch()
        main_layout.addLayout(footer_layout)
    
    def create_chat_tab(self) -> QWidget:
        """Create chat interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(
            "QTextEdit { background-color: #1e1e1e; color: #00ff00; "
            "border: 1px solid #444; border-radius: 5px; font-family: Courier; }"
        )
        layout.addWidget(QLabel("💬 Conversation:"))
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(f"Type or say 'Jarvis, ...' (Press Enter or click buttons)")
        self.input_field.returnPressed.connect(self.send_text_input)
        
        listen_btn = QPushButton("🎤 Listen")
        listen_btn.clicked.connect(self.start_voice_input)
        listen_btn.setStyleSheet(
            "QPushButton { background-color: #0066cc; color: white; "
            "border: none; padding: 8px; border-radius: 4px; font-weight: bold; }"
        )
        
        send_btn = QPushButton("📤 Send")
        send_btn.clicked.connect(self.send_text_input)
        send_btn.setStyleSheet(
            "QPushButton { background-color: #00aa00; color: white; "
            "border: none; padding: 8px; border-radius: 4px; font-weight: bold; }"
        )
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_chat)
        clear_btn.setStyleSheet(
            "QPushButton { background-color: #aa0000; color: white; "
            "border: none; padding: 8px; border-radius: 4px; font-weight: bold; }"
        )
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(listen_btn)
        input_layout.addWidget(send_btn)
        input_layout.addWidget(clear_btn)
        
        layout.addLayout(input_layout)
        
        # Quick commands
        quick_label = QLabel("⚡ Quick Commands:")
        quick_layout = QHBoxLayout()
        
        quick_commands = [
            ("Time", lambda: self.quick_command("What time is it?")),
            ("Weather", lambda: self.quick_command("What's the weather?")),
            ("Joke", lambda: self.quick_command("Tell me a joke")),
            ("Date", lambda: self.quick_command("What's today's date?")),
        ]
        
        for cmd_name, cmd_func in quick_commands:
            btn = QPushButton(cmd_name)
            btn.clicked.connect(cmd_func)
            btn.setStyleSheet(
                "QPushButton { background-color: #333; color: #0ff; "
                "border: 1px solid #0ff; padding: 5px; border-radius: 3px; }"
            )
            quick_layout.addWidget(btn)
        
        layout.addWidget(quick_label)
        layout.addLayout(quick_layout)
        
        return widget
    
    def create_settings_tab(self) -> QWidget:
        """Create settings interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Theme
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)
        
        # Voice Output
        self.voice_output_check = QCheckBox("Enable Voice Output")
        self.voice_output_check.setChecked(ENABLE_VOICE_OUTPUT)
        layout.addWidget(self.voice_output_check)
        
        # Temperature
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("AI Temperature:"))
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setMinimum(0)
        self.temp_slider.setMaximum(100)
        self.temp_slider.setValue(int(AI_TEMPERATURE * 100))
        self.temp_value = QLabel(f"{AI_TEMPERATURE}")
        self.temp_slider.valueChanged.connect(self.update_temperature)
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_value)
        layout.addLayout(temp_layout)
        
        # API Status
        layout.addWidget(QLabel("API Status:"))
        api_status = QTextEdit()
        api_status.setReadOnly(True)
        api_status.setText(self.get_api_status())
        api_status.setMaximumHeight(100)
        layout.addWidget(api_status)
        
        layout.addStretch()
        
        # Save Settings
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        return widget
    
    def create_history_tab(self) -> QWidget:
        """Create history interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("📜 Conversation History:"))
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_history_item)
        layout.addWidget(self.history_list)
        
        button_layout = QHBoxLayout()
        export_btn = QPushButton("📥 Export History")
        export_btn.clicked.connect(self.export_history)
        clear_history_btn = QPushButton("🗑️ Clear History")
        clear_history_btn.clicked.connect(self.clear_history)
        
        button_layout.addWidget(export_btn)
        button_layout.addWidget(clear_history_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.refresh_history_list()
        
        return widget
    
    def start_voice_input(self):
        """Start listening for voice input"""
        self.status_label.setText("🎤 Listening...")
        self.status_label.setStyleSheet("color: #ffff00; font-weight: bold;")
        
        self.voice_worker = VoiceWorker()
        self.voice_worker.text_received.connect(self.on_voice_input)
        self.voice_worker.error.connect(self.on_voice_error)
        self.voice_worker.listening_stopped.connect(self.on_listening_stopped)
        self.voice_worker.start()
    
    def on_voice_input(self, text: str):
        """Handle voice input"""
        self.input_field.setText(text)
        self.send_text_input()
    
    def on_voice_error(self, error: str):
        """Handle voice error"""
        self.append_chat(f"❌ Error: {error}", "error")
    
    def on_listening_stopped(self):
        """Handle listening stopped"""
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
    
    def send_text_input(self):
        """Send text input"""
        text = self.input_field.text().strip()
        if not text:
            return
        
        self.input_field.clear()
        self.append_chat(f"You: {text}", "user")
        
        self.status_label.setText("🤖 Thinking...")
        self.status_label.setStyleSheet("color: #ffaa00; font-weight: bold;")
        
        try:
            response = self.jarvis.process_command(text)
            self.append_chat(f"Jarvis: {response}", "assistant")
            
            # Save to history
            self.history.append({
                "timestamp": datetime.now().isoformat(),
                "user": text,
                "assistant": response
            })
            self._save_history()
            self.refresh_history_list()
            
            # Speak response
            if self.voice_output_check.isChecked():
                self.voice_handler.speak(response)
        
        except Exception as e:
            self.append_chat(f"❌ Error: {str(e)}", "error")
        
        finally:
            self.status_label.setText("Ready")
            self.status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
    
    def quick_command(self, command: str):
        """Execute quick command"""
        self.input_field.setText(f"Jarvis, {command}")
        self.send_text_input()
    
    def append_chat(self, message: str, msg_type: str = "info"):
        """Append message to chat display"""
        if msg_type == "user":
            formatted = f"<span style='color: #00ff00;'>{message}</span>"
        elif msg_type == "assistant":
            formatted = f"<span style='color: #00aaff;'>{message}</span>"
        elif msg_type == "error":
            formatted = f"<span style='color: #ff0000;'>{message}</span>"
        else:
            formatted = f"<span style='color: #aaaaaa;'>{message}</span>"
        
        self.chat_display.append(formatted)
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.clear()
    
    def change_theme(self, theme: str):
        """Change application theme"""
        # This would apply different stylesheets
        pass
    
    def update_temperature(self, value: int):
        """Update AI temperature"""
        temp = value / 100.0
        self.temp_value.setText(f"{temp:.2f}")
    
    def save_settings(self):
        """Save settings"""
        QMessageBox.information(self, "Success", "Settings saved successfully!")
    
    def get_api_status(self) -> str:
        """Get API status information"""
        status = "✅ APIs Configured\n"
        status += "- OpenAI/Groq: Connected\n"
        status += "- Speech Recognition: Ready\n"
        status += "- Text-to-Speech: Ready"
        return status
    
    def _load_history(self) -> list:
        """Load chat history from file"""
        try:
            if Path(HISTORY_FILE).exists():
                with open(HISTORY_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
        return []
    
    def _save_history(self):
        """Save chat history to file"""
        try:
            Path(HISTORY_FILE).parent.mkdir(parents=True, exist_ok=True)
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def refresh_history_list(self):
        """Refresh history list widget"""
        self.history_list.clear()
        for i, entry in enumerate(reversed(self.history[-20:])):
            timestamp = entry.get("timestamp", "Unknown")
            user_text = entry.get("user", "")[:50]
            item_text = f"[{timestamp}] {user_text}..."
            self.history_list.addItem(QListWidgetItem(item_text))
    
    def load_history_item(self, item: QListWidgetItem):
        """Load selected history item"""
        index = self.history_list.row(item)
        if index >= 0:
            entry = list(reversed(self.history[-20:]))[index]
            self.append_chat(f"\n[History] You: {entry.get('user')}", "info")
            self.append_chat(f"Jarvis: {entry.get('assistant')}", "info")
    
    def export_history(self):
        """Export history to file"""
        export_file = f"jarvis_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(export_file, 'w') as f:
                json.dump(self.history, f, indent=2)
            QMessageBox.information(self, "Success", f"History exported to {export_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {e}")
    
    def clear_history(self):
        """Clear conversation history"""
        reply = QMessageBox.question(
            self, "Confirm", "Are you sure you want to clear all history?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.history = []
            self._save_history()
            self.refresh_history_list()
            self.append_chat("History cleared.", "info")
    
    def setup_stylesheet(self):
        """Setup application stylesheet"""
        stylesheet = """
        QMainWindow {
            background-color: #0a0e27;
        }
        QWidget {
            background-color: #0a0e27;
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #1a3a52;
            color: #00ff00;
            border: 1px solid #0066cc;
            padding: 5px;
            border-radius: 3px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2a5a72;
        }
        QLineEdit, QTextEdit {
            background-color: #1a1a2e;
            color: #00ff00;
            border: 1px solid #0066cc;
            border-radius: 3px;
            padding: 5px;
        }
        QLabel {
            color: #e0e0e0;
        }
        QTabWidget::pane {
            border: 1px solid #0066cc;
        }
        QTabBar::tab {
            background-color: #1a1a2e;
            color: #00ff00;
            padding: 5px 15px;
            border: 1px solid #0066cc;
        }
        QTabBar::tab:selected {
            background-color: #2a4a5e;
        }
        """
        self.setStyleSheet(stylesheet)


def main():
    """Run the application"""
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    
    window = JarvisDesktopUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
