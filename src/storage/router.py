from fastapi import APIRouter, UploadFile, File, HTTPException
from .service import StorageService

router = APIRouter(prefix="/storage", tags=["Azure Blob Storage"])
service = StorageService()


@router.post("/files")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to Azure Blob Storage."""
    try:
        filename = service.upload_file(file)
        return {"message": f"File '{filename}' successfully uploaded to Azure Blob Storage."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files")
async def list_files():
    """Return a list of all files in the container."""
    try:
        return {"files": service.list_files()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/{filename}")
async def download_file(filename: str):
    """Read and return the content of a file."""
    try:
        content = service.download_file(filename)
        return {"filename": filename, "content": content}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/files/{filename}")
async def delete_file(filename: str):
    """Delete a file from Azure Blob Storage."""
    try:
        service.delete_file(filename)
        return {"message": f"File '{filename}' successfully deleted from Azure Blob Storage."}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
