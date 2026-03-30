from typing import Union

from pydantic_settings import BaseSettings

from stalecheck.settings.dev import DevSettings

available_settings = {
    "dev": DevSettings(),
}


def get_settings(env: str) -> Union[DevSettings, BaseSettings]:
    settings = available_settings.get(env, None)
    if settings is None:
        raise ValueError(f"'{env}' is not a valid environment")

    return settings
