# --- REFINED AI INTEL REPORT (v5.3.1) ---
st.divider()
st.subheader("🤖 AI INTEL REPORT")

if SYSTEM_READY:
    try:
        # 1. CONFIGURE THE BRAIN WITH SYSTEM INSTRUCTIONS
        # Using the absolute most stable model identifier
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            system_instruction="""
            IDENTITY: You are PANOPTICON, a ruthless Financial Intel Unit.
            VOICE: Cold, data-driven, cynical of market hype. 
            GOAL: Identify asymmetric risk and hidden intel.
            """
        )
        
        # 2. GENERATE RESPONSE WITH LIVE CONTEXT
        # We pass the real stock data to the AI so it's never "dumb"
        intel_prompt = f"Analyze {target}. Current price: ${current:.2f}. Previous close: ${prev:.2f}. Give a 3-point ruthless risk assessment."
        
        response = model.generate_content(intel_prompt)
        st.markdown(response.text)
        
    except Exception as ai_err:
        st.error(f"NEURAL LINK FAILURE: {ai_err}")