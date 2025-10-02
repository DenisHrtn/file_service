import mimetypes

from application.interfaces.get_content_type import IGetContentType


class GetContentTypeService(IGetContentType):
    async def get_content_type(self, content: str) -> str:
        content_type, _ = mimetypes.guess_type(content)
        return content_type or "application/octet-stream"
