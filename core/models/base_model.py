from enum import Enum

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_default=True,
        validate_by_name=True,
        use_enum_values=True,
    )
