import os
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()


def get_env_var(name: str, default: Optional[Any] = None) -> str:
    value = os.getenv(name, default=default)

    if not value:
        raise KeyError(f'Environment variable {name} is not found')

    return value
