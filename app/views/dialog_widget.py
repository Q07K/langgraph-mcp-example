# def mcp_state():

import streamlit as st

from app.utils.mcp_utils import save_mcp_server


@st.dialog(title="Add MCP Server")
def add_mcp_server():
    with st.form(key="Add", border=False):
        str_input = st.text_area(
            label="Add MCP Server",
            height=400,
            label_visibility="collapsed",
        )
        if st.form_submit_button(label="Add", use_container_width=True):
            save_mcp_server(str_input=str_input)
            st.rerun()
