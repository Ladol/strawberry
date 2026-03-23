from typing import Any

from strawberry.types import ExecutionResult


def process_extensions(
    execution_result: ExecutionResult, extensions: list[Any]
) -> None:
    """Run the execution result through active schema extensions."""
    for ext in extensions:
        extension_instance = ext(execution_context=None) if isinstance(ext, type) else ext

        if hasattr(extension_instance, "_process_result"):
            extension_instance._process_result(execution_result)
