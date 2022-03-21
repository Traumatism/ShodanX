import pydantic

from rich.console import RenderableType
from rich.table import Table


class BaseModel(pydantic.BaseModel):
    """ Base model for all API models """

    def __rich__(self) -> RenderableType:
        table = Table(show_header=False)

        for _, field in self.__fields__.items():

            if field.name == "__raw__":
                continue

            value = getattr(self, field.name)

            if value is None:
                continue

            table.add_row(field.name.replace("_", " ").capitalize(), str(value))

        return table
