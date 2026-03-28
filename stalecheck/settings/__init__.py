from typing import Union

from pydantic_settings import BaseSettings

from stalecheck.settings.dev import DevSettings


available_settings = {
    "dev": DevSettings(),
}


def get_settings(env: str) -> Union[DevSettings, BaseSettings]:
    """
    Retrieve settings for a specific environment.

    :param env: The environment name (e.g., 'dev').
    :returns: An instance of BaseSettings or its subclass.
    """
    settings = available_settings.get(env)

    if settings is None:
        raise ValueError(f"'{env}' is not a valid environment")

    return settings