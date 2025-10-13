from azure.core.exceptions import ResourceNotFoundError
from .config import azure_config


class StorageService:
    """Business logic for working with Azure Blob Storage."""

    def __init__(self):
        self.container_client = azure_config.container_client

    def upload_file(self, file):
        """Upload file to Azure container."""
        blob_client = self.container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file.file, overwrite=True)
        return file.filename

    def list_files(self):
        """List all blobs in the container."""
        return [blob.name for blob in self.container_client.list_blobs()]

    def download_file(self, filename: str) -> str:
        """Download the content of a file by name."""
        blob_client = self.container_client.get_blob_client(filename)
        try:
            stream = blob_client.download_blob()
            return stream.readall().decode("utf-8", errors="ignore")
        except ResourceNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found")

    def delete_file(self, filename: str):
        """Delete a file from the container."""
        blob_client = self.container_client.get_blob_client(filename)
        try:
            blob_client.delete_blob()
        except ResourceNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found")
