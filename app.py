import streamlit as st
from agents.coordinator_agent import Coordinator
from utils.download_pdf import generate_pdf

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🧠", layout="wide")
st.title("Multi-Agent Research Assistant")
st.write("Enter a research topic, and let multiple AI agents collaborate to fetch papers, summarize, write, and critique your report.")
topic=st.text_input("Enter your Research Topic")
if "result" not in st.session_state:
    st.session_state.result = None
if st.button("🚀 Generate Research Report"):
    if not topic:
        st.warning("Please enter a topic first!")
    else:
        with st.spinner("Running multi-agent process..."):
            coordinator = Coordinator(topic)
            st.session_state.result = coordinator.run()
        st.success("✅ Process complete!")

        st.subheader("📄 Final Research Report")
        st.write(st.session_state.result)
        pdf_buffer=generate_pdf(f"Research Report - {topic}", st.session_state.result)
    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name=f"{topic.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )


    