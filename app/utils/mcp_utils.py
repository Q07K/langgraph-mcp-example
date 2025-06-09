"""MCP Server utils"""

import json

# MCP Server 설정 파일의 기본 경로
MCP_SERVERS_PATH = "./mcp_servers.json"


def load_mcp_server() -> dict:
    """`mcp_servers.json` 설정 파일을 읽어와 내용을 반환합니다.

    파일이 없으면 기본 구조를 반환하고, 파일이 손상되었거나
    읽을 수 없으면 예외를 발생시킵니다.

    Returns
    -------
    dict
        MCP Server config 내용이 담긴 딕셔너리.

    Raises
    ------
    IOError
        파일을 읽는 중 I/O 에러가 발생한 경우.
    json.JSONDecodeError
        파일 내용이 유효한 JSON 형식이 아닌 경우.
    """
    try:
        with open(file=MCP_SERVERS_PATH, mode="r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        raw_data = {"mcpServers": {}}
    return raw_data


def save_mcp_server(str_input: str):
    """문자열로 된 서버 정보를 `mcp_servers.json` 파일에 추가합니다.

    `load_mcp_server`를 호출하여 현재 설정을 가져온 뒤, 새로운 서버 정보를
    추가하고 파일에 다시 저장합니다.

    Parameters
    ----------
    str_input : str
        JSON 객체의 내용물에 해당하는 문자열.
        예: `"my-server": {"command": ["python", "tool.py"]}`

    Raises
    ------
    ValueError
        입력된 문자열의 JSON 형식이 올바르지 않은 경우.
    IOError
        파일을 쓰는 중 I/O 에러가 발생한 경우.
    """
    # 1. 입력 문자열 파싱 및 유효성 검사
    try:
        new_servers: dict = json.loads("{" + str_input + "}")
    except json.JSONDecodeError as e:
        raise ValueError(
            f"입력된 내용의 JSON 형식이 올바르지 않습니다:\n{e}"
        ) from e

    # 2. 기존 설정 로드
    raw_data = load_mcp_server()

    # 3. 새로운 정보 추가
    if "mcpServers" not in raw_data:
        raw_data["mcpServers"] = {}

    for server_name, server_config in new_servers.items():
        # 기존에 없는 서버만 추가
        if server_name not in raw_data["mcpServers"]:
            raw_data["mcpServers"][server_name] = server_config

    # 4. 파일에 다시 쓰기
    try:
        with open(file=MCP_SERVERS_PATH, mode="w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        raise IOError(
            f"설정 파일({MCP_SERVERS_PATH})에 쓰는 중 오류 발생: {e}"
        ) from e


def set_mcp_server() -> dict:
    """원시 MCP Server 설정을 `MultiServerMCPClient`에 적합한 형태로 변환합니다.

    `load_mcp_server`로 원시 설정 데이터를 가져온 뒤, 각 서버의 연결 방식이
    'command'인지 'url'인지 판별합니다. 그에 따라 'transport' 키에 'stdio'
    또는 'sse' 값을 지정하여 요구하는 형식의 새로운 설정을 생성하여 반환합니다.

    Returns
    -------
    dict
        `MultiServerMCPClient`에 바로 사용할 수 있도록 가공된 서버 설정.
    """
    raw_config = load_mcp_server()
    client_config = {}

    servers = raw_config.get("mcpServers", {})

    for server_name, config_data in servers.items():
        if "command" in config_data:
            client_config[server_name] = {
                "command": config_data.get("command"),
                "args": config_data.get("args", []),
                "env": config_data.get("env", {}),
                "transport": "stdio",
            }
        elif "url" in config_data:
            client_config[server_name] = {
                "url": config_data.get("url"),
                "transport": "sse",
            }
    return client_config


if __name__ == "__main__":
    # 테스트 예시
    try:
        # 새로운 서버 정보 추가 시도
        test_input = '"test-server-1": {"command": ["python", "my_tool.py"]}'
        save_mcp_server(test_input)
        print("서버 정보가 성공적으로 저장되었습니다.")

        # 변환된 설정 출력
        final_config = set_mcp_server()
        print("변환된 설정:")
        print(final_config)
    except (ValueError, IOError, json.JSONDecodeError) as e:
        print(f"오류 발생: {e}")
