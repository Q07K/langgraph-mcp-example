import streamlit as st

from app.utils.mcp_utils import set_mcp_server
from app.views import llm_widget, mcp_widget
from app.views.chat_widget import reset_history
from app.views.dialog_widget import add_mcp_server


def sidebar() -> None:
    st.title("LLM")
    llm_widget.view_llm_list()
    llm_widget.base_url_input()
    llm_widget.api_key_input()
    st.divider()

    st.title("MCP Servers")
    server_config = set_mcp_server()
    mcp_widget.view_mcp_servers(
        mcp_servers=server_config,
    )
    st.divider()
    col1, col2 = st.columns(2, gap="large")
    col1.button(
        label="Add",
        use_container_width=True,
        on_click=add_mcp_server,
    )
    col2.button(
        label="Chat Reset",
        use_container_width=True,
        on_click=reset_history,
    )
