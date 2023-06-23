import sys
import os
import subprocess
from pathlib import Path

from config.utils import check_env

BASE_DIR = Path(__file__).resolve().parent

INTERP = os.path.expanduser(BASE_DIR / "venv" / "bin" / "python3")

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

from environs import Env
ENV = Env()
ENV.read_env(str(BASE_DIR / "env" / "mysql.env"))
ENV.read_env(str(BASE_DIR / "env" / "django.env"))

check_env()

DJANGO_DEBUG = ENV.bool("DJANGO_DEBUG", default=False)
if DJANGO_DEBUG is False:
    subprocess.run(["python3", "manage.py", "collectstatic", "--clear", "--noinput"])

from config.wsgi import application
