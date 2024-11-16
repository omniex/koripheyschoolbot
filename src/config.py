from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False
    )

    token: str
    admin_ids: frozenset[int] = frozenset({1059897141})
    moderator_ids: set[int] = set()
    teacher_ids: frozenset[int] = frozenset({1059897141})


settings = Settings()