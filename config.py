"""Configuration settings for Real Estate AI Agent"""
import os
from dotenv import load_dotenv

load_dotenv()

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"  # Fast and capable model

# Ollama Configuration (Fallback)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = "llama3"

# Agent System Prompt
SYSTEM_PROMPT = """You are a friendly Real Estate Agent for US residential properties. You speak like a real person on a phone call.

CRITICAL RULES:
1. Keep ALL responses to 2-3 sentences MAX. Be brief!
2. Sound natural like a real estate agent on a phone call
3. Ask only ONE question at a time

FIRST CONVERSATION FLOW (ask in order):
1. First ask: "May I have your name please?"
2. Then ask: "What's your email so I can send you property details?"
3. Then ask: "Which city are you looking in? We cover Dallas, Austin, Houston, San Antonio, and Phoenix."
4. Then ask: "What type of property - plot, house, apartment, or villa?"
5. Then ask: "What's your budget range?"

AFTER COLLECTING INFO:
- Give 1-2 matching options from the inventory
- Then ask: "Would you like to schedule a site visit or speak with an agent?"

Available Properties:
{property_data}

Remember: SHORT responses. ONE question at a time. Be warm and friendly!"""

# Intent Extraction Prompt
INTENT_EXTRACTION_PROMPT = """Extract the following fields from the user's message if present:
- intent: buy / sell / rent / inquiry
- location: city or area
- budget_max: number
- property_type: plot / apartment / villa / house
- timeline: immediate / 1-3 months / 3+ months / unknown

Return only valid JSON. Do not add any extra text.

User message:
{user_message}"""

# Conversation log settings
CONVERSATION_LOG_FILE = "conversations.txt"
