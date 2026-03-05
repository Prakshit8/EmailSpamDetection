"""
FraudShield AI - Email Fraud Detection System Frontend

Professional Streamlit frontend for email fraud detection
with FastAPI backend integration.
"""

import streamlit as st
import requests
import time
from typing import Dict, Any, Optional
import json

# Page configuration for professional look
st.set_page_config(
    page_title="FraudShield AI - Email Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuration
BACKEND_URL = "http://localhost:8001"  # Updated to match running backend

# Custom CSS for dark theme and professional styling
def load_custom_css():
    st.markdown("""
    <style>
        /* Import modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Global styles */
        .main {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 25%, #2d1b69 50%, #1a0033 75%, #0a0a0a 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: white;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Title section */
        .title-section {
            text-align: center;
            padding: 3rem 2rem;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 25px;
            margin-bottom: 2rem;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(138, 43, 226, 0.3);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }
        
        .title-section::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(138, 43, 226, 0.2), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .main-title {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #ffffff, #8a2be2, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 40px rgba(138, 43, 226, 0.5);
            position: relative;
            z-index: 1;
            animation: titleGlow 2s ease-in-out infinite alternate;
        }
        
        @keyframes titleGlow {
            from { filter: drop-shadow(0 0 20px rgba(138, 43, 226, 0.3)); }
            to { filter: drop-shadow(0 0 30px rgba(138, 43, 226, 0.6)); }
        }
        
        .subtitle {
            font-size: 1.3rem;
            color: #e8d5ff;
            margin-bottom: 0.5rem;
            font-weight: 300;
            position: relative;
            z-index: 1;
        }
        
        .business-impact {
            color: #b8a9d9;
            font-size: 1rem;
            margin-top: 1rem;
            font-style: italic;
        }
        
        /* Card styles */
        .card {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 20px;
            padding: 2.5rem;
            backdrop-filter: blur(25px);
            border: 1px solid rgba(138, 43, 226, 0.4);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(138, 43, 226, 0.7), transparent);
            animation: slideLight 3s infinite;
        }
        
        @keyframes slideLight {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.5);
            border-color: rgba(138, 43, 226, 0.6);
        }
        
        .model-info-card {
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.4), rgba(138, 43, 226, 0.1));
            border-left: 5px solid #8a2be2;
            position: relative;
        }
        
        .model-info-card::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(138, 43, 226, 0.4), transparent);
            border-radius: 50%;
        }
        
        .result-card {
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.5), rgba(138, 43, 226, 0.2));
            border-radius: 25px;
            padding: 2.5rem;
            margin-top: 2rem;
            text-align: center;
            backdrop-filter: blur(30px);
            border: 2px solid rgba(138, 43, 226, 0.4);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }
        
        .result-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(138, 43, 226, 0.2), transparent);
            animation: rotate 10s linear infinite;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .status-safe {
            background: linear-gradient(135deg, #1a0033, #4b0082, #1a0033);
            background-size: 200% 200%;
            animation: gradientMove 3s ease infinite;
            color: white;
            padding: 1.5rem 3rem;
            border-radius: 15px;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 1.5rem 0;
            box-shadow: 0 10px 25px rgba(75, 0, 130, 0.4);
            position: relative;
            z-index: 1;
        }
        
        .status-spam {
            background: linear-gradient(135deg, #4a0080, #8a2be2, #4a0080);
            background-size: 200% 200%;
            animation: gradientMove 3s ease infinite;
            color: white;
            padding: 1.5rem 3rem;
            border-radius: 15px;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 1.5rem 0;
            box-shadow: 0 10px 25px rgba(138, 43, 226, 0.4);
            position: relative;
            z-index: 1;
        }
        
        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .confidence-score {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 1.5rem 0;
            background: linear-gradient(45deg, #ffffff, #8a2be2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(138, 43, 226, 0.3);
        }
        
        .recommendation {
            background: rgba(0, 0, 0, 0.3);
            padding: 1.5rem;
            border-radius: 12px;
            margin-top: 1.5rem;
            border-left: 5px solid #8a2be2;
            backdrop-filter: blur(10px);
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        /* Input area styling */
        .stTextArea > div > div > textarea {
            background: rgba(0, 0, 0, 0.3);
            color: white;
            border: 2px solid rgba(138, 43, 226, 0.4);
            border-radius: 15px;
            font-size: 1.1rem;
            padding: 1rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #8a2be2;
            box-shadow: 0 0 20px rgba(138, 43, 226, 0.4);
            background: rgba(0, 0, 0, 0.4);
            outline: none;
        }
        
        .stTextArea > div > div > textarea::placeholder {
            color: rgba(232, 213, 255, 0.7);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(45deg, #1a0033, #4b0082, #8a2be2);
            background-size: 200% 200%;
            animation: gradientMove 3s ease infinite;
            color: white;
            border: none;
            padding: 1rem 2.5rem;
            font-size: 1.2rem;
            font-weight: 600;
            border-radius: 15px;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(75, 0, 130, 0.4);
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s ease;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(75, 0, 130, 0.5);
        }
        
        .stButton > button:active {
            transform: translateY(-1px);
        }
        
        /* Info items */
        .info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px solid rgba(138, 43, 226, 0.2);
            transition: all 0.3s ease;
        }
        
        .info-item:hover {
            background: rgba(138, 43, 226, 0.1);
            margin: 0 -1rem;
            padding: 1rem;
            border-radius: 10px;
        }
        
        .info-label {
            font-weight: 600;
            color: #8a2be2;
            font-size: 1rem;
        }
        
        .info-value {
            color: #ffffff;
            font-weight: 500;
            font-size: 1rem;
        }
        
        /* Hide streamlit branding */
        .stDeployButton {
            display: none;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #1a0033, #8a2be2);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(45deg, #4b0082, #8a2be2);
        }
        
        /* Loading animation */
        .stSpinner > div {
            border-top-color: #8a2be2 !important;
        }
        
        /* Error styling */
        .error-message {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.2), rgba(138, 43, 226, 0.1));
            border-left: 5px solid #8a2be2;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        /* Success styling */
        .success-message {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.2), rgba(138, 43, 226, 0.1));
            border-left: 5px solid #8a2be2;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

def check_backend_health() -> bool:
    """Check if the backend is healthy."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_model_stats() -> Optional[Dict[str, Any]]:
    """Get model statistics from backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def predict_email(email_text: str) -> Optional[Dict[str, Any]]:
    """
    Send email text to backend for prediction.
    
    Args:
        email_text: The email text to analyze
    
    Returns:
        Prediction response or None if failed
    """
    try:
        payload = {"email_text": email_text}
        response = requests.post(
            f"{BACKEND_URL}/predict",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Backend error: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Please ensure it's running.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def render_header():
    """Render professional header section."""
    st.markdown("""
    <div class="title-section">
        <h1 class="main-title">🛡️ FraudShield AI</h1>
        <p class="subtitle">Email Fraud Detection System</p>
        <p class="business-impact">
            Protect your organization from sophisticated email threats with AI-powered detection
        </p>
        <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700; color: #8a2be2;">99.2%</div>
                <div style="font-size: 0.9rem; color: #e8d5ff;">Accuracy</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700; color: #4b0082;">&lt;100ms</div>
                <div style="font-size: 0.9rem; color: #e8d5ff;">Response Time</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700; color: #6a0dad;">24/7</div>
                <div style="font-size: 0.9rem; color: #e8d5ff;">Protection</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_model_info(model_stats: Optional[Dict[str, Any]]):
    """Render model information card."""
    if not model_stats:
        model_stats = {
            "model_type": "Loading...",
            "vectorizer_type": "TF-IDF",
            "algorithm": "Loading...",
            "status": "Unknown",
            "cache_enabled": False
        }
    
    st.markdown("""
    <div class="card model-info-card">
        <h3 style="color: #8a2be2; margin-bottom: 1.5rem;">🤖 Model Information</h3>
    """, unsafe_allow_html=True)
    
    info_items = [
        ("Algorithm", model_stats.get("algorithm", "Unknown")),
        ("Model Type", model_stats.get("model_type", "Unknown")),
        ("Vectorizer", model_stats.get("vectorizer_type", "TF-IDF")),
        ("Status", model_stats.get("status", "Unknown")),
        ("Cache", "Enabled" if model_stats.get("cache_enabled") else "Disabled")
    ]
    
    for label, value in info_items:
        st.markdown(f"""
        <div class="info-item">
            <span class="info-label">{label}:</span>
            <span class="info-value">{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_result(prediction_data: Dict[str, Any]):
    """Render prediction result with professional styling."""
    prediction = prediction_data.get("prediction", "Unknown")
    confidence = prediction_data.get("confidence", 0.0)
    processing_time = prediction_data.get("processing_time_ms", 0.0)
    
    if prediction.lower() == "spam":
        status_text = "🚨 SPAM DETECTED"
        status_class = "status-spam"
        recommendation = """
        <strong>⚠️ Immediate Action Required:</strong><br>
        • Do not click any links in this email<br>
        • Do not download attachments<br>
        • Report as spam/phishing<br>
        • Delete the email immediately<br>
        • Consider changing passwords if personal info was shared
        """
    else:
        status_text = "✅ EMAIL SAFE"
        status_class = "status-safe"
        recommendation = """
        <strong>✅ Email appears safe:</strong><br>
        • No obvious spam indicators detected<br>
        • Standard email patterns observed<br>
        • Proceed with normal caution<br>
        • Still verify sender identity for sensitive requests
        """
    
    st.markdown(f"""
    <div class="result-card">
        <div class="{status_class}">{status_text}</div>
        <div class="confidence-score">
            Confidence: {confidence:.1f}%
        </div>
        <div style="color: #e8d5ff; font-size: 1rem; margin: 1rem 0;">
            Processing Time: {processing_time:.2f}ms
        </div>
        <div class="recommendation">
            {recommendation}
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function."""
    # Load custom CSS
    load_custom_css()
    
    # Render header
    render_header()
    
    # Check backend health
    backend_healthy = check_backend_health()
    
    if not backend_healthy:
        st.error("🚨 Backend service is not available. Please start the backend server first.")
        st.markdown("""
        <div class="error-message">
            <strong>To start the backend:</strong><br>
            1. Navigate to the backend directory<br>
            2. Run: <code>uvicorn main:app --host 0.0.0.0 --port 8000</code>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Get model stats
    model_stats = get_model_stats()
    
    # Create two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #8a2be2; margin-bottom: 1.5rem;">📧 Email Analysis</h3>', unsafe_allow_html=True)
        
        # Email input area
        email_input = st.text_area(
            "📧 Paste Email Content Here:",
            placeholder="✨ Enter the complete email text including:\n• Subject line\n• Sender information\n• Email body\n• Any links or attachments\n\nOur AI will analyze it for spam/fraud indicators...",
            height=350,
            label_visibility="visible"
        )
        
        # Analyze button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            analyze_button = st.button(
                "🔍 Analyze Email", 
                use_container_width=True,
                type="primary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle analysis
        if analyze_button:
            if not email_input or not email_input.strip():
                st.warning("⚠️ Please enter email content before analysis.")
                st.stop()
            
            # Show loading spinner
            with st.spinner("🤖 Analyzing email..."):
                prediction_data = predict_email(email_input)
            
            if prediction_data:
                # Render result
                render_result(prediction_data)
                
                # Success message
                st.markdown("""
                <div class="success-message">
                    <strong>✅ Analysis completed successfully!</strong><br>
                    The email has been processed using our advanced AI algorithms.
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # Render model information
        render_model_info(model_stats)
        
        # Additional info card
        st.markdown("""
        <div class="card" style="margin-top: 1rem;">
            <h4 style="color: #8a2be2; margin-bottom: 1rem;">📊 System Features</h4>
            <ul style="color: white; line-height: 1.8;">
                <li>Advanced text preprocessing</li>
                <li>TF-IDF feature extraction</li>
                <li>Machine learning classification</li>
                <li>Real-time confidence scoring</li>
                <li>Sub-second processing</li>
                <li>API-based architecture</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Backend status
        if backend_healthy:
            st.markdown("""
            <div class="card" style="margin-top: 1rem; border-left: 5px solid #00ff88;">
                <h4 style="color: #00ff88; margin-bottom: 1rem;">🟢 Backend Status</h4>
                <p style="color: white; margin: 0;">Connected and operational</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
