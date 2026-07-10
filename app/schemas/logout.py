from typing import Optional

from pydantic import BaseModel


class LogoutRequest(BaseModel):

    access_token: str

    refresh_token: Optional[str] = None