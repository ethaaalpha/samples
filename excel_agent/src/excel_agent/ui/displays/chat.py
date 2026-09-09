import streamlit as st

from excel_agent.ui.app.context import context


def _send_message():
    message = st.session_state.user_input

    if message:
        st.session_state.messages.append({"role": "user", "content": message})

        response = context.agent.ask(message)
        st.session_state.messages.append({"role": "assistant", "content": response})


def display_chat():
    st.title("Ask Excel Agent!")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    st.chat_input(
        "Your question!", key="user_input", max_chars=512, on_submit=_send_message
    )
