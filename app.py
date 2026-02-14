"""
Real Estate AI Agent - Voice Conversation App
"""
import streamlit as st
import re
from datetime import datetime

# Import custom modules
from llm_client import LLMClient
from conversation_logger import ConversationLogger, format_conversation_for_display
from property_data import PROPERTIES
from appointment_agent import AppointmentAgent

# Page Configuration
st.set_page_config(
    page_title="Real Estate AI Agent",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .agent-msg { background: #E3F2FD; padding: 15px; border-radius: 15px; margin: 10px 0; border-left: 4px solid #1976D2; }
    .user-msg { background: #FFF3E0; padding: 15px; border-radius: 15px; margin: 10px 0; border-left: 4px solid #F57C00; }
    .stTextInput > div > div > input { font-size: 18px !important; padding: 15px !important; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'llm_client' not in st.session_state:
    st.session_state.llm_client = LLMClient()
if 'logger' not in st.session_state:
    st.session_state.logger = ConversationLogger()
    st.session_state.logger.start_session()
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'agent_spoke' not in st.session_state:
    st.session_state.agent_spoke = ""
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""
if 'appointment_agent' not in st.session_state:
    st.session_state.appointment_agent = AppointmentAgent()
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False
if 'selected_property' not in st.session_state:
    st.session_state.selected_property = None

# Sidebar
with st.sidebar:
    st.title("🏠 Real Estate Agent")
    st.markdown("---")
    st.markdown(st.session_state.llm_client.get_status())
    st.markdown("---")
    
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.user_info = {}
        st.session_state.agent_spoke = ""
        st.session_state.voice_text = ""
        st.session_state.logger = ConversationLogger()
        st.session_state.logger.start_session()
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Locations:** Dallas, Austin, Houston, San Antonio, Phoenix")
    
    # Show user info if collected
    if st.session_state.user_info:
        st.markdown("---")
        st.markdown("**Customer Info:**")
        for k, v in st.session_state.user_info.items():
            st.markdown(f"• {k}: {v}")

# Main header
st.markdown("## 🏠 Real Estate Voice Agent")

# Welcome message - Ask for user details
if not st.session_state.messages:
    welcome = """Hello! Welcome to Premium Real Estate Services. I'm your personal property advisor.

Before we begin, may I have your name please? And which city are you calling from?"""
    
    st.session_state.messages.append({
        "role": "assistant", 
        "content": welcome, 
        "time": datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.logger.log_agent_message(welcome)
    st.session_state.agent_spoke = ""

# Display conversation
st.markdown("### 💬 Conversation")
for msg in st.session_state.messages:
    ts = msg.get("time", "")
    if msg["role"] == "assistant":
        st.markdown(f'<div class="agent-msg"><b>🏠 Agent [{ts}]:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-msg"><b>👤 You [{ts}]:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# Speak last agent message
if st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant" and st.session_state.agent_spoke != last_msg["content"]:
        speak_text = last_msg["content"].replace('"', '').replace("'", "").replace('\n', ' ').replace('•', '').replace('**', '').replace('$', ' dollars ')
        
        speak_html = f"""
        <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var utterance = new SpeechSynthesisUtterance("{speak_text}");
                utterance.rate = 0.9;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;
                utterance.lang = 'en-US';
                window.speechSynthesis.speak(utterance);
            }}
        }})();
        </script>
        """
        st.components.v1.html(speak_html, height=0)
        st.session_state.agent_spoke = last_msg["content"]

st.markdown("---")

# Voice Input Section
st.markdown("### 🎤 Voice Input")
st.info("💡 **Tip:** Click microphone, speak, then PASTE (Ctrl+V) in the text box below and press Send")

voice_html = """
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px; color: white;">
    <button id="micBtn" onclick="toggleRec()" style="
        background: #28a745;
        color: white;
        border: none;
        padding: 25px 50px;
        border-radius: 50px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    ">🎤 CLICK TO SPEAK</button>
    
    <div id="liveText" style="margin-top: 20px; padding: 20px; background: rgba(255,255,255,0.2); border-radius: 10px; font-size: 22px; min-height: 60px;">
        Click the button and speak...
    </div>
    
    <div id="statusText" style="margin-top: 10px; font-size: 16px; color: #ffd54f;">
    </div>
</div>

<script>
var recognition = null;
var isRecording = false;
var transcript = '';
var silenceTimer = null;

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    
    recognition.onstart = function() {
        isRecording = true;
        document.getElementById('micBtn').innerHTML = '🔴 LISTENING...';
        document.getElementById('micBtn').style.background = '#dc3545';
        document.getElementById('liveText').innerHTML = '🎧 Speak now...';
        document.getElementById('statusText').innerHTML = '';
        transcript = '';
    };
    
    recognition.onresult = function(e) {
        transcript = '';
        for (var i = 0; i < e.results.length; i++) {
            transcript += e.results[i][0].transcript;
        }
        document.getElementById('liveText').innerHTML = '🗣️ "' + transcript + '"';
        
        // Auto-stop after 2 seconds of silence
        clearTimeout(silenceTimer);
        silenceTimer = setTimeout(function() {
            if (transcript.trim() && isRecording) {
                recognition.stop();
            }
        }, 2000);
    };
    
    recognition.onend = function() {
        isRecording = false;
        clearTimeout(silenceTimer);
        document.getElementById('micBtn').innerHTML = '🎤 CLICK TO SPEAK';
        document.getElementById('micBtn').style.background = '#28a745';
        
        if (transcript.trim()) {
            // Auto-copy to clipboard
            navigator.clipboard.writeText(transcript.trim()).then(function() {
                document.getElementById('liveText').innerHTML = '✅ "' + transcript + '"';
                document.getElementById('statusText').innerHTML = '📋 COPIED! Now paste (Ctrl+V) in the text box below and press Send';
            }).catch(function() {
                document.getElementById('liveText').innerHTML = '✅ "' + transcript + '"<br><br>⬇️ Copy this text manually and paste below';
            });
        } else {
            document.getElementById('liveText').innerHTML = 'No speech detected. Click and try again.';
        }
    };
    
    recognition.onerror = function(e) {
        isRecording = false;
        document.getElementById('liveText').innerHTML = '❌ Error: ' + e.error;
        document.getElementById('micBtn').innerHTML = '🎤 CLICK TO SPEAK';
        document.getElementById('micBtn').style.background = '#28a745';
    };
} else {
    document.getElementById('liveText').innerHTML = '⚠️ Voice not supported. Please use Chrome browser.';
}

function toggleRec() {
    if (!recognition) {
        alert('Voice recognition not supported. Please use Chrome browser.');
        return;
    }
    if (isRecording) {
        recognition.stop();
    } else {
        transcript = '';
        recognition.start();
    }
}
</script>
"""
st.components.v1.html(voice_html, height=220)

# Text input
st.markdown("### ⌨️ Type or Paste Your Message:")
with st.form("textform", clear_on_submit=True):
    text_input = st.text_input("", label_visibility="collapsed", placeholder="Type here or paste voice text (Ctrl+V)...")
    submitted = st.form_submit_button("📤 Send Message", use_container_width=True)

if submitted and text_input:
    user_time = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": text_input, "time": user_time})
    st.session_state.logger.log_user_message(text_input)
    
    print(f"\n<user>\n[{user_time}] USER: {text_input}\n</user>")
    
    # Get intent
    intent = st.session_state.llm_client.extract_intent(text_input)
    if intent:
        st.session_state.logger.log_intent(intent)
        if intent.get('location'):
            st.session_state.user_info['Location'] = intent.get('location')
        if intent.get('budget_max'):
            st.session_state.user_info['Budget'] = f"${intent.get('budget_max'):,}"
        if intent.get('property_type'):
            st.session_state.user_info['Property Type'] = intent.get('property_type')
    
    # Extract name from conversation
    text_lower = text_input.lower()
    if 'my name is' in text_lower or 'i am' in text_lower or "i'm" in text_lower:
        name_match = re.search(r'(?:my name is|i am|i\'m)\s+([a-zA-Z]+)', text_lower)
        if name_match:
            st.session_state.user_info['Name'] = name_match.group(1).title()
    
    # Extract email
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_input)
    if email_match:
        st.session_state.user_info['Email'] = email_match.group(0)
    
    # Check for site visit request and send emails
    site_visit_keywords = ['site visit', 'visit', 'schedule', 'book', 'appointment', 'see the property', 'view the property']
    is_site_visit = any(kw in text_lower for kw in site_visit_keywords)
    
    # Check for time preference
    visit_time = 'morning'
    if 'afternoon' in text_lower or 'evening' in text_lower:
        visit_time = 'afternoon'
    elif 'morning' in text_lower:
        visit_time = 'morning'
    
    # If site visit confirmed and we have customer info, send emails
    if is_site_visit and not st.session_state.email_sent:
        customer_info = {
            'name': st.session_state.user_info.get('Name', 'Valued Customer'),
            'email': st.session_state.user_info.get('Email', ''),
            'phone': st.session_state.user_info.get('Phone', 'Not provided')
        }
        
        # Get property info from selected or first matching
        property_info = st.session_state.selected_property or {
            'name': 'Downtown Dallas Apartment',
            'address': 'Downtown Dallas, TX',
            'price': st.session_state.user_info.get('Budget', '$1,500,000'),
            'type': st.session_state.user_info.get('Property Type', 'apartment')
        }
        
        if customer_info.get('email'):
            result = st.session_state.appointment_agent.schedule_site_visit(
                customer_info, property_info, visit_time
            )
            st.session_state.email_sent = True
            st.session_state.booking_ref = result.get('booking_ref', '')
            
            if result.get('customer_email_sent'):
                st.success(f"📧 Confirmation email sent to {customer_info['email']}!")
            if result.get('officer_email_sent'):
                st.success("📧 Field officer notified!")
    
    # Get LLM response
    chat_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    response = st.session_state.llm_client.chat(chat_msgs)
    
    agent_time = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "assistant", "content": response, "time": agent_time})
    st.session_state.logger.log_agent_message(response)
    st.session_state.agent_spoke = ""  # Reset to trigger speech
    
    print(f"\n<agcl>\n[{agent_time}] AGENT: {response}\n</agcl>")
    
    st.rerun()

# Conversation Log
st.markdown("---")
with st.expander("📝 View Conversation Log", expanded=False):
    log_text = ""
    for msg in st.session_state.messages:
        ts = msg.get("time", "")
        if msg["role"] == "user":
            log_text += f"<user>\n[{ts}] USER: {msg['content']}\n</user>\n\n"
        else:
            log_text += f"<agcl>\n[{ts}] AGENT: {msg['content']}\n</agcl>\n\n"
    
    if log_text:
        st.code(log_text, language="xml")
    
    # Download button
    if st.session_state.messages:
        st.download_button(
            "📥 Download Conversation",
            data=format_conversation_for_display(st.session_state.messages),
            file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

st.caption("🏠 Real Estate AI Agent | Voice: Speak → Copy → Paste → Send")
