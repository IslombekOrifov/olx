from enum import Enum

class AdvantageType(Enum):
    t = "TOP"
    u = "UP"
    v = "VIP"

    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)