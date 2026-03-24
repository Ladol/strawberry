import inspect
from typing import Any

from strawberry.types import ExecutionResult


def process_extensions(
    execution_result: ExecutionResult, extensions: list[Any]
) -> None:
    """Run the execution result through active schema extensions."""
    for ext in extensions:
        if isinstance(ext, type):
            # Inspect the constructor to see if it requires execution_context
            sig = inspect.signature(ext.__init__)
            if "execution_context" in sig.parameters:
                extension_instance = ext(execution_context=None)
            else:
                extension_instance = ext()

            # Explicitly set this ONLY for newly constructed instances
            extension_instance.execution_context = None
        else:
            extension_instance = ext

        if hasattr(extension_instance, "_process_result"):
            extension_instance._process_result(execution_result)
