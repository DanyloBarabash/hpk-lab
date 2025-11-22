from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from .service import StorageService, get_storage_service

router = APIRouter(prefix="/storage", tags=["Azure Blob Storage"])


@router.post("/files")
async def upload_file(file: UploadFile = File(...), service: StorageService = Depends(get_storage_service)):
    """Upload a file to Azure Blob Storage."""
    try:
        filename = service.upload_file(file)
        return {"message": f"File '{filename}' successfully uploaded to Azure Blob Storage."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files")
async def list_files(service: StorageService = Depends(get_storage_service)):
    """Return a list of all files in the container."""
    try:
        return {"files": service.list_files()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/{filename}")
async def download_file(filename: str, service: StorageService = Depends(get_storage_service)):
    """Read and return the content of a file."""
    try:
        content = service.download_file(filename)
        return {"filename": filename, "content": content}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/files/{filename}")
async def delete_file(filename: str, service: StorageService = Depends(get_storage_service)):
    """Delete a file from Azure Blob Storage."""
    try:
        service.delete_file(filename)
        return {"message": f"File '{filename}' successfully deleted from Azure Blob Storage."}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
