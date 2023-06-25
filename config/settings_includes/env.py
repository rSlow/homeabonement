from pathlib import Path

from environs import Env


def get_env(env_dir: Path):
    env = Env()
    env_files = [
        "django.env",  # base
        "mysql.env",  # database
        "smtp.env",  # email
        "yookassa.env",  # payments
        "yookassa_net.env",  # yookassa ips
    ]
    for env_file in env_files:
        env.read_env(str(env_dir / env_file))

    return env
