import inspect
from typing import Any


def build_operation_extensions(extensions: list[Any]) -> list[Any]:
    """Build a fresh, isolated set of extensions for a single operation.

    Only extensions that are either pre-constructed instances or
    zero-argument classes (optionally accepting execution_context) are
    fully supported. Class-based extensions requiring custom constructor
    arguments should be passed as pre-constructed instances.

    Full extension lifecycle support (on_operation, on_execute, etc.)
    for subscriptions should be tracked as a separate issue.
    """
    instances = []
    for ext in extensions:
        if isinstance(ext, type):
            sig = inspect.signature(ext.__init__)
            if "execution_context" in sig.parameters:
                extension_instance = ext(execution_context=None)
            else:
                extension_instance = ext()

            extension_instance.execution_context = None
            instances.append(extension_instance)
        else:
            instances.append(ext)
    return instances
