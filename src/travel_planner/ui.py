# src/travel_planner/ui.py
import streamlit as st
import sys
import os
from pathlib import Path
import json
from datetime import datetime, timedelta

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from travel_planner.crew import crew

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .flight-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    
    .itinerary-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>✈️ AI Travel Planner</h1>
    <p>Plan your perfect trip with intelligent multi-agent assistance</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.markdown("### 🎯 Trip Details")
    
    # Origin and destination with autocomplete suggestions
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("🛫 Origin (IATA)", "MEL", help="Enter airport code (e.g., MEL, SYD, LAX)")
    with col2:
        destination = st.text_input("🛬 Destination (IATA)", "BLR", help="Enter airport code (e.g., BLR, DEL, NYC)")
    
    # Date selection with smart defaults
    default_date = datetime.now() + timedelta(days=30)
    date = st.date_input("📅 Travel Date", value=default_date, min_value=datetime.now().date())
    
    # Interests with better options
    st.markdown("### 🎨 Interests")
    interests = st.multiselect(
        "What interests you?",
        ["🍽️ Food & Dining", "🏛️ Culture & History", "🌿 Nature & Outdoors", 
         "🛍️ Shopping", "🎭 Arts & Entertainment", "🏖️ Beaches & Relaxation",
         "🏃 Adventure & Sports", "🍷 Wine & Nightlife"],
        default=["🍽️ Food & Dining", "🏛️ Culture & History"]
    )
    
    # Additional options
    st.markdown("### ⚙️ Options")
    max_price = st.slider("💰 Max Price (EUR)", 200, 2000, 1000, 50)
    preferred_airlines = st.multiselect(
        "✈️ Preferred Airlines",
        ["Any", "Cathay Pacific", "Singapore Airlines", "Emirates", "Qatar Airways", "Lufthansa"]
    )
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <h4>💡 Tips</h4>
        <ul>
            <li>Use 3-letter airport codes</li>
            <li>Select multiple interests for better recommendations</li>
            <li>Our AI agents will find the best routes with stopovers</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Plan Trip button
    if st.button("🚀 Plan My Trip", use_container_width=True):
        if not origin or not destination:
            st.error("Please enter both origin and destination airports.")
        else:
            # Show progress
            with st.spinner("🤖 AI agents are planning your perfect trip..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate progress
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text("🔍 Searching for flights...")
                    elif i < 60:
                        status_text.text("📊 Evaluating routes...")
                    elif i < 90:
                        status_text.text("🗺️ Creating itineraries...")
                    else:
                        status_text.text("✨ Finalizing your travel plan...")
                
                try:
                    # Run the crew
                    result = crew.kickoff(inputs={
                        "origin": origin,
                        "destination": destination,
                        "date": str(date),
                        "interests": interests
                    })
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Success message
                    st.markdown("""
                    <div class="success-message">
                        <h3>🎉 Your Travel Plan is Ready!</h3>
                        <p>Our AI agents have found the perfect routes and created amazing itineraries for your stopovers.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display results in a structured way
                    st.markdown("## 📋 Travel Plan Summary")
                    
                    # Parse and display the result
                    if isinstance(result, str):
                        # Try to extract flight information
                        if "Flight ID" in result:
                            st.markdown("### ✈️ Recommended Flights")
                            
                            # Extract flight information using simple parsing
                            lines = result.split('\n')
                            current_flight = None
                            
                            for line in lines:
                                if "Flight ID" in line and "€" in line:
                                    # Extract flight info
                                    flight_info = line.strip()
                                    st.markdown(f"""
                                    <div class="flight-card">
                                        <h4>{flight_info}</h4>
                                    </div>
                                    """, unsafe_allow_html=True)
                                elif "**Day" in line or "**Morning" in line or "**Evening" in line:
                                    st.markdown(line)
                                elif line.strip().startswith("-"):
                                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{line}")
                                elif line.strip() and not line.startswith("**"):
                                    st.markdown(line)
                        else:
                            st.markdown(result)
                    else:
                        st.json(result)
                    
                    # Add download button for the plan
                    st.markdown("### 💾 Download Your Plan")
                    plan_data = {
                        "origin": origin,
                        "destination": destination,
                        "date": str(date),
                        "interests": interests,
                        "plan": result
                    }
                    
                    st.download_button(
                        label="📥 Download Travel Plan (JSON)",
                        data=json.dumps(plan_data, indent=2),
                        file_name=f"travel_plan_{origin}_{destination}_{date}.json",
                        mime="application/json"
                    )
                    
                except Exception as e:
                    st.error(f"❌ An error occurred while planning your trip: {str(e)}")
                    st.info("Please try again or check your inputs.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>Powered by CrewAI Multi-Agent System | Built with ❤️ for travelers</p>
    <p>✈️ Find the best routes | 🗺️ Discover amazing stopovers | 🎯 Plan perfect itineraries</p>
</div>
""", unsafe_allow_html=True)
