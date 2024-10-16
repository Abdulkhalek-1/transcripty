"""
This type stub file was generated by pyright.
"""

import uvicorn
from typing import Optional
from flet_core.types import WebRenderer

logger = ...
class WebServerHandle:
    def __init__(self, page_url: str, server: uvicorn.Server) -> None:
        ...
    
    async def close(self): # -> None:
        ...
    


def get_fastapi_web_app(session_handler, page_name: str, assets_dir, upload_dir, web_renderer: Optional[WebRenderer], use_color_emoji, route_url_strategy): # -> FastAPI:
    ...

async def serve_fastapi_web_app(session_handler, host, url_host, port, page_name: str, assets_dir, upload_dir, web_renderer: Optional[WebRenderer], use_color_emoji, route_url_strategy, blocking, on_startup, log_level): # -> WebServerHandle:
    ...

