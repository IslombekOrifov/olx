from enum import Enum


class Licences(Enum):
    a = 'A'
    b = 'B'
    c = 'C'
    d = 'D'
    b_e = 'B+E'
    c_e = 'C+E'
    d_e = 'D+E'
    yoq = 'YOQ'


    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)


class Levels(Enum):
    il = 'B2'
    bo = 'Beginner'
    er = 'Native'
    oa = 'B1'

    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)
      

class Languages(Enum):
    ar = 'Arabic'
    en = 'English'
    ru = 'Russian'
    uz = 'Uzbek'
    

    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)