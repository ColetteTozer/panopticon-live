# app.py (PANOPTICON v5.3 - ALPHA VANTAGE EDITION)
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="PANOPTICON v5.3", page_icon="👁️", layout="wide")

# 2. AUTHENTICATION
try:
    ALPHA_KEY = st.secrets["ALPHA_VANTAGE_KEY"]
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    SYSTEM_READY = True
except Exception as e:
    st.error(f"AUTH ERROR: {e}")
    SYSTEM_READY = False

# 3. ALPHA VANTAGE ENGINE
def fetch_alpha_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_KEY}'
    r = requests.get(url)
    data = r.json()
    
    if "Time Series (Daily)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df.index = pd.to_datetime(df.index)
        df = df.astype(float).sort_index()
        return df
    else:
        st.warning(f"LIMIT REACHED: {data.get('Note', 'Check API Key')}")
        return None

# 4. INTERFACE
with st.sidebar:
    st.title("👁️ PANOPTICON")
    target = st.text_input("TARGET TICKER:", value="PLTR").upper()
    run_btn = st.button("EXECUTE SCAN") # Only calls API when clicked

if run_btn and SYSTEM_READY:
    with st.spinner("INFILTRATING MARKET DATA..."):
        hist = fetch_alpha_data(target)
        
        if hist is not None:
            # Metrics
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            change = ((current - prev) / prev) * 100
            
            st.title(f"📂 DOSSIER: {target}")
            st.metric("PRICE", f"${current:.2f}", f"{change:.2f}%")

            # Pro Chart
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(template="plotly_dark", height=500, margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)

            # AI Analyst (Remains the same, uses the data we just fetched)
            st.divider()
            st.subheader("🤖 AI INTEL REPORT")
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            prompt = f"Analyze {target}. Current price is {current}. Previous close was {prev}. Give a 3-point ruthless risk assessment."
            response = model.generate_content(prompt)
            st.markdown(response.text)