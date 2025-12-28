# app.py (PANOPTICON v5.0 - THE SENTIENT ENGINE)
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import google.generativeai as genai

# 1. SETUP & AUTH
st.set_page_config(page_title="PANOPTICON v5.0", page_icon="👁️", layout="wide")

# Try to load API Key from Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    AI_STATUS = "ONLINE"
except:
    AI_STATUS = "OFFLINE (MISSING KEY)"

# 2. THE PERSONA (THE "DOC SIMPLE" FOR FINANCE)
SYSTEM_PROMPT = """
You are PANOPTICON, an elite OSINT Financial Intelligence Unit.
Your Directive: Provide ruthless, data-backed analysis.
Tone: Cold, professional, military-grade precision.
Rules:
1. NEVER give generic "financial advice." Give "Intel."
2. Focus on "Asymmetric Risk" (What could go wrong?).
3. If the data is bad, say it is TOXIC. Do not sugarcoat.
4. Use formatting (Bullet points, bold text) to make it readable.
"""

# 3. SIDEBAR & INPUTS
with st.sidebar:
    st.title("👁️ CONTROLS")
    target = st.text_input("TARGET:", value="PLTR").upper()
    rival = st.text_input("RIVAL:", value="NVDA").upper()
    st.divider()
    st.caption(f"🧠 CORTEX: {AI_STATUS}")

# 4. DATA ENGINE
if target:
    stock = yf.Ticker(target)
    info = stock.info
    hist = stock.history(period="6mo")
    
    # Header
    current = info.get('currentPrice', 0)
    st.title(f"📂 DOSSIER: {target}")
    st.metric("PRICE", f"${current}")

    # --- SECTOR A: VISUALS ---
    st.subheader("📊 VISUAL INTELLIGENCE")
    fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
    fig.update_layout(height=400, template="plotly_dark", margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

    # --- SECTOR B: THE BRAIN (CHAT) ---
    st.divider()
    st.subheader("🤖 PANOPTICON AI ANALYST")
    
    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input(f"QUERY THE INTEL ON {target}..."):
        # 1. User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. AI Response
        if AI_STATUS == "ONLINE":
            with st.chat_message("assistant"):
                with st.spinner("TRIANGULATING DATA..."):
                    # We feed the AI the live data so it's not "Dumb"
                    context = f"CONTEXT: Analysis of {target}. Price: ${current}. Market Cap: {info.get('marketCap')}."
                    full_prompt = f"{SYSTEM_PROMPT}\n\n{context}\n\nUSER QUERY: {prompt}"
                    
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(full_prompt)
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
        else:
            st.error("SYSTEM ALERT: API KEY MISSING IN SECRETS.")