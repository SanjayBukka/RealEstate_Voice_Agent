"""Conversation logger for Real Estate AI Agent - separates agent and user messages"""
import os
from datetime import datetime
from config import CONVERSATION_LOG_FILE

class ConversationLogger:
    def __init__(self, log_file=None):
        self.log_file = log_file or CONVERSATION_LOG_FILE
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def _ensure_file_exists(self):
        """Create log file if it doesn't exist"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("REAL ESTATE AI AGENT - CONVERSATION LOGS\n")
                f.write("=" * 80 + "\n\n")
    
    def start_session(self):
        """Log the start of a new conversation session"""
        self._ensure_file_exists()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"SESSION: {self.session_id}\n")
            f.write(f"STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
    
    def log_agent_message(self, message: str):
        """Log an agent message with <agcl> tag"""
        self._ensure_file_exists()
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"<agcl>\n")
            f.write(f"[{timestamp}] AGENT:\n")
            f.write(f"{message}\n")
            f.write(f"</agcl>\n\n")
    
    def log_user_message(self, message: str):
        """Log a user message with <user> tag"""
        self._ensure_file_exists()
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"<user>\n")
            f.write(f"[{timestamp}] USER:\n")
            f.write(f"{message}\n")
            f.write(f"</user>\n\n")
    
    def log_intent(self, intent_data: dict):
        """Log extracted intent data"""
        self._ensure_file_exists()
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"<intent>\n")
            f.write(f"[{timestamp}] EXTRACTED INTENT:\n")
            for key, value in intent_data.items():
                if value:
                    f.write(f"  - {key}: {value}\n")
            f.write(f"</intent>\n\n")
    
    def end_session(self):
        """Log the end of a conversation session"""
        self._ensure_file_exists()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("-" * 80 + "\n")
            f.write(f"SESSION ENDED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 80 + "\n\n")
    
    def get_full_conversation(self):
        """Read and return the full conversation log"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""


def format_conversation_for_display(messages: list) -> str:
    """Format messages list for display with proper tags"""
    formatted = []
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        
        if role == "assistant":
            formatted.append(f"<agcl>\nAGENT: {content}\n</agcl>")
        elif role == "user":
            formatted.append(f"<user>\nUSER: {content}\n</user>")
    
    return "\n\n".join(formatted)
