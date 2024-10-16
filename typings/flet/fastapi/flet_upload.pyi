"""
This type stub file was generated by pyright.
"""

from typing import Optional
from fastapi import Request

logger = ...
class FletUpload:
    """
    Flet app uploads handler.

    Parameters:

    * `upload_dir` (str) - an absolute path to a directory with uploaded files.
    * `max_upload_size` (str, int) - maximum size of a single upload, bytes. Unlimited if `None`.
    * `secret_key` (str, optional) - secret key to sign and verify upload requests.
    """
    def __init__(self, upload_dir: str, max_upload_size: Optional[int] = ..., secret_key: Optional[str] = ...) -> None:
        ...
    
    async def handle(self, request: Request): # -> None:
        ...
    


