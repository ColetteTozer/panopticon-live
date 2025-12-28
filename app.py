# app.py
import streamlit as st
import urllib.request
import json

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="PANOPTICON v3.2", page_icon="👁️", layout="wide")

# 2. THE STEALTH PROBE LOGIC (Hidden Function)
def run_stealth_probe(ticker):
    # Yahoo Finance URL
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        result = data['chart']['result'][0]
        meta = result['meta']
        
        return {
            "price": meta['regularMarketPrice'],
            "prev_close": meta['chartPreviousClose'],
            "currency": meta.get('currency', 'USD'),
            "status": "ACTIVE"
        }
    except Exception as e:
        return {"error": str(e)}

# 3. THE USER INTERFACE
st.title("👁️ PANOPTICON OSINT ENGINE")
st.markdown("`STATUS: ONLINE` | `MODE: STEALTH` | `SOURCE: YAHOO QUERY1`")

# Input Box
col1, col2 = st.columns([3, 1])
with col1:
    target = st.text_input("ENTER ASSET TICKER:", value="PLTR").upper()
with col2:
    st.write("") # Spacer
    st.write("") # Spacer
    run_btn = st.button("INITIATE PROBE", type="primary")

# 4. EXECUTION ON BUTTON CLICK
if run_btn:
    with st.spinner(f"TRIANGULATING TARGET: {target}..."):
        data = run_stealth_probe(target)
        
        if "error" in data:
            st.error(f"CONNECTION FAILED: {data['error']}")
        else:
            # Calculate metrics
            price = data['price']
            prev = data['prev_close']
            change = price - prev
            pct_change = (change / prev) * 100
            
            # Display Big Metrics
            st.divider()
            m1, m2, m3 = st.columns(3)
            m1.metric("CURRENT PRICE", f"${price:.2f}", f"{pct_change:.2f}%")
            m2.metric("PREVIOUS CLOSE", f"${prev:.2f}")
            m3.metric("SIGNAL STRENGTH", "HIGH (Stealth)")
            
            # Display "Dossier" Style Report
            st.divider()
            st.subheader(f"📂 DOSSIER: {target}")
            st.markdown(f"""
            > **VERDICT:** The asset is currently trading at **${price}**. 
            > Volatility detected. System recommends cross-referencing with 10-K filings.
            
            * **Data Source:** `query1.finance.yahoo.com`
            * **Method:** `urllib` (Stealth Headers)
            * **Latency:** < 200ms
            """)
            st.success("INTELLIGENCE PACKAGE DELIVERED.")