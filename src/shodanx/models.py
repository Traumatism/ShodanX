from rich.table import Table
from rich.console import RenderableType

from typing import Any, List, Optional, Union, Literal

from .abc import BaseModel


Tag = Literal[
    "c2", "cdn", "cloud", "compromised", "cryptocurrency", "database",
    "devops", "doublepulsar", "honeypot", "ics", "iot", "malware", "medical",
    "onion", "self-signed", "scanner", "starttls", "tor", "videogame", "vpn"
]


class MacAddressInfo(BaseModel):
    """ Mac address model """
    assignment: str
    org: str
    date: Optional[str]


class Vulnerability(BaseModel):
    """ Vulnerability model """
    cvss: int
    references: List[str]
    summary: str
    verified: bool


class GeneralProperties(BaseModel):
    """ General properties model """
    data: str
    domains: List[str]
    hash: int
    hostnames: List[str]
    port: int
    timestamp: str
    transport: str
    asn: Optional[str]
    cpe23: Optional[List[str]]
    device: Optional[str]
    devicetype: Optional[str]
    ip: Optional[int]
    ip_str: Optional[str]
    info: Optional[str]
    ipv6: Optional[str]
    isp: Optional[str]
    link: Optional[str]
    opts: Optional[Any]
    org: Optional[str]
    os: Optional[str]
    platform: Optional[str]
    product: Optional[str]
    tags: Optional[Tag]
    uptime: Optional[int]
    vendor: Optional[str]
    version: Optional[str]


class ShodanOptions(BaseModel):
    """ _ShodanOptions property model """
    hostname: Optional[str]
    referrer: Optional[str]
    scan: Optional[str]


class ShodanProperty(BaseModel):
    """ _Shodan property model """
    crawler: str
    id: str
    module: str
    options: ShodanOptions
    ptr: Optional[bool]


class Location(BaseModel):
    """ Location property """
    city: Optional[str]
    country_code: Optional[str]
    country_name: Optional[str]
    dma_code: Optional[str]
    latitude: Optional[Union[int, float]]
    longitude: Optional[Union[int, float]]
    region_code: Optional[str]


class InternetDB(BaseModel):
    """ InternetDB property """
    ip: Optional[str]
    cpes: Optional[List[str]]
    hostnames: Optional[List[str]]
    ports: Optional[List[int]]
    tags: Optional[List[str]]
    vulns: Optional[List[str]]

    def __rich__(self):

        _fields = {
            "IP": self.ip,
            "CPEs": self.cpes,
            "Hostnames": self.hostnames,
            "Ports": self.ports,
            "Tags": self.tags,
            "Vulnerabilities": self.vulns
        }

        fields = {key: value for key, value in _fields.items() if value}

        table = Table(show_header=False)

        for key, value in fields.items():

            if isinstance(value, list):
                table.add_row(key, ", ".join(map(str, value)))
                continue

            table.add_row(key, value)

        return table


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


class AccountInfo(BaseModel):
    """ Account info response model """
