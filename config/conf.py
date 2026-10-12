import os
from pathlib import Path
from dotenv import load_dotenv

# Try loading .env, fallback to dev.env if present
for env_file in [".env", "dev.env"]:
    env_path = Path(env_file)
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path)
        break

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "authorization, Content-Type, X-Requested-With",
}


def get_env_var(key: str, default=None):
    """Get an environment variable with an optional default."""
    return os.getenv(key, default)

