import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
import time

# Page configuration with modern styling
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 0;
    }
    
    /* Form container styling */
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        margin-bottom: 2rem;
    }
    
    /* Custom selectbox styling */
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        font-weight: 500;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Generated post styling */
    .post-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .post-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        color: #2c3e50;
        font-weight: 600;
        font-size: 1.3rem;
    }
    
    .post-content {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        line-height: 1.6;
        font-size: 1rem;
        color: #2c3e50;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
        white-space: pre-wrap;
    }
    
    /* Copy button styling */
    .copy-button {
        background: #28a745;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    
    .copy-button:hover {
        background: #218838;
        transform: translateY(-1px);
    }
    
    /* Stats cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        flex: 1;
        border-top: 3px solid #667eea;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #6c757d;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Loading animation */
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        border-top: 1px solid #e9ecef;
        margin-top: 3rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📝 LinkedIn Post Generator</h1>
    <p class="header-subtitle">LinkedIn Post Generator Powered by LLMs</p>
</div>
""", unsafe_allow_html=True)

# Initialize FewShotPosts instance and get tags
fs = FewShotPosts()
tags = fs.get_tags()

# Stats section
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">50+</div>
        <div class="stat-label">Topics Available</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">3</div>
        <div class="stat-label">Post Lengths</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">2</div>
        <div class="stat-label">Languages</div>
    </div>
    """, unsafe_allow_html=True)

# Form section
st.markdown('<div class="form-container">', unsafe_allow_html=True)

st.markdown("### 🎯 Customize Your Post")

col1, col2 = st.columns(2)

with col1:
    selected_tag = st.selectbox(
        "📌 Select Topic:",
        options=tags,
        help="Choose the main topic for your LinkedIn post"
    )
    
    selected_length = st.selectbox(
        "📏 Post Length:",
        options=["Short", "Medium", "Long"],
        help="Short: 1-5 lines, Medium: 6-10 lines, Long: 11-15 lines"
    )

with col2:
    selected_language = st.selectbox(
        "🌐 Language:",
        options=["English", "Hinglish"],
        help="Choose between English or Hinglish (Hindi + English mix)"
    )
    
    st.markdown("### 🚀 Ready to Generate?")
    generate_clicked = st.button("✨ Generate LinkedIn Post", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Generate button and post display
if generate_clicked:
    # Loading animation
    with st.spinner('🤖 AI is crafting your perfect LinkedIn post...'):
        time.sleep(1)  # Small delay for better UX
        post = generate_post(selected_length, selected_language, selected_tag)
    
    # Display generated post
    st.markdown("""
    <div class="post-container">
        <div class="post-header">
            📝 Your Generated LinkedIn Post
        </div>
        <div class="post-content">{}</div>
    </div>
    """.format(post.replace('\n', '<br>')), unsafe_allow_html=True)
    
    # Copy to clipboard functionality
    st.code(post, language=None)
    
    # Success message
    st.success("🎉 Your LinkedIn post is ready! Copy the text above and share it on LinkedIn.")
    
    # Additional tips
    with st.expander("💡 Tips for Better Engagement"):
        st.markdown("""
        - **Add relevant hashtags** to increase visibility
        - **Tag relevant people** in your network
        - **Post during peak hours** (8-10 AM or 12-2 PM)
        - **Engage with comments** to boost algorithm reach
        - **Use emojis sparingly** but effectively
        - **Ask questions** to encourage interaction
        """)

# Footer
st.markdown("""
<div class="footer">
    <p>LinkedIn Post Generator Powered by LLMs</p>
</div>
""", unsafe_allow_html=True)

