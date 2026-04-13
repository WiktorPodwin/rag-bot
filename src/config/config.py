import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, BaseModel, computed_field


class DatabaseConfig(BaseModel):
    """
    Configuration for PostgreSQL database connection.
    """

    POSTGRES_USER: str = Field(..., description="Database username")
    POSTGRES_PASSWORD: SecretStr = Field(..., description="Database password")
    POSTGRES_HOST: str = Field(..., description="Database host address")
    POSTGRES_PORT: int = Field(5432, description="Database port")
    POSTGRES_DB: str = Field(..., description="Database name")

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> SecretStr:
        """
        Constructs SQLAlchemy database URI.
        """
        return SecretStr(
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD.get_secret_value()}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


class AzureConfig(BaseModel):
    """
    Configuration for Azure Blob Storage.
    """

    ACCOUNT_NAME: str = Field(..., description="Azure storage account name")
    ACCOUNT_KEY: SecretStr = Field(..., description="Azure storage account key")
    CONTAINER_NAME: str = Field(..., description="Azure blob container name")

    @computed_field
    @property
    def AZURE_STORAGE_CONNECTION_STRING(self) -> SecretStr:
        """
        Constructs Azure storage connection string.
        """
        return SecretStr(
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={self.ACCOUNT_NAME};"
            f"AccountKey={self.ACCOUNT_KEY.get_secret_value()};"
            f"EndpointSuffix=core.windows.net"
        )


class LLMConfig(BaseModel):
    """
    Configuration for language model provider.
    """

    OPENAI_API_KEY: SecretStr = Field(..., description="OpenAI API key")


class RAGConfig(BaseModel):
    """
    Configuration for RAG pipeline and text processing.
    """

    IMAGE_RESOLUTION_SCALE: float = Field(
        2.5, description="Scale factor for extracted image resolution"
    )
    NUMBER_OF_THREADS: int | None = Field(
        default_factory=os.cpu_count, description="Number of CPU threads to use"
    )

    MIN_CHUNK_LENGTH: int = Field(300, description="Minimum length of text chunks")
    MAX_CHUNK_LENGTH: int = Field(1000, description="Maximum length of text chunks")
    PERCENTILE_THRESHOLD: int = Field(
        98, description="Percentile threshold for semantic chunk splitting"
    )


class AppConfig(BaseModel):
    """
    General application configuration.
    """

    APP_PORT: int = Field(8000, description="Port on which the app runs")

    @computed_field
    @property
    def BASE_DIR(self) -> str:
        """
        Base directory of the project.
        """
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    @computed_field
    @property
    def EMBEDDER_DIR(self) -> str:
        """
        Path to embedding model directory.
        """
        return os.path.join(self.BASE_DIR, "checkpoints/BAAI/bge-small-en")

    @computed_field
    @property
    def DATA_DIR(self) -> str:
        """
        Path to data directory.
        """
        return os.path.join(self.BASE_DIR, "data")


class Settings(BaseSettings):
    """
    Main application settings loaded from environment variables.
    Combines all configuration domains into a single object.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_ignore_empty=True,
        extra="ignore",
    )

    db: DatabaseConfig
    azure: AzureConfig
    llm: LLMConfig
    rag: RAGConfig = RAGConfig()
    app: AppConfig = AppConfig()


base_settings = Settings()
