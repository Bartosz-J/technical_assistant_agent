from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding= "utf-8"
    )

    ollama_host: str = 'http://localhost:11434'
    ollama_model: str = 'gpt-oss:20b'#'gpt-oss:20b'# #'gemma4:latest'
    ollama_max_num_predict: int = 4096      # to jest niby max dlugosc odpowiedzi - po przekroczeniu go odpowiedz jest ucinana!
    ollama_max_context_length: int =  16384 # max dlugosc calego kontekstu
    ollama_model_temperature: float = 0.2

    mcp_server_url: str = 'http://127.0.0.1:8000/mcp/'

    max_agent_iterations: int = 8
    max_tool_calls: int = 20

settings = Settings()