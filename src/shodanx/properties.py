from .abc import BaseModel

from typing import Any, List, Optional, Union, Literal


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
