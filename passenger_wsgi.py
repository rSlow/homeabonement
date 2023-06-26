import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INTERP = os.path.expanduser(BASE_DIR / "venv" / "bin" / "python3")

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

try:
    from config.wsgi import application
except Exception as ex:
    raise
