from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False
    )

    token: str
    #token: str = 'YOUR TOKEN'
    admin_ids: frozenset[int] = frozenset({1059897141})
    teacher_ids: set[int] = set()
    council_ids: set[int] = set()
    user_ids: set[int] = set()

    roles: ClassVar[list[str]] = ['admin', 'teacher', 'council', 'user']


settings = Settings()
