from src.models import FileMetadata

from sqlmodel import Session, delete
from datetime import datetime

import logging


class DBOperations:
    """
    Handles operations for the PostgreSQL database.
    """

    def __init__(self, session: Session) -> None:
        """
        Initializes the database operations.

        Args:
            session: (Session): Active SQLModel session connected to the database.
        """
        self.session = session

    def clear_table(self) -> None:
        """
        Clears all rows from the FileMetadata table.
        """
        statement = delete(FileMetadata)
        self.session.exec(statement)
        self.session.commit()
        logging.info("Cleared all rows from the FileMetadata table.")

    def create_file_metadata(
        self, name: str, content_md5: str, last_modified: datetime = None
    ) -> None:
        """
        Creates a new record in the FileMetadata table.

        Args:
            name (str): The name of the file.
            content_md5: (str): The MD5 hash of the file content.
            last_modified (datetime): The last modified timestamp of the file.
        """
        if last_modified:
            file_metadata = FileMetadata(
                name=name, content_md5=content_md5, last_modified=last_modified
            )
        else:
            file_metadata = FileMetadata(name=name, content_md5=content_md5)

        self.session.add(file_metadata)
        self.session.commit()
        self.session.refresh(file_metadata)
        return file_metadata

    def get_file_metadata(self, content_md5: bytes) -> FileMetadata:
        """
        Retrieves file's metadata by its MD5 hash.

        Args:
            content_md5: (str): The MD5 hash of the file content.

        Returns:
            FileMetadata: The rtrieved FileMetadata object or None, if not found.
        """
        file_metadata = self.session.get(FileMetadata, content_md5)
        return file_metadata

    def delete_file_metadata(self, content_md5: bytes) -> None:
        """
        Deletes file's metadata by its MD5 hash.

        Args:
            content_md5: (str): The MD5 hash of the file content.
        """
        file_metadata = self.session.get(FileMetadata, content_md5)
        if not file_metadata:
            return
        self.session.delete(file_metadata)
        self.session.commit()
