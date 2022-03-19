import pydantic

from rich.table import Table


class BaseModel(pydantic.BaseModel):
    """ Base model for all API models """

    def __rich__(self) -> Table:
        """ Override the rich repr """
        ...

    def __repr__(self) -> str:
        """ Override the repr """
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str:
        return repr(self)
