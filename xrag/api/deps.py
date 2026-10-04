from fastapi import FastAPI, Depends, Form
from typing import Annotated, Literal
from uuid import uuid4

from xrag.services.storage import (
    S3StorageService, StorageService, PathObject
)
from xrag.services.retrieve import RetrievalService
from xrag.configs import Configs, get_configs


def generate_uuid() -> str:
    return uuid4().hex

def get_storage_service(
    configs: Annotated[Configs, Depends(get_configs)]
) -> StorageService:
    return S3StorageService(configs=configs)

def get_retrieve_service(
    configs: Annotated[Configs, Depends(get_configs)]
) -> RetrievalService:
    return RetrievalService(configs=configs)

def path_args(
    workspace_id: Annotated[str, Form()],
    document_type: Annotated[
        Literal["raw", "parsed", "chunked", "manifest"] | None, Form()
    ] = "raw",
    document_id: Annotated[str | None, Form()] = None,
) -> PathObject:
    
    return PathObject(
        workspace_id=workspace_id,
        document_type=document_type,
        document_id=document_id,
    )