import json


def load_mcp_config():
    """현재 디렉토리의 MCP 설정 파일을 로드"""
    try:
        with open(file="./mcp_servers.json", mode="r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"설정 파일을 읽는 중 오류 발생: {str(e)}")
        return None


def set_mcp_config():
    """MCP 서버 설정을 생성"""
    config = load_mcp_config()
    server_config = {}

    if config.get("mcpServers", None) is None:
        return server_config

    config = config.get("mcpServers")
    for server_name, server_config_data in config.items():
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
    print(set_mcp_config())
