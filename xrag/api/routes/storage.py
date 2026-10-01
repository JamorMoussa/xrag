from fastapi import (
    APIRouter, UploadFile, Depends
)
from fastapi.responses import StreamingResponse
from typing import Annotated
from pathlib import Path

from xrag.configs import configs
from xrag.utils import get_object_key
from ..schemas import UploadArgs, DownloadArgs
from ..deps import (
    get_storage_service, generate_uuid, upload_args, download_args
)
from xrag.services.storage import (
    StorageService, File, StorageKey, StorageType
)

storage_router = APIRouter(
    prefix= str(
        Path(configs.API_PREFIX_PATH) / "s"
    )
)


@storage_router.post("/upload")
async def upload(
    args: Annotated[UploadArgs, Depends(upload_args)],
    file: UploadFile,
    storage_service: Annotated[StorageService, Depends(get_storage_service)],
):
    if args.document_id is None:
        document_id = generate_uuid()
    else:
        document_id = args.document_id

    storage_key = StorageKey(
        workspace_id=args.workspace_id,
        document_id=document_id,
        storage_type=StorageType(args.storage_type),
        content_type=file.content_type,
        ext=Path(file.filename).suffix
    )

    storage_file = File(
        content=file.file,
        filename=file.filename,
        content_type=file.content_type
    )

    key = storage_service.upload(
        file=storage_file, storage_key=storage_key
    )

    return {
        "document_id": document_id,
        "key": key
    }

# TODO: handle the error: botocore.errorfactory.NoSuchKey
@storage_router.post("/download")
async def download(
    args: DownloadArgs,
    storage_service: Annotated[StorageService, Depends(get_storage_service)],
):
    name = None 

    if StorageType(args.storage_type) is StorageType.RAW:
        name = args.document_id
    else:
        name = args.storage_type

    key = get_object_key(
        workspace_id=args.workspace_id,
        document_id=args.document_id,
        name=name,
        ext=args.ext
    )

    file = storage_service.download(
        object_key=key
    )

    return StreamingResponse(
        content = file.content, 
        media_type=file.content_type,
        headers={"Content-Disposition": f"attachment; filename={file.filename}"}
    )