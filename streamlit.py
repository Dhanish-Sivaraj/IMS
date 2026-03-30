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

# ------------------ UI ------------------ #
def ai_resolution():

    st.title("KeDB - Incident Management System")

    left_col, right_col = st.columns([1, 2])

    # ----------- LEFT ----------- #
    with left_col:
        st.markdown("### 🎫 Tickets")

        for _, row in df.iterrows():
            if st.button(row["Ticket ID"], use_container_width=True):

                st.session_state.selected_ticket = row["Ticket ID"]

                # 🔥 Real-time resolution generation
                with st.spinner("Analyzing issue..."):
                    time.sleep(1)

                    issue = row["Issue"].lower()

                    if "qlik sense reload" in issue:
                        steps = [
                            "Check Qlik Management Console (QMC) reload task logs",
                            "Verify data source connections (DB / APIs)",
                            "Check if any script error occurred in load script",
                            "Restart Qlik Engine and Scheduler services",
                            "Re-trigger reload task manually and monitor"
                        ]

                    elif "qlik site is down" in issue:
                        steps = [
                            "Check server status and CPU/memory usage",
                            "Verify Qlik Proxy service",
                            "Restart Qlik services",
                            "Check network/DNS resolution",
                            "Validate SSL certificate if applicable"
                        ]

                    elif "cloud run" in issue:
                        steps = [
                            "Check cloud logs (GCP/AWS)",
                            "Identify failing service",
                            "Restart service/container",
                            "Validate environment variables",
                            "Monitor logs after restart"
                        ]

                    else:
                        steps = [
                            "Check application logs",
                            "Validate configuration",
                            "Restart service",
                            "Verify connectivity",
                            "Monitor after fix"
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
