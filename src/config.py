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
    banned_ids: set[int] = set()
    pending_users: set[int] = set()
    rejected_users: set[int] = set()
    approved_users: set[int] = {1059897141}

    not_completed_tickets: set[int] = set()
    in_work_tickets: set[int] = set()
    completed_tickets: set[int] = set()

    roles: ClassVar[list[str]] = ['admin', 'teacher', 'council', 'user', 'banned']
    statuses: ClassVar[list[str]] = ['pending', 'approved', 'rejected']
    statuses_ticket: ClassVar[list[str]] = ['new', 'in work', 'completed', 'not completed', 'rejected']


settings = Settings()
