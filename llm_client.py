"""LLM integration module - Groq (primary) + Ollama (fallback)"""
import json
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, OLLAMA_HOST, OLLAMA_MODEL, SYSTEM_PROMPT, INTENT_EXTRACTION_PROMPT
from property_data import get_properties_summary

class LLMClient:
    def __init__(self):
        self.groq_client = None
        self.ollama_available = False
        self.using_groq = False
        
        # Try to initialize Groq
        if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
            try:
                self.groq_client = Groq(api_key=GROQ_API_KEY)
                self.using_groq = True
                print("✓ Groq API initialized successfully")
            except Exception as e:
                print(f"✗ Groq initialization failed: {e}")
        
        # Check Ollama availability as fallback
        if not self.using_groq:
            try:
                import ollama
                self.ollama_available = True
                print("✓ Ollama fallback available")
            except:
                print("✗ Ollama not available")
    
    def get_system_prompt(self):
        """Get the system prompt with property data"""
        property_summary = get_properties_summary()
        return SYSTEM_PROMPT.format(property_data=property_summary)
    
    def chat(self, messages: list) -> str:
        """Send messages to LLM and get response"""
        # Prepare messages with system prompt
        full_messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ] + messages
        
        if self.using_groq and self.groq_client:
            return self._chat_groq(full_messages)
        elif self.ollama_available:
            return self._chat_ollama(full_messages)
        else:
            return "I apologize, but I'm having trouble connecting to my backend services. Please check your API configuration."
    
    def _chat_groq(self, messages: list) -> str:
        """Chat using Groq API"""
        try:
            response = self.groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq API error: {e}")
            if self.ollama_available:
                return self._chat_ollama(messages)
            return f"I'm experiencing some technical difficulties. Error: {str(e)}"
    
    def _chat_ollama(self, messages: list) -> str:
        """Chat using Ollama (fallback)"""
        try:
            import ollama
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            return f"I'm experiencing some technical difficulties with our backup system. Error: {str(e)}"
    
    def extract_intent(self, user_message: str) -> dict:
        """Extract structured intent from user message"""
        prompt = INTENT_EXTRACTION_PROMPT.format(user_message=user_message)
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            if self.using_groq and self.groq_client:
                response = self.groq_client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=messages,
                    temperature=0,
                    max_tokens=200
                )
                result = response.choices[0].message.content
            elif self.ollama_available:
                import ollama
                response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
                result = response['message']['content']
            else:
                return {}
            
            # Parse JSON from response
            result = result.strip()
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
            
            return json.loads(result)
        except Exception as e:
            print(f"Intent extraction error: {e}")
            return {}
    
    def get_status(self) -> str:
        """Get current LLM connection status"""
        if self.using_groq:
            return f"🟢 Connected to Groq ({GROQ_MODEL})"
        elif self.ollama_available:
            return f"🟡 Using Ollama fallback ({OLLAMA_MODEL})"
        else:
            return "🔴 No LLM backend available"
