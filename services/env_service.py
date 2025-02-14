import os

from dotenv import load_dotenv

load_dotenv()


def get_env_var(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise KeyError(f'Environment variable {name} is not found')

    return value
