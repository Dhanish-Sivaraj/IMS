import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(layout="wide")

# ------------------ SAMPLE DATA ------------------ #
@st.cache_data
def load_data():
    data = {
    "Ticket ID": [
        "INC0378190","INC0377971","INC0377591","INC0378233",
        "INC0374293","INC0374280","INC0373329","INC0371859",
        "INC0373383","INC0373650","INC0371663","INC0371362",
        "INC0371276","INC0375731"
    ],
    
    "Issue": [
        "production - qlik sense reload task failed!!!",
        "compliancewire scheduled report",
        "[alert - error] [alert]: errors detected in cloud run service in inroads prod",
        "alert for device qlik.insmed.com - qlik site is down",
        "device qlik.insmed.com recovered from qlik site is down",
        "alert for device insawsqlik.insmed.local - qlik site is down",
        "device insawsqlik.insmed.local recovered from qlik site is down",
        "qlik cloud - redshift japan sales reload task failed!!!",
        "qlik cloud - marketing qvd gen reload task failed!!!",
        "automatic reply: insmed connect reinvite you to access applications within their organization.",
        "sandbox: verify your identity in salesforce",
        "automatic reply: insmed connect invite you to access applications within their organization.",
        "compliancewire scheduled report",
        "prod deployment approval - emea sales dashboard"
    ],

    "Resolution": [
        "Restart Qlik services and verify reload task logs",
        "Validate report schedule and re-trigger job",
        "Check cloud run logs and fix service errors",
        "Verify Qlik server status and restart services",
        "Monitor system recovery and validate uptime",
        "Check server connectivity and restart Qlik services",
        "Confirm recovery and monitor system stability",
        "Check Redshift connection and reload task config",
        "Validate QVD generation pipeline and rerun job",
        "Ignore auto reply or verify access request if needed",
        "Complete Salesforce identity verification steps",
        "Accept invite and validate access permissions",
        "Revalidate report scheduling configuration",
        "Review deployment approval workflow and proceed"
    ]
}
    return pd.DataFrame(data)

df = load_data()

# ------------------ SESSION STATE ------------------ #
if "selected_ticket" not in st.session_state:
    st.session_state.selected_ticket = None

if "resolution_data" not in st.session_state:
    st.session_state.resolution_data = None

# ------------------ CUSTOM CSS ------------------ #
st.markdown("""
<style>
.section {
    padding: 20px;
    border-radius: 10px;
    background-color: #F9FAFB;
    border: 1px solid #E5E7EB;
}
</style>
""", unsafe_allow_html=True)

# ------------------ MAIN PAGE ------------------ #
def ai_resolution():

    st.title("KeDB - Incident Management System")

    # ----------- LAYOUT ----------- #
    left_col, right_col = st.columns([1, 2])

    # ----------- LEFT: TICKETS ----------- #
    with left_col:
        st.markdown("### 🎫 Available Tickets")

        for i, row in df.iterrows():
            if st.button(
                f"{row['Ticket ID']}",
                use_container_width=True,
                key=row["Ticket ID"]
            ):
                st.session_state.selected_ticket = row["Ticket ID"]

                # 🔥 Auto-generate AI resolution
                with st.spinner("Generating AI resolution..."):
                    time.sleep(0.8)

                    steps = [
                        "Validate user credentials",
                        "Restart system/session",
                        "Clear cache and temp files",
                        "Check network connectivity",
                        "Reconfigure application settings"
                    ]

                    resolution_plan = random.sample(steps, 3)
                    confidence = round(random.uniform(0.75, 0.95), 2)

                    st.session_state.resolution_data = {
                        "steps": resolution_plan,
                        "confidence": confidence
                    }

    # ----------- RIGHT: DETAILS ----------- #
    with right_col:

        if st.session_state.selected_ticket:

            ticket_data = df[df["Ticket ID"] == st.session_state.selected_ticket].iloc[0]

            st.markdown('<div class="section">', unsafe_allow_html=True)

            st.subheader("📄 Ticket Details")

            col1, col2 = st.columns(2)
            col1.write(f"**Ticket ID:** {ticket_data['Ticket ID']}")
            col2.write(f"**Category:** {ticket_data['Category']}")

            st.info(f"**Issue:** {ticket_data['Issue']}")

            # ----------- AUTO AI RESOLUTION ----------- #
            if st.session_state.resolution_data:

                st.subheader("🤖 AI Suggested Resolution")

                for i, step in enumerate(st.session_state.resolution_data["steps"], 1):
                    st.write(f"**Step {i}:** {step}")

                st.metric(
                    "📊 AI Confidence",
                    f"{st.session_state.resolution_data['confidence'] * 100}%"
                )

                st.subheader("📘 Known Resolution")
                st.success(ticket_data["Resolution"])

                # ----------- FEEDBACK ----------- #
                st.subheader("💬 Feedback")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("👍 Useful"):
                        st.success("Thanks! Feedback recorded.")

                with col2:
                    if st.button("👎 Not Useful"):
                        st.warning("We'll improve based on your feedback.")

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.info("👈 Select a ticket to generate resolution")

# ------------------ KNOWLEDGE BASE ------------------ #
def knowledge_base():
    st.title("📂 Ticket Knowledge Base")
    st.dataframe(df, use_container_width=True)

# ------------------ NAVIGATION ------------------ #
pages = {
    "🚀 Resolution Engine": ai_resolution,
    "📂 Knowledge Base": knowledge_base
}

st.sidebar.title("AI Support System")
selected_page = st.sidebar.radio("Navigation", list(pages.keys()))

pages[selected_page]()
