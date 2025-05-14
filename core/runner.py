# core/runner.py

from typing import Callable, Any
from core.schemas import ExecutionResult as SchemaResult

PLUGINS: dict[str, Callable[[dict], SchemaResult]] = {}

def register_plugin(name: str):
    def decorator(fn: Callable[[dict], SchemaResult]):
        PLUGINS[name] = fn
        return fn
    return decorator

def run_plugin(key: str, payload: dict) -> SchemaResult:
    if key not in PLUGINS:
        return SchemaResult(success=False, outputs={"error": f"No plugin '{key}'"})
    try:
        return PLUGINS[key](payload)
    except Exception as e:
        return SchemaResult(success=False, outputs={"error": str(e)})
