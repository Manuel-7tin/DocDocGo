from pathlib import Path
import json

from platformdirs import user_config_dir


APP_NAME = "docdocpy"


def get_config_path() -> Path:
    config_dir = Path(user_config_dir(APP_NAME))
    config_dir.mkdir(parents=True, exist_ok=True)

    return config_dir / "config.json"


def save_api_key(api_key: str) -> None:
    config_path = get_config_path()

    config_path.write_text(
        json.dumps({"api_key": api_key}),
        encoding="utf-8",
    )


def get_api_key() -> str | None:
    config_path = get_config_path()

    if not config_path.exists():
        return None

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    return data.get("api_key")