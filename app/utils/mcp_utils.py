import json

MCP_SERVERS_PATH = "./mcp_servers.json"


def save_mcp_server(str_input: str):
    """현재 디렉토리의 MCP 설정 파일에 저장"""
    server: dict = json.loads("{" + str_input + "}")
    server_names = server.keys()

    try:
        with open(file=MCP_SERVERS_PATH, mode="r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        return f"설정 파일을 읽는 중 오류 발생: {str(e)}"

    try:
        with open(file=MCP_SERVERS_PATH, mode="w", encoding="utf-8") as f:
            if raw_data.get("mcpServers", None) is None:
                raw_data["mcpServers"] = {}
            for server_name in server_names:
                if not raw_data["mcpServers"].get(server_name, False):
                    raw_data["mcpServers"][server_name] = server[server_name]

            return json.dump(raw_data, f)

    except Exception as e:
        return f"설정 파일을 추가하는 중 오류 발생: {str(e)}"


def load_mcp_server():
    """현재 디렉토리의 MCP 설정 파일을 로드"""
    try:
        with open(file=MCP_SERVERS_PATH, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return f"설정 파일을 읽는 중 오류 발생: {str(e)}"


def set_mcp_server():
    """MCP 서버 설정을 생성"""
    server = load_mcp_server()
    server_config = {}

    if server.get("mcpServers", None) is None:
        return server_config

    server = server.get("mcpServers")
    for server_name, server_config_data in server.items():
        # command가 있으면 stdio 방식
        if "command" in server_config_data:
            server_config[server_name] = {
                "command": server_config_data.get("command"),
                "args": server_config_data.get("args", []),
                "env": server_config_data.get("env", {}),
                "transport": "stdio",
            }
        # url이 있으면 sse 방식
        elif "url" in server_config_data:
            server_config[server_name] = {
                "url": server_config_data.get("url"),
                "transport": "sse",
            }

    return server_config


if __name__ == "__main__":
    print(set_mcp_server())
