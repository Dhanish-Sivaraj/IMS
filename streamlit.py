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

# ------------------ CUSTOM CSS (OPTION 1) ------------------ #
st.markdown("""
<style>
/* 🔥 Compact ticket buttons */
div.stButton > button {
    padding: 4px 8px;
    font-size: 12px;
    height: 35px;
    border-radius: 6px;
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
    
            # Highlight selected ticket
            if is_selected:
                button_label = f"🔵 {row['Ticket ID']}"
                button_type = "primary"
            else:
                button_label = row["Ticket ID"]
                button_type = "secondary"
    
            if st.button(
                button_label,
                use_container_width=True,
                key=row["Ticket ID"],
                type=button_type
            ):
                st.session_state.selected_ticket = row["Ticket ID"]
    
                # 🔥 Real-time resolution generation
                with st.spinner("Analyzing issue..."):
                    time.sleep(1)
    
                    issue = row["Issue"].lower()
    
                    if "qlik sense reload" in issue:
                        steps = [
                            "Check Qlik Management Console (QMC) reload task logs",
                            "Verify data source connections (DB / APIs)",
                            "Check script errors in load script",
                            "Restart Qlik Engine & Scheduler services",
                            "Re-trigger reload task"
                        ]
    
                    elif "qlik site is down" in issue:
                        steps = [
                            "Check server health (CPU/memory)",
                            "Verify Qlik Proxy service",
                            "Restart Qlik services",
                            "Check DNS/network",
                            "Validate SSL"
                        ]
    
                    elif "cloud run" in issue:
                        steps = [
                            "Check cloud logs",
                            "Identify failing service",
                            "Restart container/service",
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

            st.subheader("📄 Ticket Details")
            st.write(f"**Ticket ID:** {ticket_data['Ticket ID']}")
            st.info(f"**Issue:** {ticket_data['Issue']}")

            # ----------- AI RESOLUTION ----------- #
            if st.session_state.resolution_steps:

                st.subheader("🤖 AI Resolution Steps")

                for i, step in enumerate(st.session_state.resolution_steps, 1):
                    st.write(f"**Step {i}:** {step}")

                st.subheader("📘 Known Fix")
                st.success(ticket_data["Resolution"])

        else:
            st.info("Select a ticket")

# ------------------ APP ------------------ #
ai_resolution()
