import streamlit as st

from api import create_report, get_reports
from utils.download_pdf import generate_pdf

st.set_page_config(
    page_title="Research Dashboard",
    page_icon="📚",
    layout="wide"
)

# =====================
# AUTH CHECK
# =====================

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("app.py")

# =====================
# SESSION STATE
# =====================

if "selected_report" not in st.session_state:
    st.session_state.selected_report = None

# =====================
# SIDEBAR
# =====================

st.sidebar.title("📚 Report History")

response = get_reports(st.session_state.token)

if response.status_code == 200:

    reports = response.json()

    if len(reports) == 0:
        st.sidebar.info("No reports found.")

    else:
        for report in reports:

            if st.sidebar.button(
                report["topic"],
                key=f"report_{report['id']}"
            ):
                st.session_state.selected_report = report

else:
    st.sidebar.error("Failed to load reports.")
st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    keys_to_remove = [
        "token",
        "selected_report"
    ]

    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]

    st.success("Logged out successfully!")

    st.switch_page("app.py")

# =====================
# MAIN PAGE
# =====================

st.title("Multi-Agent Research Assistant")

topic = st.text_input(
    "Enter Research Topic",
    placeholder="e.g. Multi-Agent Systems, RAG, LLM Agents..."
)

# =====================
# GENERATE REPORT
# =====================

if st.button("🚀 Generate Report"):

    if not topic.strip():
        st.warning("Please enter a topic.")
    else:

        with st.spinner("Generating report..."):

            response = create_report(
                st.session_state.token,
                topic
            )

        if response.status_code in [200, 201]:

            data = response.json()

            # Save report to session state
            st.session_state.selected_report = data["report"]

            st.success("Report generated successfully!")

        else:
            st.error(response.text)

# =====================
# DISPLAY REPORT
# =====================

if st.session_state.selected_report:

    report = st.session_state.selected_report

    st.divider()

    st.subheader(f"📄 {report['topic']}")

    st.markdown(report["report"])

    # PDF DOWNLOAD

    try:

        pdf_buffer = generate_pdf(
            report["topic"],
            report["report"]
        )

        st.download_button(
            label="📥 Download PDF",
            data=pdf_buffer,
            file_name=f"{report['topic'].replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"PDF generation failed: {str(e)}")