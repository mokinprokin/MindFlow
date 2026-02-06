from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    DB_PATH: str

    @property
    def DB_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.DB_PATH}"

    SYNC_START_HOUR: int
    SYNC_END_HOUR: int
    SYNC_CHECK_INTERVAL: int

    PRIMARY_COLOR: str
    SECONDARY_COLOR: str
    ACCENT_COLOR: str
    TEXT_COLOR: str
    TEXT_SECONDARY: str
    CHECKBOX_COLOR: str

    CLIENT_ID:str
    CLIENT_SECRET:str
    TOKEN_URI:str
    SCOPES:list[str]
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
