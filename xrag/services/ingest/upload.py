from fastapi import UploadFile, HTTPException
from pathlib import Path
import uuid

from ..storage.base import StorageService

class UploadService:

    def __init__(
        self, 
        sts: StorageService
    ):
        self.sts = sts

    @property
    def configs(self):
        return self.sts.configs

    async def upload(
        self, 
        project_id: str, 
        file: UploadFile
    ):
        self.is_valid_file(file=file)

        object_key = self._generate_key(
            project_id=project_id, file=file
        )

        await self.sts.upload(
            object_key= object_key,
            fileobj=file.file,
            content_type=file.content_type
        )

        return object_key


    def is_valid_file(
        self, 
        file: UploadFile
    ):
        if (
            file.content_type not in self.configs.FILE_ALLOWED_TYPES
        ):
            raise HTTPException(
                status_code=415,
                detail="Unsupported Document Type"
            )

        if file.size > (self.configs.FILE_MAX_SIZE * 1048576):
            raise HTTPException(
                status_code=413,
                detail="File Too Large (>10MB)"
            )

    def _generate_key(
        self, project_id: str, file: UploadFile
    ):
        ext = Path(file.filename).suffix.lower()
        key = f"{project_id}/{str(uuid.uuid4())}.{ext}"

        return key 
