"""Automation and system commands"""
import os
import platform
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)

SYSTEM = platform.system()


class Automation:
    """Handle system automation and commands"""
    
    @staticmethod
    def open_application(app_name: str) -> bool:
        """Open an application"""
        try:
            if SYSTEM == "Windows":
                os.startfile(app_name)
            elif SYSTEM == "Darwin":  # macOS
                subprocess.run(["open", "-a", app_name])
            elif SYSTEM == "Linux":
                subprocess.Popen([app_name])
            logger.info(f"Opened {app_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return False
    
    @staticmethod
    def open_url(url: str) -> bool:
        """Open a URL in default browser"""
        try:
            if SYSTEM == "Windows":
                os.startfile(url)
            elif SYSTEM == "Darwin":
                subprocess.run(["open", url])
            elif SYSTEM == "Linux":
                subprocess.run(["xdg-open", url])
            logger.info(f"Opened URL: {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to open URL: {e}")
            return False
    
    @staticmethod
    def execute_command(command: str) -> Optional[str]:
        """Execute system command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return None
    
    @staticmethod
    def get_system_info() -> dict:
        """Get system information"""
        return {
            "system": SYSTEM,
            "python_version": platform.python_version(),
            "machine": platform.machine(),
        }
    
    @staticmethod
    def shutdown(delay: int = 0):
        """Shutdown system"""
        try:
            if SYSTEM == "Windows":
                os.system(f"shutdown /s /t {delay}")
            else:
                os.system(f"sudo shutdown -h +{delay // 60}")
        except Exception as e:
            logger.error(f"Shutdown error: {e}")
    
    @staticmethod
    def restart(delay: int = 0):
        """Restart system"""
        try:
            if SYSTEM == "Windows":
                os.system(f"shutdown /r /t {delay}")
            else:
                os.system(f"sudo shutdown -r +{delay // 60}")
        except Exception as e:
            logger.error(f"Restart error: {e}")
