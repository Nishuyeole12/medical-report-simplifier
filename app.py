import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration using Streamlit Secrets
# This is secure. Ensure you add 'GEMINI_API_KEY' in Streamlit Cloud Secrets settings.
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("API Key not found! Please set 'GEMINI_API_KEY' in your Streamlit secrets.")
    st.stop()

# 2. Model Selection
model = genai.GenerativeModel('gemini-2.0-flash')

st.set_page_config(page_title="Med-Dost AI", page_icon="🏥")

# Sidebar - Instructions & Constraints
st.sidebar.header("Instructions")
st.sidebar.warning("⚠️ Only Image formats (JPG/PNG) are supported. PDF files are not allowed.")

# 3. Sidebar for Language
lang = st.sidebar.selectbox("Select Output Language", ["Marathi", "Hindi", "English"])

st.title("🏥 Med-Dost AI: Medical Assistant")
st.markdown("### Upload your medical report photo for instant AI analysis.")

# 4. Main UI - File Uploader
uploaded_file = st.file_uploader("Choose a Report Photo", type=["jpg", "jpeg", "png"])

st.info("💡 Tip: If you have a PDF, please take a screenshot of it and upload the image.")

if uploaded_file:
    # Load and display the image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Report", use_container_width=True)
    
    if st.button("Analyze Now"):
        with st.spinner("AI is analyzing your report..."):
            try:
                # Instruction to AI
                prompt = f"Explain this medical report image in very simple {lang}. Use bullet points."
                
                # API Call
                response = model.generate_content([prompt, img])
                
                st.success("Analysis Complete!")
                st.markdown("### 📝 AI Findings:")
                st.write(response.text)
                
            except Exception as e:
                # Handling common errors like quota limits
                st.error("System is busy or quota limit reached. Please try again in 60 seconds.")
                
                # Internal fallback to older stable model
                try:
                    fallback_model = genai.GenerativeModel('gemini-flash-latest')
                    response = fallback_model.generate_content([prompt, img])
                    st.write(response.text)
                except:
                    pass

st.divider()
st.caption("Secured Deployment Mode | Running on Gemini 2.0 Flash")