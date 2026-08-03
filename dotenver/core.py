import os
from dotenv import load_dotenv

_env_loaded = False

def _ensure_loaded():
    global _env_loaded
    if not _env_loaded:
        load_dotenv()
        _env_loaded = True

_MISSING = object()

def getenv(name: str, default=_MISSING):
    _ensure_loaded()
    var = os.getenv(name)
    if not var:
        if default is _MISSING:
            raise ValueError(f"Environment variable `{name}` not found.")
        return default
    return var