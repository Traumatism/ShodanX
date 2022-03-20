import pydantic
import abc

from rich.console import RenderableType


class BaseModel(pydantic.BaseModel):
    """ Base model for all API models """

    @abc.abstractmethod
    def __rich__(self) -> RenderableType:
        raise NotImplementedError("__rich__() must be implemented")
