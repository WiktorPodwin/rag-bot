from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class FileMetadata(SQLModel, table=True):
    """
    Represents metadata for a file stored in the system

    Attributes:
        content_md5 (str): The MD5 hash of the file, uses as a unique identifier.
        name (str): The name of the file.
        last_modified (datetime): The timestamp of when the file was last modified.
    """

    content_md5: str = Field(
        primary_key=True, title="MD5 Hash", unique=True, min_length=32, max_length=32
    )
    name: str = Field(title="File Name", unique=True, max_length=255)
    last_modified: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Last Modified Timestamp",
    )
