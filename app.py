# app.py (PANOPTICON v5.1 - API REPAIR)
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import google.generativeai as genai

# 1. SETUP & AUTH
st.set_page_config(page_title="PANOPTICON v5.1", page_icon="👁️", layout="wide")

# Try to load API Key from Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    AI_STATUS = "ONLINE"
except Exception as e:
    AI_STATUS = f"OFFLINE ({e})"

# 2. THE PERSONA (THE "BRAIN" RULES)
SYSTEM_PROMPT = """
IDENTITY:
You are PANOPTICON, an elite Financial Intelligence Unit.
* Persona: Cold, professional, ruthless, and data-driven.
* Voice: You provide 'Intel', not 'Advice'. You are cynical of market hype.

PRIME DIRECTIVES:
1. FOCUS ON RISK: Highlight what the herd is missing.
2. NO SUGARCOATING: If a stock is overvalued, call it 'Toxic'.
3. FORMATTING: Use bold headers and bullet points for speed of reading.
"""

# 3. SIDEBAR
with st.sidebar:
    st.title("👁️ CONTROLS")
    target = st.text_input("PRIMARY TARGET:", value="PLTR").upper()
    st.divider()
    st.caption(f"🧠 CORTEX: {AI_STATUS}")

# 4. MAIN INTERFACE
if target:
    try:
        stock = yf.Ticker(target)
        info = stock.info
        hist = stock.history(period="6mo")
        current_price = info.get('currentPrice', 0)

        # Header
        st.title(f"📂 DOSSIER: {target}")
        st.metric("LIVE PRICE", f"${current_price}")

        # Visuals
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

        # AI CHAT SECTOR
        st.divider()
        st.subheader("🤖 PANOPTICON AI ANALYST")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("QUERY THE INTEL..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            if AI_STATUS == "ONLINE":
                with st.chat_message("assistant"):
                    # FIX: Use 'gemini-1.5-flash-latest' and inject Persona
                    model = genai.GenerativeModel(
                        model_name='gemini-1.5-flash-latest',
                        system_instruction=SYSTEM_PROMPT
                    )
                    
                    # Provide live context so it isn't "dumb"
                    context = f"The user is looking at {target}. Current price is ${current_price}."
                    
                    response = model.generate_content(f"{context}\n\nUSER QUERY: {prompt}")
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("API CONNECTION FAILED. CHECK SECRETS.")

    except Exception as e:
        st.error(f"SYSTEM FAILURE: {e}")