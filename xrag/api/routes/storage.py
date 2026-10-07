from fastapi import (
    APIRouter, UploadFile, Depends, Form
)
from fastapi.responses import StreamingResponse
from botocore.exceptions import ClientError
from typing import Annotated, Literal
from pathlib import Path
from io import BytesIO

from xrag.configs import configs
from xrag.services.storage import (
    PathObject, FileObject
)
from xrag.deps import StorageDep
from xrag.exceptions import DocumentNotFoundError

storage_router = APIRouter(
    prefix= str(
        Path(configs.API_PREFIX_PATH) / "s"
    )
)

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

@storage_router.post("/upload")
async def upload(
    path: Annotated[PathObject, Depends(path_args)],
    file: UploadFile,
    storage_service: StorageDep,
):  
    try:
        storage_service.save(
            file=FileObject(
                content=await file.read(), 
                filename=file.filename,
                content_type=file.content_type
            ),
            path=path
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]

        if error_code == "NoSuchKey":
            raise DocumentNotFoundError(
                key=path.key
            ) from exc

        raise

    return {
        "message": "ok", 
        "key": path.key 
    }


@storage_router.post("/download")
async def download(
    path: PathObject,
    storage_service: StorageDep,
) -> StreamingResponse:
    try:
        file = storage_service.load(path=path)
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]

        if error_code == "NoSuchKey":
            raise DocumentNotFoundError(
                key=path.key
            ) from exc

        raise

    return StreamingResponse(
        content=BytesIO(file.content),
        media_type=file.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{file.filename}"'
        }
    )
