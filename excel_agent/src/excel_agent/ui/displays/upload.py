import streamlit as st

from excel_agent.services.core import ingest
from excel_agent.ui.app.context import context


def display_upload():
    st.title("Upload a file for ingestion!")

    with st.form("ingestion_form"):
        uploaded_file = st.file_uploader(
            label="Ingestion uploader", label_visibility="hidden", type=["xlsx"]
        )

        submit_button = st.form_submit_button("Ingest file")

        if submit_button:
            if uploaded_file is not None:
                with st.spinner(f"Ingesting {uploaded_file.name}..."):
                    ingest(context.agent, context.database, uploaded_file)

                st.session_state.ingestion_status = True
                st.success("Ingestion finished successfully!")
                st.rerun()
            else:
                st.warning("Please upload a file first.")
