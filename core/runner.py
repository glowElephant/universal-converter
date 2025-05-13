from typing import Dict, Any

# 플러그인 등록을 위한 레지스트리
PLUGINS: Dict[str, Any] = {}

def register_plugin(key: str):
    """
    @register_plugin('youtube') 처럼 데코레이터로 쓰이며,
    PLUGINS 딕셔너리에 함수 참조를 저장합니다.
    """
    def decorator(func):
        PLUGINS[key] = func
        return func
    return decorator

def run_plugin(key: str, payload: Any) -> Any:
    """
    run_plugin('youtube', payload) 호출 시,
    PLUGINS 레지스트리에서 해당 함수를 찾아 실행합니다.
    """
    if key not in PLUGINS:
        raise ValueError(f"Unknown plugin: {key}")
    return PLUGINS[key](payload)
