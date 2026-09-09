import os

import streamlit as st

from excel_agent.ui.app.context import context
from excel_agent.ui.displays.chat import display_chat
from excel_agent.ui.displays.upload import display_upload

# applications states
if "ingestion_status" not in st.session_state:
    st.session_state.ingestion_status = os.path.exists(context.config.database_file)

if "messages" not in st.session_state:
    st.session_state.messages = []

# main runner
if st.session_state.ingestion_status == True:
    display_chat()
else:
    display_upload()
