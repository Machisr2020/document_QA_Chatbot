import streamlit as st
from query import ask_question

st.set_page_config(
    page_title="Document Q&A Bot",
    page_icon="📄"
)

st.title("🤖 AI Question Answering Bot System")

question = st.text_input(
    "Ask a question about your document"
)

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        answer = ask_question(question)

        st.subheader("Answer")

        st.write(answer)