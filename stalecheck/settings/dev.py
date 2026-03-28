from typing import ClassVar

from pydantic_settings import BaseSettings


class DevSettings(BaseSettings):
    REQUEST_TIMEOUT: ClassVar[int] = 5
