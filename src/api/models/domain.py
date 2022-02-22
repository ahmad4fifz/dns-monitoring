from typing import Optional

from pydantic import BaseModel, Field


class DomainSchema(BaseModel):
    fuzzer: str = Field(...)
    domain: str = Field(...)
    dns_a: str = Field(...)
    dns_aaaa: str = Field(...)
    dns_mx: str = Field(...)
    dns_ns: str = Field(...)
    geoip: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fuzzer": "*original",
                "domain": "example.com",
                "dns_a": "93.184.216.34",
                "dns_aaaa": "2606:2800:220:1:248:1893:25c8:1946",
                "dns_mx": "mx.zoho.in",
                "dns_ns": "a.iana-servers.net",
                "geoip": "United States",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
