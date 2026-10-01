
def get_object_key(
    workspace_id: str,
    document_id: str,
    name: str,
    ext: str 
):
    return "/".join([
        workspace_id,
        document_id,
        f"{name}.{ext}"
    ])
    