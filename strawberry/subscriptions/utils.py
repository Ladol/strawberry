from typing import Any

from strawberry.types import ExecutionResult


def process_extensions(
    execution_result: ExecutionResult, extensions: list[Any]
) -> None:
    """Run the execution result through active schema extensions."""
    for ext in extensions:
        if isinstance(ext, type):
            try:
                # Try passing the context for extensions like ApolloTracing
                extension_instance = ext(execution_context=None)
            except TypeError:
                # Fallback for extensions like MaskErrors that don't want it
                extension_instance = ext()

            # Explicitly set this ONLY for newly constructed instances
            extension_instance.execution_context = None
        else:
            extension_instance = ext

        if hasattr(extension_instance, "_process_result"):
            extension_instance._process_result(execution_result)
