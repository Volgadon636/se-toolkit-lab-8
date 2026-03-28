import json
import os
import sys

def main():
    # Use paths relative to the script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    resolved_path = os.path.join(base_dir, "config.resolved.json")
    workspace_path = os.path.join(base_dir, "workspace")

    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found")
        sys.exit(1)

    with open(config_path, "r") as f:
        config = json.load(f)

    # Inject LLM Provider settings
    provider = config.setdefault("providers", {}).setdefault("custom", {})
    provider["apiKey"] = os.environ.get("LLM_API_KEY", provider.get("apiKey", ""))
    provider["apiBase"] = os.environ.get("LLM_API_BASE_URL", provider.get("apiBase", ""))
    
    # Inject Agent defaults
    agents_defaults = config.setdefault("agents", {}).setdefault("defaults", {})
    agents_defaults["model"] = os.environ.get("LLM_API_MODEL", agents_defaults.get("model", ""))
    agents_defaults["workspace"] = workspace_path

    # Inject Gateway settings
    config["gateway"] = config.get("gateway", {})
    config["gateway"]["host"] = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    config["gateway"]["port"] = int(os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790"))

    # Inject MCP Server settings for LMS
    mcp_servers = config.setdefault("tools", {}).setdefault("mcpServers", {})
    
    lms_env = mcp_servers.setdefault("lms", {}).setdefault("env", {})
    lms_env["NANOBOT_LMS_BACKEND_URL"] = os.environ.get("NANOBOT_LMS_BACKEND_URL", "http://backend:8000")
    lms_env["NANOBOT_LMS_API_KEY"] = os.environ.get("NANOBOT_LMS_API_KEY", "")

    # Inject WebChat Channel settings
    channels = config.setdefault("channels", {})
    webchat = channels.setdefault("webchat", {})
    webchat["enabled"] = True
    webchat["host"] = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    webchat["port"] = int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765"))
    webchat["allow_from"] = ["*"]

    # Inject WebChat MCP Server settings
    access_key = os.environ.get("NANOBOT_ACCESS_KEY", "")
    webchat_mcp = mcp_servers.setdefault("webchat", {})
    webchat_mcp["command"] = "python"
    webchat_mcp["args"] = ["-m", "mcp_webchat"]
    webchat_mcp_env = webchat_mcp.setdefault("env", {})
    webchat_mcp_env["NANOBOT_UI_RELAY_URL"] = "http://127.0.0.1:8766"
    webchat_mcp_env["NANOBOT_UI_RELAY_TOKEN"] = access_key

    # Inject Observability MCP Server settings
    obs_mcp = mcp_servers.setdefault("observability", {})
    obs_mcp["command"] = "python"
    obs_mcp["args"] = ["-m", "mcp_obs.server"]
    obs_mcp_env = obs_mcp.setdefault("env", {})
    obs_mcp_env["NANOBOT_VICTORIALOGS_URL"] = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")
    obs_mcp_env["NANOBOT_VICTORIATRACES_URL"] = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")

    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {os.path.abspath(resolved_path)}")
    
    # Change to the base directory so nanobot finds its plugins etc.
    os.chdir(base_dir)
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_path, "--workspace", workspace_path])

if __name__ == "__main__":
    main()
