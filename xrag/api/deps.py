from fastapi import FastAPI, Depends, Form
from typing import Annotated, Literal
from uuid import uuid4

from xrag.services.storage import S3StorageService, StorageService
from xrag.configs import Configs, get_configs
from .schemas import UploadArgs, DownloadArgs


def upload_args(
    workspace_id: Annotated[str, Form()],
    storage_type: Annotated[
        Literal["raw", "parsed", "chunks"] | None, Form()
    ] = "raw",
    document_id: Annotated[str | None, Form()] = None,
) -> UploadArgs:
    
    return UploadArgs(
        workspace_id=workspace_id,
        storage_type=storage_type,
        document_id=document_id,
    )

def download_args(
    workspace_id: Annotated[str, Form()],
    storage_type: Annotated[
        Literal["raw", "parsed", "chunks"] | None, Form()
    ] = None,
    document_id: Annotated[str | None, Form()] = None,
) -> DownloadArgs:
    
    return DownloadArgs(
        workspace_id=workspace_id,
        storage_type=storage_type,
        document_id=document_id,
    )

def generate_uuid() -> str:
    return uuid4().hex

def get_storage_service(
    configs: Annotated[Configs, Depends(get_configs)]
) -> StorageService:
    return S3StorageService(configs=configs)