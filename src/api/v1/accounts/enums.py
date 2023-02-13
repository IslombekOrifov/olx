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
    il = 'Ilg\'or'
    bo = 'Boshlang\'ich'
    er = 'Erkin'
    oa = 'O\'rta'

    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)
      

class Languages(Enum):
    ar = 'Arab tili'
    en = 'Ingliz tili'
    ru = 'Rus tili'
    uz = 'O\'zbek tili'
    

    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)