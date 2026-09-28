from pypdf import PdfReader, PdfWriter
from io import BytesIO
from pathlib import Path
import asyncio
import httpx

from llama_index.core import Document

from xrag.configs import Configs

class LiteParserService:

    def __init__(
        self, configs: Configs
    ):
        self.configs = configs

        self.client = httpx.AsyncClient(
            base_url=self.configs.LITE_PARSER_BASE_URL,
            timeout=120.0
        )

    async def parse(
        self,
        content: bytes,
        filename: str,
        content_type: str,
    ) -> list[Document]:
        
        if content_type.split(";")[0].strip().lower() != "application/pdf":
            raise ValueError("Per-page Markdown currently supports PDFs only.")

        def split_pages() -> list[bytes]:
            reader = PdfReader(BytesIO(content))
            result = []

            for page in reader.pages:
                writer = PdfWriter()
                writer.add_page(page)

                with BytesIO() as buffer:
                    writer.write(buffer)
                    result.append(buffer.getvalue())

                writer.close()

            return result

        pdf_pages = await asyncio.to_thread(split_pages)
        pages = []
        name = Path(filename).stem

        for index, page_content in enumerate(pdf_pages):
            response = await self.client.post(
                "/parse",
                params={"markdown": "true"},
                files={
                    "file": (
                        f"{name}-page-{index + 1}.pdf",
                        page_content,
                        "application/pdf",
                    )
                },
                timeout=120.0,
            )
            response.raise_for_status()

            pages.append({
                "page": index,
                "markdown": response.text,
            })

        return [
            Document(
                text=f["markdown"],
                metadata={
                    "filename": Path(filename), "page": f["page"]
                }       
            ) for f in pages
        ]
    
    async def close(self):
        await self.client.aclose()
        