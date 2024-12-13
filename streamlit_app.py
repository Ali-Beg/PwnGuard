import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import json
from check_my_passwoed import (
    pawned_api_check, 
    generate_strong_password, 
    check_password_strength,
    encrypt_message,
    decrypt_message,
    log_password_check
)

# Configure page with dark theme
st.set_page_config(
    page_title="PwnGuard - Password Security Tool",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with better visibility
st.markdown("""
    <style>
    .main {
        background-color: #262730;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    div[data-testid="stMarkdownContainer"] {
        color: #ffffff;
    }
    .st-emotion-cache-nahz7x {
        background-color: #1f1f1f;
        color: white;
    }
    div[data-baseweb="tab-list"] {
        background-color: #333333;
    }
    .st-emotion-cache-1cypcdb {
        background-color: #333333;
        color: white;
        border: 1px solid #4CAF50;
    }
    .success-message {
        padding: 1rem;
        border-radius: 4px;
        background-color: #4CAF50;
        color: white;
    }
    .warning-message {
        padding: 1rem;
        border-radius: 4px;
        background-color: #f44336;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

def load_password_history():
    try:
        data = []
        with open('password_history.txt', 'rb') as f:
            for line in f:
                try:
                    decrypted = decrypt_message(line.strip())
                    if decrypted:
                        # Parse: "2023-12-31 23:59:59 - Password: xxx - Times found: 5 - Strength: 4/5"
                        parts = decrypted.split(' - ')
                        timestamp = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S')
                        password = parts[1].split(': ')[1]
                        times_found = int(parts[2].split(': ')[1])
                        strength = int(parts[3].split(': ')[1].split('/')[0])
                        
                        data.append({
                            'Date': timestamp,
                            'Password': password,
                            'Times Found': times_found,
                            'Strength': strength
                        })
                except Exception as e:
                    st.error(f"Error parsing entry: {str(e)}")
                    continue
        
        return pd.DataFrame(data)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Password', 'Times Found', 'Strength'])
    except Exception as e:
        st.error(f"Error loading history: {str(e)}")
        return pd.DataFrame(columns=['Date', 'Password', 'Times Found', 'Strength'])

def main():
    st.title("🔒 PwnGuard - Password Security Tool")
    
    # Verify secrets are configured
    if "fernet_key" not in st.secrets:
        st.error("Error: Streamlit secrets not configured! Please set up fernet_key in secrets.")
        st.stop()
    
    # Initialize session state for dashboard updates
    if 'history_updated' not in st.session_state:
        st.session_state.history_updated = False
    
    tabs = st.tabs(["Check Password", "Generate Password", "Security Dashboard"])
    
    with tabs[0]:
        st.header("Check Password Security")
        password = st.text_input("Enter password to check:", type="password")
        if st.button("Check Password"):
            if password:
                with st.spinner("Checking password security..."):
                    count = pawned_api_check(password)
                    strength_score, feedback = check_password_strength(password)
                    
                    # Log the check
                    log_password_check(password, count, strength_score)
                    st.session_state.history_updated = True
                    
                    if count:
                        st.error(f"⚠️ Password found in {count} data breaches!")
                    else:
                        st.success("✅ Password is safe!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Password Strength:")
                        st.progress(strength_score/5)
                        st.write(f"Score: {strength_score}/5")
                    
                    with col2:
                        if feedback:
                            st.write("Improvements needed:")
                            for item in feedback:
                                st.write(f"• {item}")

    with tabs[1]:
        st.header("Generate Strong Password")
        col1, col2 = st.columns([2,1])
        with col1:
            length = st.slider("Password Length", 12, 32, 16)
        with col2:
            if st.button("Generate Password"):
                password = generate_strong_password(length)
                st.code(password)
                
                # Check and log the generated password
                count = pawned_api_check(password)
                strength_score, _ = check_password_strength(password)
                log_password_check(password, count, strength_score)
                st.session_state.history_updated = True
                
                st.write("Password Strength:")
                st.progress(strength_score/5)

    with tabs[2]:
        st.header("Security Analytics")
        
        # Load history data
        if st.session_state.history_updated:
            df = load_password_history()
            st.session_state.history_updated = False
        else:
            df = load_password_history()
        
        if not df.empty:
            # Display analytics
            col1, col2 = st.columns(2)
            
            with col1:
                # Strength trend
                fig1 = px.line(df, x='Date', y='Strength',
                              title='Password Strength Trend')
                fig1.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(50, 50, 50, 0.8)',
                    paper_bgcolor='rgba(50, 50, 50, 0.8)'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Breach history
                fig2 = px.bar(df, x='Date', y='Times Found',
                             title='Password Breach History')
                fig2.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(50, 50, 50, 0.8)',
                    paper_bgcolor='rgba(50, 50, 50, 0.8)'
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Summary statistics
            st.subheader("Password Security Summary")
            col3, col4, col5 = st.columns(3)
            
            with col3:
                avg_strength = df['Strength'].mean()
                st.metric("Average Strength", f"{avg_strength:.1f}/5")
            
            with col4:
                breached = df[df['Times Found'] > 0].shape[0]
                st.metric("Breached Passwords", breached)
            
            with col5:
                total_checks = len(df)
                st.metric("Total Checks", total_checks)
            
            # Recent checks table
            st.subheader("Recent Password Checks")
            recent = df.sort_values('Date', ascending=False).head()
            st.dataframe(recent[['Date', 'Strength', 'Times Found']])
        else:
            st.info("No password check history available yet. Start checking passwords to see analytics!")

if __name__ == "__main__":
    main()
