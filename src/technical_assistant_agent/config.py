from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding= "utf-8"
    )

    ollama_base_url: str
    ollama_model: str

    mcp_server_url: str

    max_agent_iterations: int = 8
    max_tool_calls: int = 20