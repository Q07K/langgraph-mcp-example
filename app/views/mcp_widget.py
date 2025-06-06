import streamlit as st


def mcp_server_manager(key: str, value: dict) -> None:
    if st.session_state.get(f"apply_{key}", False):
        st.session_state["mcp_servers"][key] = value
    else:
        st.session_state[f"apply_{key}"] = False
        st.session_state["mcp_servers"].pop(key)


def apply_toggle(key: str, value: dict) -> None:
    st.toggle(
        label=".",
        key=f"apply_{key}",
        value=False,
        label_visibility="collapsed",
        on_change=mcp_server_manager,
        kwargs={"key": key, "value": value},
    )


def view_mcp_server(key: str):
    if st.session_state["mcp_servers"].get(key):
        st.success(key)
    else:
        st.error(key)


def view_mcp_servers(mcp_servers: dict):
    for key, value in mcp_servers.items():
        col1, col2 = st.columns(spec=[0.9, 0.1], vertical_alignment="top")
        with col1:
            view_mcp_server(key=key)
        with col2:
            apply_toggle(key=key, value=value)
