import uvicorn
from xrag.api import xrag_api


if __name__ == "__main__":
    uvicorn.run("main:xrag_api", host="127.0.0.1", port=8000, reload=True)