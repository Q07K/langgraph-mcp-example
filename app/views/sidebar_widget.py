import streamlit as st

from app.utils.mcp_utils import set_mcp_config
from app.views import llm_widget, mcp_widget
from app.views.dialog_widget import add_mcp_server


def sidebar() -> None:
    st.title("LLM")
    llm_widget.view_llm_list()
    llm_widget.base_url_input()
    llm_widget.api_key_input()
    st.divider()

    st.title("MCP Servers")
    server_config = set_mcp_config()
    mcp_widget.view_mcp_servers(
        mcp_servers=server_config,
    )
    st.divider()
    _, col, _ = st.columns([0.2, 0.6, 0.2])
    col.button(
        label="Add",
        use_container_width=True,
        on_click=add_mcp_server,
    )
