import sys
import os
import subprocess
from pathlib import Path

from config.utils import check_env

BASE_DIR = Path(__file__).resolve().parent

INTERP = os.path.expanduser(BASE_DIR / "venv" / "bin" / "python3")

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

from dotenv import load_dotenv

load_dotenv(BASE_DIR / "env" / "mysql.env")
load_dotenv(BASE_DIR / "env" / "django.env")

check_env()

DJANGO_DEBUG = bool(int(os.getenv("DJANGO_DEBUG", 0)))
if DJANGO_DEBUG is False:
    subprocess.run(["python3", "manage.py", "collectstatic", "--clear", "--noinput"])

from config.wsgi import application
