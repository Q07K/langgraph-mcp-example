"""Streamlit MCP widget"""

import streamlit as st


def mcp_server_manager(key: str, value: dict) -> None:
    """MCP Server 적용 상태를 관리하는 콜백 함수입니다.

    `st.toggle` 위젯의 상태 변경(`on_change`) 시 호출됩니다. 토글이 켜지면
    해당 MCP Server의 정보를 `st.session_state["mcp_servers"]`에 추가하고,
    꺼지면 제거하여 MCP Server의 '적용' 상태를 관리합니다.

    Parameters
    ----------
    key : str
        관리할 MCP Server의 고유 식별자 키.
    value : dict
        MCP Server의 구성 정보를 담은 딕셔너리.
    """
    if st.session_state.get(f"apply_{key}", False):
        st.session_state["mcp_servers"][key] = value
    else:
        st.session_state[f"apply_{key}"] = False
        st.session_state["mcp_servers"].pop(key)


def apply_toggle(key: str, value: dict) -> None:
    """특정 MCP Server를 적용/해제하는 `st.toggle` 위젯을 생성합니다.

    토글 위젯의 상태가 변경되면 `mcp_server_manager` 콜백 함수를
    호출하여 서버 적용 상태를 실제로 변경합니다.

    Parameters
    ----------
    key : str
        토글이 제어할 MCP Server의 고유 식별자 키.
    value : dict
        콜백 함수에 전달될 MCP Server의 구성 정보 딕셔너리.
    """
    st.toggle(
        label=".",
        key=f"apply_{key}",
        value=False,
        label_visibility="collapsed",
        on_change=mcp_server_manager,
        kwargs={"key": key, "value": value},
    )


def view_mcp_server(key: str) -> None:
    """MCP Server를의 현재 적용 상태를 시각적으로 표시합니다.

    `st.session_state["mcp_servers"]`에 해당 MCP Server 정보가 있는지 확인하여,
    '적용' 상태인 경우 `st.success`로, 아닌 경우 `st.error`로 상태를
    표시합니다.

    Parameters
    ----------
    key : str
        상태를 표시할 MCP Server의 고유 식별자 키.
    """
    if st.session_state["mcp_servers"].get(key):
        st.success(key)
    else:
        st.error(key)


def view_mcp_servers(mcp_servers: dict) -> None:
    """전체 MCP Server 목록과 각 서버의 제어 위젯을 표시합니다.

    전달받은 `mcp_servers` 딕셔너리를 순회하며, 각 서버에 대해
    `view_mcp_server`로 상태를 표시하고, `apply_toggle`로 제어용 토글 스위치를
    생성하여 UI에 렌더링합니다.

    Parameters
    ----------
    mcp_servers : dict
        화면에 표시할 모든 MCP Server의 구성 정보를 담은 딕셔너리.
        `mcp_servers.json`에서 불러온 MCP Server의 구성 정보 입니다.
    """
    for key, value in mcp_servers.items():
        col1, col2 = st.columns(spec=[0.9, 0.1], vertical_alignment="top")
        with col1:
            view_mcp_server(key=key)
        with col2:
            apply_toggle(key=key, value=value)
