from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    """
    Manages src.application settings, loading configurations from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    ACCOUNT_NAME: str
    ACCOUNT_KEY: str
    CONTAINER_NAME: str

    @computed_field
    @property
    def AZURE_STORAGE_CONNECTION_STRING(self) -> str:
        return f"DefaultEndpointsProtocol=https;AccountName={self.ACCOUNT_NAME};AccountKey={self.ACCOUNT_KEY};EndpointSuffix=core.windows.net"


Settings.model_rebuild()

settings = Settings()
