"""Application settings persistence."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Session, SQLModel, create_engine, select


class AppSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    local_llm_endpoint: str = "http://localhost:11434"
    storage_path: str = ".promptspec/app.sqlite"


class SettingRow(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str


class SettingsRepository:
    def __init__(self, database_url: str = "sqlite:///.promptspec/settings.sqlite") -> None:
        if database_url.startswith("sqlite:///"):
            db_path = Path(database_url.removeprefix("sqlite:///"))
            if str(db_path) != ":memory:":
                db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(database_url)
        SQLModel.metadata.create_all(self.engine)

    def get(self) -> AppSettings:
        values: dict[str, str] = {}
        with Session(self.engine) as session:
            for row in session.exec(select(SettingRow)):
                values[row.key] = row.value
        return AppSettings(**values)

    def update(self, settings: AppSettings) -> AppSettings:
        with Session(self.engine) as session:
            for key, value in settings.model_dump().items():
                row = session.get(SettingRow, key) or SettingRow(key=key, value=str(value))
                row.value = str(value)
                session.add(row)
            session.commit()
        return self.get()

