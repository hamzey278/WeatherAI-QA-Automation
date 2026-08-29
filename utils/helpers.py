import json
from pathlib import Path
from typing import Any


def load_schema(schema_name: str) -> dict[str, Any]:
    """Loads a JSON schema file from the schemas directory."""
    schemas_dir = Path(__file__).resolve().parent.parent / "schemas"
    schema_file = schemas_dir / schema_name
    if not schema_file.exists():
        raise FileNotFoundError(f"JSON Schema file not found: {schema_file}")

    with open(schema_file, "r", encoding="utf-8") as f:
        return json.load(f)
