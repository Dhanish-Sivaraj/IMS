import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(layout="wide")

# ------------------ SAMPLE DATA ------------------ #
@st.cache_data
def load_data():
    data = {
        "Ticket ID": ["INC1001","INC1002","INC1003","INC1004"],
        "Issue": [
            "Login issue in VDI",
            "VPN not connecting",
            "Email not syncing",
            "System running slow"
        ],
        "Resolution": [
            "Reset credentials and restart VDI",
            "Reconfigure VPN settings",
            "Re-add email account",
            "Clear temp files and optimize system"
        ],
        "Category": ["Access", "Network", "Email", "Performance"]
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
        st.markdown("### Available Tickets")

        for i, row in df.iterrows():
            if st.button(
                f"{row['Ticket ID']}",
                use_container_width=True,
                key=row["Ticket ID"]
            ):
                st.session_state.selected_ticket = row["Ticket ID"]

                #  Auto-generate AI resolution
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

                st.subheader("Suggested Resolution")

                for i, step in enumerate(st.session_state.resolution_data["steps"], 1):
                    st.write(f"**Step {i}:** {step}")

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
            st.info("Select a ticket to generate resolution")

# ------------------ KNOWLEDGE BASE ------------------ #
def knowledge_base():
    st.title("Ticket Knowledge Base")
    st.dataframe(df, use_container_width=True)

# ------------------ NAVIGATION ------------------ #
pages = {
    "Resolution Engine": ai_resolution,
     "Knowledge Base": knowledge_base
}

st.sidebar.title("AI Support System")
selected_page = st.sidebar.radio("Navigation", list(pages.keys()))

pages[selected_page]()
