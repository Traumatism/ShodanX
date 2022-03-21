from typing import List, Optional, Union

from .abc import BaseModel


class Location(BaseModel):
    city: Optional[str]
    country_code: Optional[str]
    country_name: Optional[str]
    dma_code: Optional[str]
    latitude: Optional[Union[int, float]]
    longitude: Optional[Union[int, float]]
    region_code: Optional[str]


class Row(BaseModel):
    ip: int
    ip_str: str
    port: int
    hash: int
    timestamp: str
    product: Optional[str]
    data: str
    domains: List[str]
    location: Location
    hostnames: List[str]
    org: str
    isp: str
    asn: str


class Host(BaseModel):
    ip: int
    ip_str: str
    ports: List[int]
    hostnames: List[str]
    domains: List[str]
    tags: List[str]
    isp: str
    asn: str
    data: List[Row]


class InternetDB(BaseModel):
    ip: Optional[str]
    cpes: Optional[List[str]]
    hostnames: Optional[List[str]]
    ports: Optional[List[int]]
    tags: Optional[List[str]]
    vulns: Optional[List[str]]


class SearchResults(BaseModel):
    total: int
    matches: List[Row]
