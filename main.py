import streamlit as st
from datetime import datetime
from search import search_agent
from verfier import verifier_agent
from scraper import scraper_agent
from synthesizer import synthesizer_agent

st.set_page_config(page_title="Autonomous AI Research Agent")
st.markdown("""
<div style='position: fixed; top: 20px; left: 0; right: 0; background-color: #0e1117; z-index: 998; padding: 1rem 0; text-align: center;'>
    <h1 style='color: white; margin: 0;'>Autonomous AI Research Agent</h1>
</div>
<div style='margin-top: 100px;'></div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask anything...", width="stretch")
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
with col2:
    if st.button("Convert to Report", use_container_width=True):
        if st.session_state.messages:
            with st.spinner("Generating report..."):
                from report import report_agent
                pdf_bytes = report_agent(st.session_state.messages)
            st.download_button(
                label="⬇stDownload PDF",
                data=pdf_bytes,
                file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.warning("No conversation to convert yet.")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})


    search_results = search_agent(user_input)
    verified = verifier_agent(search_results)
    scraped = scraper_agent(verified)
    synthesised_result = synthesizer_agent(user_input, scraped)

    response = f"Research result for: {user_input}"

    with st.chat_message("Research Agent"):
        st.write(response)
        st.write(synthesised_result)
    st.session_state.messages.append({"role": "assistant", "content": synthesised_result})
