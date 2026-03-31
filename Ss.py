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
div.stButton > button {
    padding: 4px 8px;
    font-size: 12px;
    height: 35px;
    border-radius: 6px;
}

div.stButton > button[kind="primary"] {
    background-color: #E0F2FE !important;
    color: #0369A1 !important;
    border: 1px solid #38BDF8 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ UI ------------------ #
def ai_resolution():

    st.title("KeDB - Incident Management System")

    left_col, right_col = st.columns([1, 2])

    # ----------- LEFT ----------- #
    with left_col:
        st.subheader("Incident Tickets")

        # BOX (Visible)
        st.info("Select an incident")

        for _, row in df.iterrows():

            is_selected = st.session_state.selected_ticket == row["Ticket ID"]
            button_type = "primary" if is_selected else "secondary"

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

            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader("Description")

            with col2:
                st.markdown("Opened: 03-27-2026 7:03:46")

            st.info(ticket_data["Issue"])

            if st.session_state.resolution_steps:

                st.subheader("Resolution Steps")

                resolution_text = ""
                for i, step in enumerate(st.session_state.resolution_steps, 1):
                    resolution_text += f"**Step {i}:** {step}\n\n"

                st.info(resolution_text)

                # ----------- FEEDBACK ----------- #
                st.markdown("### Feedback")

                col1, col2, _ = st.columns([1, 1, 10])

                with col1:
                    if st.button("👍", key="up"):
                        st.session_state.feedback[st.session_state.selected_ticket] = "Useful"
                        st.success("Thanks for your feedback!")

                with col2:
                    if st.button("👎", key="down"):
                        st.session_state.feedback[st.session_state.selected_ticket] = "Not Useful"
                        st.warning("We’ll improve this!")

        else:
            st.info("Select a ticket")

# ------------------ RUN ------------------ #
ai_resolution()
