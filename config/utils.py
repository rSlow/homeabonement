import os

ENV_PARAMS = [
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DJANGO_DEBUG",
    "SECRET_KEY",
    "ALLOWED_HOSTS",
]


def check_env() -> None:
    for param in ENV_PARAMS:
        if os.getenv(param) is None:
            raise RuntimeError(f"{param} environment parameter expected, but not passed")
