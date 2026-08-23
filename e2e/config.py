import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

@dataclass(frozen=True, slots=True)
class E2EConfig:
    base_url: str
    admin_username: str
    admin_password: str
    
def load_e2e_config() -> E2EConfig:
    env_values = dotenv_values(ENV_PATH)

    return E2EConfig(
        base_url=(
            os.getenv("E2E_BASE_URL")
            or env_values.get("E2E_BASE_URL")
            or "http://localhost:5173"
        ),
        admin_username=(
            os.getenv("ADMIN_USERNAME")
            or env_values.get("ADMIN_USERNAME")
            or "admin"
        ),
        admin_password=(
            os.getenv("ADMIN_PASSWORD")
            or env_values.get("ADMIN_PASSWORD")
            or "admin"
        ),
    )
    
e2e_config = load_e2e_config()