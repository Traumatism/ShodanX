import pydantic

from rich.console import RenderableType


class BaseModel(pydantic.BaseModel):
    """ Base model for all API models """

    def __rich__(self) -> RenderableType: ...

    def __repr__(self) -> str:
        """ Override the repr """
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str:
        return repr(self)
