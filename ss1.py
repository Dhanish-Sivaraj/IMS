import streamlit as st
import pandas as pd
import time

st.set_page_config(layout="wide")

# ------------------ SAMPLE DATA ------------------ #
@st.cache_data
def load_data():
    data = {
        "Ticket ID": [
            "INC0378190","INC0377971","INC0377591","INC0378233",
            "INC0374293","INC0374280","INC0373329","INC0371859",
            "INC0373383","INC0373650"
        ],
        
        "Issue": [
            "production - qlik sense reload task failed",
            "compliancewire scheduled report",
            "errors detected in cloud run service",
            "qlik site is down",
            "qlik site recovered",
            "qlik local site down",
            "qlik local site recovered",
            "redshift sales reload failed",
            "marketing qvd reload failed",
            "auto reply email access issue"
        ],

        "Resolution": [
            "Check Qlik reload logs, validate data connection, restart reload task",
            "Validate schedule and re-trigger report",
            "Check logs and restart cloud service",
            "Restart Qlik engine and proxy services",
            "Monitor system stability",
            "Check server connectivity and restart services",
            "Confirm recovery and monitor logs",
            "Check Redshift connection and reload config",
            "Validate QVD pipeline and rerun",
            "Verify access and ignore auto replies"
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# ------------------ SESSION STATE ------------------ #
if "selected_ticket" not in st.session_state:
    st.session_state.selected_ticket = None

if "resolution_steps" not in st.session_state:
    st.session_state.resolution_steps = None

if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# ------------------ CUSTOM CSS ------------------ #
st.markdown("""
<style>

/* Compact ticket buttons */
div.stButton > button {
    padding: 4px 8px;
    font-size: 12px;
    height: 35px;
    border-radius: 6px;
}

/* Selected ticket (light blue) */
div.stButton > button[kind="primary"] {
    background-color: #E0F2FE !important;
    color: #0369A1 !important;
    border: 1px solid #38BDF8 !important;
}

/* Custom emoji button styling */
.custom-thumb-up {
    background: none !important;
    border: none !important;
    font-size: 24px !important;
    cursor: pointer !important;
    padding: 5px 10px !important;
    transition: transform 0.2s ease !important;
}

.custom-thumb-up:hover {
    transform: scale(1.2) !important;
}

.custom-thumb-down {
    background: none !important;
    border: none !important;
    font-size: 24px !important;
    cursor: pointer !important;
    padding: 5px 10px !important;
    transition: transform 0.2s ease !important;
}

.custom-thumb-down:hover {
    transform: scale(1.2) !important;
}

/* Reduce gap between feedback buttons */
div[data-testid="column"] {
    padding: 0px !important;
    margin: 0px !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------ UI ------------------ #
def ai_resolution():

    st.title("KeDB - Incident Management System")

    left_col, right_col = st.columns([1, 2])

    # ----------- LEFT ----------- #
    with left_col:
        st.markdown("### Incident Tickets")
    
        for _, row in df.iterrows():
    
            is_selected = st.session_state.selected_ticket == row["Ticket ID"]
    
            if is_selected:
                button_type = "primary"
            else:
                button_type = "secondary"
    
            if st.button(
                row["Ticket ID"],
                use_container_width=True,
                key=row["Ticket ID"],
                type=button_type
            ):
                st.session_state.selected_ticket = row["Ticket ID"]
    
                with st.spinner("Analyzing issue..."):
                    time.sleep(1)
    
                    issue = row["Issue"].lower()
    
                    if "qlik sense reload" in issue:
                        steps = [
                            "Check QMC reload task logs",
                            "Verify data source connections",
                            "Check script errors",
                            "Restart Qlik services",
                            "Re-trigger reload task"
                        ]
    
                    elif "qlik site is down" in issue:
                        steps = [
                            "Check server health",
                            "Verify Qlik Proxy",
                            "Restart services",
                            "Check network/DNS",
                            "Validate SSL"
                        ]
    
                    elif "cloud run" in issue:
                        steps = [
                            "Check cloud logs",
                            "Identify failing service",
                            "Restart service",
                            "Validate configs",
                            "Monitor logs"
                        ]
    
                    else:
                        steps = [
                            "Check logs",
                            "Validate config",
                            "Restart service",
                            "Check connectivity",
                            "Monitor system"
                        ]
    
                    st.session_state.resolution_steps = steps

    # ----------- RIGHT ----------- #
    with right_col:
    
        if st.session_state.selected_ticket:
    
            ticket_data = df[df["Ticket ID"] == st.session_state.selected_ticket].iloc[0]
    
            # Create two columns for Description header and timestamp
            desc_col1, desc_col2 = st.columns([3, 1])
            
            with desc_col1:
                st.subheader("Description")
            
            with desc_col2:
                st.markdown("Opened: 03-27-2026 7:03:46")
            
            st.info(f" {ticket_data['Issue']}")
    
            if st.session_state.resolution_steps:
    
                # Create columns for Resolution header
                res_col1, res_col2 = st.columns([3, 1])
                
                with res_col1:
                    st.subheader("Resolution Steps")
                
                with res_col2:
                    st.markdown("")  # Empty for alignment
                
                # Resolution steps in a blue info box
                resolution_text = ""
                for i, step in enumerate(st.session_state.resolution_steps, 1):
                    resolution_text += f"**Step {i}:** {step}\n\n"
                
                st.info(resolution_text)
    
                # ----------- FEEDBACK (INLINE 👍👎) ----------- #
                st.markdown("### Feedback")
    
                col1, col2, col3 = st.columns([1, 1, 15])
    
                with col1:
                    # Using HTML for green thumbs up
                    green_thumbs_up = st.button(
                        "👍", 
                        key="thumbs_up",
                        help="Useful"
                    )
                    if green_thumbs_up:
                        st.session_state.feedback[st.session_state.selected_ticket] = "Useful"
                        st.success("✅ Thank you for your feedback!")
                    
                    # Apply green color using st.markdown with JavaScript
                    st.markdown("""
                    <script>
                    setTimeout(function() {
                        let btn = document.querySelector('button[key="thumbs_up"]');
                        if(btn) {
                            btn.style.color = '#16A34A';
                            btn.style.background = 'none';
                            btn.style.border = 'none';
                            btn.style.fontSize = '24px';
                        }
                    }, 100);
                    </script>
                    """, unsafe_allow_html=True)
    
                with col2:
                    # Using HTML for red thumbs down
                    red_thumbs_down = st.button(
                        "👎", 
                        key="thumbs_down",
                        help="Not Useful"
                    )
                    if red_thumbs_down:
                        st.session_state.feedback[st.session_state.selected_ticket] = "Not Useful"
                        st.warning("📝 We'll work on improving this resolution!")
                    
                    # Apply red color using st.markdown with JavaScript
                    st.markdown("""
                    <script>
                    setTimeout(function() {
                        let btn = document.querySelector('button[key="thumbs_down"]');
                        if(btn) {
                            btn.style.color = '#DC2626';
                            btn.style.background = 'none';
                            btn.style.border = 'none';
                            btn.style.fontSize = '24px';
                        }
                    }, 100);
                    </script>
                    """, unsafe_allow_html=True)
    
        else:
            st.info("Select a ticket")

# ------------------ APP ------------------ #
ai_resolution()
