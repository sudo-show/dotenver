import os
import json
import datetime as dt
from dotenv import load_dotenv

_env_loaded = False

def _ensure_loaded():
    global _env_loaded
    if not _env_loaded:
        load_dotenv()
        _env_loaded = True

_MISSING = object()
_TRUE  = {"1", "true", "yes", "y", "on"}
_FALSE = {"0", "false", "no", "n", "off"}

def _to_bool(raw):
    v = raw.strip().lower()
    if v in _TRUE:  return True
    if v in _FALSE: return False
    raise ValueError(f"Expected a boolean.")


_CASTS = {
    "str":      str,
    "int":      int,
    "float":    float,
    "bool":     _to_bool,
    "json":     json.loads,
    "date":     dt.date.fromisoformat,
    "time":     dt.time.fromisoformat,
    "datetime": dt.datetime.fromisoformat,
}

def getenv(name: str, default=_MISSING, cast: str = "str"):
    """Read an environment variable, converted to the type you ask for.

    The .env file is loaded once, on the first call.

    name    -- variable to read.
    default -- value to return when the variable is unset or empty. Omit it
               to make the lookup strict: a missing variable raises instead.
               Returned as given, without conversion.
    cast    -- one of "str", "int", "float", "bool", "json". Applied only to
               values that actually came from the environment.

    A variable set to an empty string counts as missing.

    "bool" accepts 1/true/yes/y/on and 0/false/no/n/off, case-insensitively;
    the builtin `bool` is not used, since every non-empty string is truthy
    and `bool("false")` would be True.

    Raises ValueError when the variable is missing and no default was given,
    when the value doesn't convert, or when `cast` isn't a known name.
    """
    _ensure_loaded()

    if cast not in _CASTS:
        raise ValueError(f"Unknown cast {cast!r}; expected one of {sorted(_CASTS)}.")

    raw = os.getenv(name)
    if not raw:
        if default is _MISSING:
            raise ValueError(f"Environment variable `{name}` not found.")
        return default

    try:
        return _CASTS[cast](raw)
    except (ValueError, TypeError) as e:
        raise ValueError(f"`{name}` is not a valid {cast}") from e