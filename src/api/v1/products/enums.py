from enum import Enum


class ProductStatus(Enum):
    wt = 'Waiting'
    ac = 'Active'
    na = 'Not Active'
    rd = 'Rejected'
    ar = 'Archive'
    bn = 'Banned'

    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)