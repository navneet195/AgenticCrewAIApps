import streamlit as st
from tab1_chatbot import render_tab1
from tab2_financial_analysis import render_tab2
from tab3_recruitment import render_tab3

st.set_page_config(
    page_title="Agentic AI Chatbot",
    page_icon="📄",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")
selected_tab = st.sidebar.radio(
    "Choose a feature",
    ["📄 Chatbot with Docs", "📊 Financial Analysis", "🤖 Job Recruitment"]
)

# Main Title & Intro
st.title("🤖 Crew Agentic AI Chatbot")
st.markdown("""
Welcome to the **Agentic AI Chatbot Demo**!  
Explore different functionalities powered by autonomous agents.  
""")
st.divider()

# Render only the selected tab
if selected_tab == "📄 Chatbot with Docs":
    # st.subheader("📄 Document Chatbot")
    render_tab1()

elif selected_tab == "📊 Financial Analysis":
    # st.subheader("📊 AI Financial Analysis")
    render_tab2()

elif selected_tab == "🤖 Job Recruitment":
    # st.subheader("🤖 Recruitment Assistant")
    render_tab3()
