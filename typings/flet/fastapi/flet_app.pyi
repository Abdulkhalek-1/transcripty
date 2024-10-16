"""
This type stub file was generated by pyright.
"""

import asyncio
from typing import List, Optional
from fastapi import WebSocket
from flet_core.local_connection import LocalConnection
from flet_core.protocol import Command

logger = ...
DEFAULT_FLET_SESSION_TIMEOUT = ...
DEFAULT_FLET_OAUTH_STATE_TIMEOUT = ...
class FletApp(LocalConnection):
    def __init__(self, loop: asyncio.AbstractEventLoop, session_handler, session_timeout_seconds: int = ..., oauth_state_timeout_seconds: int = ..., upload_endpoint_path: Optional[str] = ..., secret_key: Optional[str] = ...) -> None:
        """
        Handle Flet app WebSocket connections.

        Parameters:

        * `session_handler` (Coroutine) - application entry point - an async method called for newly connected user. Handler coroutine must have 1 parameter: `page` - `Page` instance.
        * `session_timeout_seconds` (int, optional) - session lifetime, in seconds, after user disconnected.
        * `oauth_state_timeout_seconds` (int, optional) - OAuth state lifetime, in seconds, which is a maximum allowed time between starting OAuth flow and redirecting to OAuth callback URL.
        * `upload_endpoint_path` (str, optional) - absolute URL of upload endpoint, e.g. `/upload`.
        * `secret_key` (str, optional) - secret key to sign upload requests.
        """
        ...
    
    async def handle(self, websocket: WebSocket): # -> None:
        """
        Handle WebSocket connection.

        Parameters:

        * `websocket` (WebSocket) - Websocket instance.
        """
        ...
    
    def send_command(self, session_id: str, command: Command): # -> PageCommandResponsePayload:
        ...
    
    def send_commands(self, session_id: str, commands: List[Command]): # -> PageCommandsBatchResponsePayload:
        ...
    
    def dispose(self): # -> None:
        ...
    


