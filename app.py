# app.py (PANOPTICON v4.1 - DUAL VECTOR)
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="PANOPTICON v4.1", page_icon="👁️", layout="wide")
st.markdown("""
<style>
    .stApp {background-color: #0e1117;}
    h1, h2, h3 {color: #00ff41 !important; font-family: 'Courier New', monospace;}
    div[data-testid="stMetricValue"] {color: #00ff41;}
    .stButton>button {border: 1px solid #00ff41; color: #00ff41; background-color: transparent;}
    .stButton>button:hover {background-color: #00ff41; color: black;}
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR CONTROL
with st.sidebar:
    st.title("👁️ CONTROLS")
    target = st.text_input("PRIMARY TARGET:", value="PLTR").upper()
    rival = st.text_input("RIVAL TARGET (OPTIONAL):", value="NVDA").upper()
    timeframe = st.selectbox("TIMEFRAME:", ["1mo", "3mo", "6mo", "1y", "5y", "max"])
    st.divider()
    st.markdown("### SYSTEM STATUS")
    st.caption("✅ VISUALS: ONLINE")
    st.caption("✅ NEWS FEED: PATCHED")

# 3. MAIN ENGINE
if target:
    try:
        # Fetch Primary Data
        stock = yf.Ticker(target)
        hist = stock.history(period=timeframe)
        info = stock.info
        
        # Fetch Rival Data (if exists)
        rival_hist = None
        if rival:
            rival_stock = yf.Ticker(rival)
            rival_hist = rival_stock.history(period=timeframe)

        # Header Metrics
        current_price = info.get('currentPrice', hist['Close'].iloc[-1])
        prev_close = info.get('previousClose', hist['Close'].iloc[-2])
        delta = ((current_price - prev_close)/prev_close)*100
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.title(f"📂 DOSSIER: {info.get('shortName', target)}")
        with col2:
            st.metric("LIVE PRICE", f"${current_price:.2f}", f"{delta:.2f}%")
        with col3:
            st.metric("MARKET CAP", f"${info.get('marketCap', 0)/1e9:.2f}B")

        # --- SECTOR A: COMPARATIVE INTELLIGENCE ---
        st.divider()
        st.subheader("📊 SECTOR A: RELATIVE PERFORMANCE")
        
        # Advanced Charting
        fig = go.Figure()
        
        # Plot Primary (Candles)
        fig.add_trace(go.Candlestick(x=hist.index,
                        open=hist['Open'], high=hist['High'],
                        low=hist['Low'], close=hist['Close'],
                        name=target))
        
        # Plot Rival (Line) - Scaled to match
        if rival_hist is not None and not rival_hist.empty:
            # Normalize to percentage change for fair comparison? 
            # For now, we just plot price on secondary axis or same axis if close.
            # Let's just plot the line for context.
            fig.add_trace(go.Scatter(x=rival_hist.index, y=rival_hist['Close'], 
                                     mode='lines', name=f"{rival} (Line)",
                                     line=dict(color='cyan', width=2)))

        fig.update_layout(xaxis_rangeslider_visible=False, height=500, 
                          template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0),
                          legend=dict(orientation="h", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)

        # --- SECTOR B: NARRATIVE STREAM (FIXED) ---
        st.divider()
        st.subheader("📰 SECTOR B: INTEL FEED")
        
        try:
            news_items = stock.news
            if news_items:
                for item in news_items[:3]:
                    # Safer dictionary access
                    title = item.get('title', 'Unknown Headline')
                    link = item.get('link', '#')
                    publisher = item.get('publisher', 'Unknown Source')
                    
                    with st.expander(f"🚨 {title}"):
                        st.write(f"**SOURCE:** {publisher}")
                        st.write(f"[ACCESS DOCUMENT]({link})")
            else:
                st.info("NO RECENT CHATTER DETECTED.")
        except Exception as e:
            st.warning(f"NEWS FEED OFFLINE: {e}")

        # --- SECTOR C: EXPORT ---
        st.divider()
        report_text = f"PANOPTICON BRIEF\nTARGET: {target}\nPRICE: ${current_price}\nRIVAL: {rival}"
        st.download_button("🖨️ DOWNLOAD BRIEF", report_text, file_name=f"{target}_BRIEF.txt")

    except Exception as e:
        st.error(f"SYSTEM FAILURE: {e}")