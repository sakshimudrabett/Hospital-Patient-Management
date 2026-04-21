import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    environment: str
    database_url: str

    @property
    def is_development(self) -> bool:
        return self.environment.lower() == "development"


def _build_settings() -> Settings:
    environment = os.getenv("ENVIRONMENT", "development")
    database_url = os.getenv("DATABASE_URL", "sqlite:///./ehr.db")
    return Settings(environment=environment, database_url=database_url)


settings = _build_settings()