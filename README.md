# 🏠 Real Estate AI Agent

A voice-enabled AI customer support agent for US residential real estate, built with Streamlit and Groq API.

## ✨ Features

- **🎤 Voice Interaction**: Speak naturally using browser's Web Speech API
- **🤖 Fast AI Responses**: Powered by Groq API (sub-second responses)
- **🏘️ Property Search**: Filter by location, budget, and property type
- **📝 Conversation Logging**: All conversations saved with `<agcl>` and `<user>` tags
- **🔄 Fallback Support**: Ollama for offline operation

## 🗂️ Project Structure

```
RealStateAgent/
├── app.py                  # Main Streamlit application
├── config.py               # Configuration settings
├── llm_client.py           # Groq + Ollama LLM integration
├── property_data.py        # Sample property database
├── conversation_logger.py  # Conversation logging with tags
├── requirements.txt        # Python dependencies
├── .env                    # API keys (create from .env.example)
├── .env.example            # Example environment file
└── conversations.txt       # Auto-generated conversation logs
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Groq API Key (Free)

1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up for free
3. Create an API key
4. Copy your key

### 3. Configure API Key

Edit `.env` file and add your key:

```
GROQ_API_KEY=your_actual_api_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

python twilio_call.py +91XXXXXXXX47{to run voce agent that calls to you on your mobile}

The app will open in your browser at `http://localhost:8501`

## 🎤 Using Voice Features

1. **Enable Voice**: Make sure "Enable Voice" is checked in the sidebar
2. **Click to Speak**: Press the microphone button and speak your request
3. **Auto-Response**: The agent will speak its response back to you

**Note**: Voice features require Google Chrome for best compatibility.

## 📝 Conversation Log Format

Conversations are saved in `conversations.txt` with the following format:

```
<agcl>
[10:30:45] AGENT:
Hello! How can I help you find your perfect property today?
</agcl>

<user>
[10:30:52] USER:
I want a plot under $400k in Dallas
</user>

<intent>
[10:30:52] EXTRACTED INTENT:
  - intent: buy
  - location: Dallas
  - budget_max: 400000
  - property_type: plot
</intent>
```

## 🏘️ Available Properties

The agent has access to properties in:
- **Dallas**: plots, houses, apartments
- **Austin**: plots, houses, villas
- **Houston**: plots, houses, apartments
- **San Antonio**: plots, houses
- **Phoenix**: plots, villas

## 🔧 Offline Fallback (Ollama)

If Groq is unavailable, the app can use Ollama as a fallback:

1. Install Ollama: [https://ollama.ai/](https://ollama.ai/)
2. Pull Llama 3: `ollama pull llama3`
3. The app will automatically detect and use Ollama

## 🎯 Example Conversations

**User**: "I'm looking for a house in Austin under $650k"

**Agent**: "Great choice! Austin has excellent properties. I found a 4-bedroom, 3-bath house in Cedar Park for $620,000 with smart home features, solar panels, and a large backyard. Would you like to schedule a site visit or speak with one of our agents?"

---

**User**: "Show me plots in Dallas"

**Agent**: "I'd be happy to help! We have two plots available in Dallas:
1. North Dallas - $350,000 (0.5 acres, corner lot, near schools)
2. Frisco - $420,000 (0.75 acres, lake view, gated community)

What's your budget range? This will help me narrow down the best option for you."

## 📊 Architecture

```
Browser Mic → Web Speech API → Text → Groq LLM → Text → Speech Synthesis API → Voice Reply
```

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **LLM**: Groq API (llama3-70b)
- **Fallback**: Ollama + Llama 3
- **Speech-to-Text**: Browser Web Speech API
- **Text-to-Speech**: Browser Speech Synthesis API

## 📄 License

MIT License - Feel free to use for hackathons and projects!
