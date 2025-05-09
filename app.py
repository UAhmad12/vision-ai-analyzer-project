import streamlit as st

# MUST BE THE VERY FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Vision AI Analyzer | Muhammad Zaqeem",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import other modules
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import io
import time
from streamlit_lottie import st_lottie
import json
import requests
import base64

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5tkzkblw.json")
lottie_upload = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5tkzkblw.json")

# Background image with overlay
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), 
                              url("https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?q=80&w=2874&auto=format&fit=crop");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .floating {{
            animation: float 3s ease-in-out infinite;
        }}
        
        .gradient-text {{
            background: linear-gradient(45deg, #4facfe, #00f2fe);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            display: inline;
        }}
        
        .glass-card {{
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }}
        
        .glass-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
        }}
        
        .stButton>button {{
            background: linear-gradient(45deg, #4facfe, #00f2fe);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 28px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .stButton>button:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .stFileUploader>div>div>div>div {{
            border: 2px dashed #4facfe;
            border-radius: 15px;
            padding: 30px;
            background: rgba(255,255,255,0.7);
            transition: all 0.3s;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()

# Header section
st.markdown("""
<div style="text-align: center; margin-bottom: 40px;">
    <h1 class="gradient-text" style="font-size: 3.5rem; margin-bottom: 0;">Vision AI Analyzer</h1>
    <p style="font-size: 1.2rem; color: #555;">Upload any image and get instant intelligent analysis powered by Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# Main content container
with st.container():
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        if lottie_ai:
            st_lottie(lottie_ai, height=300, key="ai-animation")
        
    with col2:
        with st.container():
            st.markdown("""
            <div class="glass-card">
                <h3 style="color: #2c3e50;">🔍 How it works:</h3>
                <ol style="color: #555;">
                    <li>Upload any image (JPG, PNG, WEBP)</li>
                    <li>Our AI will analyze the contents</li>
                    <li>Get detailed insights in seconds</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

# Upload section
with st.container():
    st.markdown("---")
    uploaded_file = st.file_uploader(
        "📤 Drag and drop or click to upload an image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supported formats: JPG, PNG, WEBP"
    )

# Analysis section
if uploaded_file:
    with st.spinner("🧠 Analyzing your image with advanced AI..."):
        # Progress animation
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        
        # Process image
        image = Image.open(uploaded_file)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Analysis prompt
        prompt = """Analyze this image comprehensively and provide:
        1. Detailed description of all visual elements
        2. Contextual interpretation
        3. Color and composition analysis
        4. Notable observations
        5. Potential creative applications
        
        Provide professional, insightful analysis in markdown format with bullet points."""
        
        try:
            response = model.generate_content(
                [prompt, {"mime_type": "image/png", "data": img_byte_arr}]
            )
            
            # Results display
            st.success("✅ Analysis Complete!")
            st.markdown("---")
            
            col1, col2 = st.columns([1, 1], gap="large")
            
            with col1:
                st.markdown("### 📸 Your Image")
                st.image(image, use_container_width=True, caption="Uploaded Image")
                
            with col2:
                st.markdown("### 🔬 AI Analysis")
                with st.expander("View Detailed Analysis", expanded=True):
                    st.markdown(response.text)
                
                st.download_button(
                    label="📥 Download Full Report",
                    data=response.text,
                    file_name="ai_vision_analysis.txt",
                    mime="text/plain",
                    key="download-btn"
                )

        except Exception as e:
            st.error(f"❌ Error in analysis: {str(e)}")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #666; font-size: 0.9rem;">
    <p>Developed by <b>Muhammad Zaqeem</b> | AI Research Lab</p>
    <p>© 2024 Vision AI Analyzer | All rights reserved</p>
</div>
""", unsafe_allow_html=True)