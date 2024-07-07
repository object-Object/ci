from enum import Enum
from typing import Literal

RecordType = Literal[
    "A",
    "AAAA",
    "CAA",
    "CNAME",
    "TXT",
    "SRV",
    "LOC",
    "MX",
    "NS",
    "SPF",
    "CERT",
    "DNSKEY",
    "DS",
    "NAPTR",
    "SMIMEA",
    "SSHFP",
    "TLSA",
    "URI",
    "PTR",
    "HTTPS",
    "SVCB",
]


class RecordName(Enum):
    """Special Cloudflare record names (subdomains).

    The enum value corresponds to `Record.name`.
    """

    ROOT = "@"
    WILDCARD = "*"

    @classmethod
    def from_record_name(cls, name: str):
        try:
            return cls(name)
        except ValueError:
            return None

    @property
    def display_name(self):
        return self.name

    @property
    def record_name(self):
        return self.value
