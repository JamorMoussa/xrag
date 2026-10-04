from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError
from io import BytesIO
import boto3
import json 

from .base import (
    StorageService, FileObject, PathObject
)
from .base import Manifest, Artifact, ArtifactType
from xrag.configs import Configs



class S3StorageService(StorageService):

    # TODO: Delegate manifest management to a dedicated class.

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__(configs=configs)
        
        self.client = boto3.client(
            "s3", 
            endpoint_url=self.configs.S3_ENDPOINT_URL,
            aws_access_key_id=self.configs.S3_ACCESS_KEY,
            aws_secret_access_key=self.configs.S3_SECRET_KEY,
            region_name=self.configs.S3_REGION,
            config= BotoConfig(
                signature_version=self.configs.S3_SIGNATURE_VERSION
            )
        )

    def save(
        self, 
        file: FileObject, 
        path: PathObject, 
    ):
        extra_args = {}

        if content_type := file.content_type:
            extra_args["ContentType"] = content_type

        manifest: Manifest | None = None 

        # Load old Manifest:
        if path.is_new:
            manifest = Manifest(
                workspace_id=path.workspace_id, document_id=path.document_id
            )
        else:
            manifest = self.load_manifest(path=path)
 
        # Save the object File: 
        self.client.upload_fileobj(
            Fileobj=BytesIO(file.content),
            Bucket=self.configs.S3_BUCKET,
            Key=path.key,
            ExtraArgs=extra_args or None,
        )

        manifest.add_artifact(
            artifact=Artifact(
                type_=ArtifactType(path.document_type), 
                filename=file.filename,
                content_type=file.content_type
            )
        )

        # Update Manifest: 
        self.save_manifest(
            path=path, manifest=manifest
        )
        

    def load(
        self,
        path: PathObject
    ) -> FileObject:

        manifest = self.load_manifest(path=path)

        if path.document_type == "manifest":

            file = FileObject(
                content=manifest.asbytes(),
                filename=path.filename,
                content_type=manifest.content_type
            )

            return file

        response = self.client.get_object(
            Bucket=self.configs.S3_BUCKET,
            Key=path.key,
        )

        body = response["Body"]

        return FileObject(
            content=body.read(),
            filename=manifest.artifacts[ArtifactType(path.document_type)].filename,
            content_type=response.get("ContentType"),
        )

    def load_manifest(
        self, 
        path: PathObject
    ) -> Manifest:

        manifest_path = (
            path.model_copy(update={
                "document_type": "manifest"
            })
        )

        response = self.client.get_object(
            Bucket=self.configs.S3_BUCKET,
            Key=manifest_path.key,
        )

        body = response["Body"]

        file = FileObject(
            content=body.read(),
            filename=manifest_path.filename,
            content_type=response.get("ContentType"),
        )

        return Manifest(**json.loads(file.content))


    def save_manifest(
        self, 
        path: PathObject,
        manifest: Manifest
    ):
        
        manifest_path = (
            path.model_copy(update={
                "document_type": "manifest"
            })
        )

        self.client.upload_fileobj(
            Fileobj=BytesIO(
                manifest.model_dump_json().encode("utf-8")
            ),
            Bucket=self.configs.S3_BUCKET,
            Key=manifest_path.key,
        )

    def raw_exists(
        self, path: PathObject
    ) -> bool:
        try:
            self.client.head_object(Bucket=self.configs.S3_BUCKET, Key=path.key)
        except ClientError as e:
            return False

        return True