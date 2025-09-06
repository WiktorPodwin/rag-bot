from src.operations.storages import (
    ChromaDBOperations,
    DBOperations,
    BlobStorageOperations,
)
from src.app.core import get_session
from src.agent.graphs import agent

from src.upload_pdfs import handle_pdfs

from fastapi import FastAPI, UploadFile
from langserve import add_routes

app = FastAPI(debug=True, version="1.0")

add_routes(app, agent)


@app.post("/remove_all_data")
async def remove_all_data():
    """
    Remove whole data stored in: Azure Blob Storage, ChromaDB and PostgreSQL.
    """
    try:
        blob_oper = BlobStorageOperations()
        blob_oper.delete_all_blobs()

        chroma_oper = ChromaDBOperations()
        chroma_oper.remove_chunks()

        session = get_session()
        db_oper = DBOperations(session=session)
        db_oper.clear_table()
    except Exception as e:
        return {
            "status": "failed",
            "message": f"An error has occurred: {type(e).__name__}: {e}",
        }

    return {
        "status": "success",
        "message": "All data has been removed successfully.",
    }


@app.post("/remove_pdf")
async def remove_pdf(file_name: str):
    """
    Remove the specified PDF from the Azure Blob Storage.

    ## Args:
    **file_name (str):** The name of the file that has to be deleted.
    """
    try:
        blob_oper = BlobStorageOperations()
        blob_oper.delete_blob(file_name)
    except Exception as e:
        return {
            "status": "failed",
            "message": f"An error has occurred: {type(e).__name__}: {e}",
        }

    return {
        "status": "success",
        "message": "The PDF has been removed successfully.",
    }


@app.post("/add_pdf")
async def add_pdf(file: UploadFile):
    """
    Add PDF to the Azure Blob Storage. If in database is already a file
    with the same content or name, it will not add the current file.

    ## Args:
    **file (UploadFile):** The file to upload to the storage.
    """
    try:
        content = await file.read()
        if not content.startswith(b"%PDF-"):
            return {
                "status": "failed",
                "message": "The uploaded file is not a valid PDF.",
            }
        blob_oper = BlobStorageOperations()
        message = blob_oper.add_blob(file.filename, content)

    except Exception as e:
        return {
            "status": "failed",
            "message": f"An error has occurred: {type(e).__name__}: {e}",
        }

    return {
        "status": "warning",
        "message": message,
    }


@app.post("/sync_data")
async def sync_data():
    """
    Synchronizes ChromaDB and PostgreSQL based on changes in PDFs in Azure Blob Storage.
    """
    try:
        handle_pdfs()
    except Exception as e:
        return {
            "status": "failed",
            "message": f"An error has occurred: {type(e).__name__}: {e}",
        }

    return {
        "status": "success",
        "message": "All data has been synchronized successfully.",
    }
