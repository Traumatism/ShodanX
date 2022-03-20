from ..abc import BaseModel
from ..properties import GeneralProperties

from typing import List, Optional

from rich.table import Table
from rich.console import RenderableType


class HostInfo(BaseModel):
    """ Host info response model """

    ip: int
    ip_str: str
    ports: List[int]
    data: List[GeneralProperties]
    asn: Optional[str]
    org: Optional[str]

    @property
    def sorted_ports(self) -> List[int]:
        """ Get the ports sorted """
        return sorted(self.ports)

    def __rich__(self) -> RenderableType:
        """ Override the rich repr """
        table = Table(show_header=False)

        table.add_row("IP", self.ip_str)
        table.add_row("Ports", ", ".join(map(str, self.sorted_ports)))
        table.add_row("ASN", self.asn)
        table.add_row("Organization", self.org)

        table_b = Table(show_header=False, show_lines=True)

        for _data in self.data:
            port = str(_data.port)
            data = ""

            if _data.product:
                data += f"{_data.product}"

            table_b.add_row(port, data or "[red]-[/red]")

        table.add_row("Data", table_b)

        if self.data[0].hostnames:
            table.add_row("Hostnames", ", ".join(self.data[0].hostnames))

        if self.data[0].domains:
            table.add_row("Domains", ", ".join(self.data[0].domains))

        if self.data[0].tags:
            table.add_row("Tags", ", ".join(self.data[0].tags))

        return table