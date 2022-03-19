from .._model import BaseModel
from .._properties import GeneralProperties

from typing import List

from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.console import RenderableType


class HostInfo(BaseModel):
    """ Host info response model """

    ip: int
    ip_str: str
    ports: List[int]
    data: List[GeneralProperties]

    @property
    def sorted_ports(self) -> List[int]:
        """ Get the ports sorted """
        return sorted(self.ports)

    def __rich__(self) -> RenderableType:
        """ Override the rich repr """
        table = Table(show_header=False)
        table.add_row("IP", self.ip_str)
        table.add_row("Ports", ", ".join(map(str, self.sorted_ports)))
        table.add_row("Organization", self.data[0].org)

        table_b = Table(show_header=False, show_lines=True)

        for data in self.data:
            table_b.add_row(str(data.port), data.product)

        return Panel(Columns((table, table_b)))
