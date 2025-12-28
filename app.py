import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time
from google import genai
from google.api_core import exceptions

# 1. INITIALIZATION
st.set_page_config(page_title="PANOPTICON v6.3", page_icon="👁️", layout="wide")

try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    ALPHA_KEY = st.secrets["ALPHA_VANTAGE_KEY"]
    SYSTEM_READY = True
except:
    st.error("SECRET KEYS MISSING. CHECK CONFIG.")
    SYSTEM_READY = False

# 2. THE ENGINE
def fetch_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_KEY}'
    data = requests.get(url).json()
    if "Time Series (Daily)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df.index = pd.to_datetime(df.index)
        return df.astype(float).sort_index()
    return None

# 3. NAVIGATION UI
st.title("👁️ PANOPTICON COMMAND")
tab1, tab2, tab3 = st.tabs(["📡 MARKET OVERVIEW", "🔍 DEEP DIVE", "⚔️ COMPARISON"])

# --- TAB 1: HOME PAGE (NO MORE EMPTY SCREEN) ---
with tab1:
    st.subheader("Current Market Recon")
    cols = st.columns(3)
    quick_tickers = ["SPY", "QQQ", "BTC"] # Pre-loaded for the "First Look"
    
    for i, t in enumerate(quick_tickers):
        with cols[i]:
            st.metric(t, "SCANNING...", help="Click Deep Dive to analyze")
    
    st.info("💡 SYSTEM READY: Use the sidebar or tabs to begin tactical analysis.")
    st.image("https://images.unsplash.com/photo-1611974714014-419b1689260c?auto=format&fit=crop&q=80&w=1000", caption="Tactical Data Feed Online")

# --- TAB 2: DEEP DIVE (THE AI ANALYST) ---
with tab2:
    target = st.text_input("ENTER TARGET TICKER:", value="PLTR").upper()
    if st.button("RUN DEEP SCAN"):
        df = fetch_data(target)
        if df is not None:
            st.metric(f"{target} PRICE", f"${df['Close'].iloc[-1]:.2f}")
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            fig.update_layout(template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Logic (Simplified for brevity)
            st.subheader("🤖 AI INTEL")
            res = client.models.generate_content(model='gemini-2.0-flash-lite', contents=f"Quick risk check for {target}")
            st.write(res.text)

# --- TAB 3: COMPARISON (NEW FEATURE) ---
with tab3:
    st.subheader("Side-by-Side Tactical Comparison")
    colA, colB = st.columns(2)
    with colA: t1 = st.text_input("TICKER A:", "AAPL").upper()
    with colB: t2 = st.text_input("TICKER B:", "MSFT").upper()
    
    if st.button("EXECUTE COMPARISON"):
        d1, d2 = fetch_data(t1), fetch_data(t2)
        if d1 is not None and d2 is not None:
            # Normalized Chart (Growth %)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=d1.index, y=(d1['Close']/d1['Close'].iloc[0])*100, name=t1))
            fig.add_trace(go.Scatter(x=d2.index, y=(d2['Close']/d2['Close'].iloc[0])*100, name=t2))
            fig.update_layout(title="Relative Growth (Indexed to 100)", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Comparison
            prompt = f"Compare {t1} vs {t2}. Which has better 6-month momentum?"
            comp_res = client.models.generate_content(model='gemini-2.0-flash-lite', contents=prompt)
            st.write(comp_res.text)