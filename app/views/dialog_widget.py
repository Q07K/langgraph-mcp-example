# def mcp_state():

import streamlit as st

MCP_SERVER_TRANSPORT = ["sse", "stdio"]


@st.dialog("Add MCP Server")
def add_mcp_server():
    with st.form("Add", border=False):

        col1, col2 = st.columns([0.2, 0.7])
        col1.subheader("transport")
        col2.selectbox(
            "transport",
            MCP_SERVER_TRANSPORT,
            label_visibility="collapsed",
        )

        if st.form_submit_button("Add", use_container_width=True):
            st.rerun()
