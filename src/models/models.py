from sqlmodel import Field, SQLModel
from datetime import datetime


class FileMetadata(SQLModel, table=True):
    name: str = Field(default="", title="File Name", max_length=255)
    content_md5: str = Field(
        primary_key=True, title="MD5 Hash", unique=True, max_length=32
    )
    last_modified: datetime = Field(
        default_factory=datetime.now(datetime.timezone.utc),
        title="Last Modified Timestamp",
    )
