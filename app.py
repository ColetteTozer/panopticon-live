import streamlit as st # THIS LINE IS THE FIX
import requests
import pandas as pd
import plotly.graph_objects as go
from google import genai

# 1. SETUP
st.set_page_config(page_title="PANOPTICON v6.0", page_icon="👁️", layout="wide")

# 2. THE NEW SDK BRAIN (V2.0 ARCHITECTURE)
try:
    # Use the new Client paradigm
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    ALPHA_KEY = st.secrets["ALPHA_VANTAGE_KEY"]
    SYSTEM_READY = True
except Exception as e:
    st.error(f"AUTH ERROR: {e}")
    SYSTEM_READY = False

# 3. INTERFACE
with st.sidebar:
    st.title("👁️ PANOPTICON")
    target = st.text_input("TARGET TICKER:", value="PLTR").upper()
    run_btn = st.button("EXECUTE SCAN")

if run_btn and SYSTEM_READY:
    # --- DATA FETCHING ---
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={target}&apikey={ALPHA_KEY}'
    r = requests.get(url)
    data = r.json()
    
    if "Time Series (Daily)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df.index = pd.to_datetime(df.index)
        df = df.astype(float).sort_index()
        
        current = df['Close'].iloc[-1]
        
        st.title(f"📂 DOSSIER: {target}")
        st.metric("PRICE", f"${current:.2f}")

        # --- THE NEW AI CALL (REFACTORED) ---
        st.divider()
        st.subheader("🤖 AI INTEL REPORT")
        
        # New stateless generate_content pattern
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Upgrade to the fastest 2025 model
            config=genai.types.GenerateContentConfig(
                system_instruction="You are PANOPTICON, a ruthless financial intel unit."
            ),
            contents=f"Analyze {target} at ${current}. 3-point risk assessment."
        )
        st.markdown(response.text)

        # Chart
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("API LIMIT: Your free Alpha Vantage key allows 25 calls/day.")
