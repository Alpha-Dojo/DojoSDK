from typing import Any, Type, TypeVar

try:
    # Pydantic v2
    from pydantic import BaseModel

    PYDANTIC_V1 = False
except ImportError:
    # Pydantic v1 fallback
    from pydantic import BaseModel  # type: ignore[no-redef]

    PYDANTIC_V1 = True

_T = TypeVar("_T", bound=BaseModel)


def model_dump(model: BaseModel, **kwargs: Any) -> dict[str, Any]:
    """Dump model to a dict, compatible across Pydantic v1 and v2."""
    if PYDANTIC_V1:
        return getattr(model, "dict")(**kwargs)  # type: ignore
    else:
        return getattr(model, "model_dump")(**kwargs)


def model_validate(model_cls: Type[_T], obj: Any) -> _T:
    """Validate and construct a model from a dict/object, compatible across Pydantic v1 and v2."""
    if PYDANTIC_V1:
        return getattr(model_cls, "parse_obj")(obj)  # type: ignore
    else:
        return getattr(model_cls, "model_validate")(obj)


def model_construct(model_cls: Type[_T], **kwargs: Any) -> _T:
    """Construct a model without validation, compatible across Pydantic v1 and v2."""
    if PYDANTIC_V1:
        return getattr(model_cls, "construct")(**kwargs)  # type: ignore
    else:
        return getattr(model_cls, "model_construct")(**kwargs)
