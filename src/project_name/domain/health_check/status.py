from dataclasses import dataclass
from typing import Dict


@dataclass()
class HealthCheckStatus:
    api_health: bool
    db_health: bool

    def to_dict(self) -> Dict:
        return self.__dict__
