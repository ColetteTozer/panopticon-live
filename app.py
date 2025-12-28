# app.py (PANOPTICON v4.0 - VISUAL INTELLIGENCE)
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="PANOPTICON v4.0", page_icon="👁️", layout="wide")

# Custom CSS for "Terminal" feel
st.markdown("""
<style>
    .stApp {background-color: #0e1117;}
    .metric-card {background-color: #1a1c24; padding: 20px; border-radius: 10px; border: 1px solid #333;}
    h1, h2, h3 {color: #00ff41 !important; font-family: 'Courier New', monospace;}
    div[data-testid="stMetricValue"] {color: #00ff41;}
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR CONTROL
with st.sidebar:
    st.title("👁️ CONTROLS")
    target = st.text_input("TARGET ASSET:", value="PLTR").upper()
    timeframe = st.selectbox("TIMEFRAME:", ["1mo", "3mo", "6mo", "1y", "5y", "max"])
    st.divider()
    st.markdown("### SYSTEM STATUS")
    st.caption("✅ NETWORK: SECURE")
    st.caption("✅ MODE: ACTIVE_HUNTER")

# 3. MAIN ENGINE
if target:
    try:
        # Fetch Data
        stock = yf.Ticker(target)
        hist = stock.history(period=timeframe)
        info = stock.info
        
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title(f"📂 DOSSIER: {info.get('shortName', target)}")
        with col2:
            current_price = info.get('currentPrice', hist['Close'].iloc[-1])
            prev_close = info.get('previousClose', hist['Close'].iloc[-2])
            delta = ((current_price - prev_close)/prev_close)*100
            st.metric("LIVE PRICE", f"${current_price:.2f}", f"{delta:.2f}%")

        # --- SECTOR A: CHART INTELLIGENCE ---
        st.divider()
        st.subheader("📊 SECTOR A: PRICE ACTION")
        
        # Interactive Candle Chart
        fig = go.Figure(data=[go.Candlestick(x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'])])
        fig.update_layout(xaxis_rangeslider_visible=False, height=500, 
                          template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

        # --- SECTOR B: FUNDAMENTAL RADAR ---
        st.divider()
        st.subheader("📡 SECTOR B: FUNDAMENTAL METRICS")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("MARKET CAP", f"${info.get('marketCap', 0)/1e9:.2f}B")
        m1.caption("Total Value")
        
        pe = info.get('trailingPE', 'N/A')
        m2.metric("P/E RATIO", f"{pe}")
        m2.caption("Valuation Heat")
        
        vol = info.get('volume', 0)
        m3.metric("VOLUME", f"{vol:,}")
        m3.caption("Liquidity")
        
        high52 = info.get('fiftyTwoWeekHigh', 0)
        m4.metric("52W HIGH", f"${high52}")
        m4.caption("Resistance Level")

        # --- SECTOR C: NEWS WIRE (THE NARRATIVE) ---
        st.divider()
        st.subheader("📰 SECTOR C: THE NARRATIVE STREAM")
        
        news_items = stock.news
        if news_items:
            for item in news_items[:3]: # Show top 3
                with st.expander(f"🚨 {item['title']}"):
                    st.write(f"**PUBLISHER:** {item['publisher']}")
                    st.write(f"**LINK:** [Read Source]({item['link']})")
        else:
            st.write("NO SIGNAL DETECTED ON NEWS WIRE.")

        # --- SECTOR D: GENERATE REPORT (PDF SIMULATION) ---
        st.divider()
        
        # Prepare text for export
        report_text = f"""
        PANOPTICON INTELLIGENCE BRIEF
        -----------------------------
        TARGET: {target}
        DATE: {datetime.now().strftime('%Y-%m-%d')}
        PRICE: ${current_price}
        TREND: {delta:.2f}%
        
        VERDICT:
        Asset is currently trading at ${current_price}. 
        Market Capitalization stands at ${info.get('marketCap', 0)/1e9:.2f}B.
        
        [END OF TRANSMISSION]
        """
        
        st.download_button(
            label="🖨️ DOWNLOAD CLASSIFIED BRIEF (TXT)",
            data=report_text,
            file_name=f"DOSSIER_{target}.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"TARGET LOST: {e}")