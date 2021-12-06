import datetime
from enum import Enum

class NumbersTypes(Enum):
    n1 = 0
    n2 = 1
    n3 = 2
    n4 = 3
    n5 = 4
    n6 = 5
    n7 = 6
    n8 = 7
    n9 = 8


    relations_by_id = [
        [.05, .8, .9, .9, 1, .8, .6, .05, .5], # отношения 1
        [.8, .9, .8, .5, .9, .9, .05, 1, 1],   # отношения 2
        [.9, .8, .05, .1, 1, .1, 1, .6, .8],   # и тд
        [.9, .5, .1, .5, .05, .5, .85, .9, .5],
        [1, .9, 1, .05, 1, .6, .9, .1, .9],
        [.8, .9, .1, .5, .6, .5, .5, .1, .5],
        [.6, .05, 1, .85, .9, .5, .5, .1, .5],
        [.05, 1, .6, .9, .1, .5, .1, .5, .1],
        [.5, 1, .8, .5, .9, 1, .5, .1, .5]
    ]

    @classmethod
    def get_relationship(cls, p1):
        return cls.relations_by_id[p1]


    @classmethod
    def get_number_id(cls, d: datetime.date):
        number = (int(d.day) // 10 + int(d.day) % 10
            + int(d.month) // 10 + int(d.month) % 10
            + int(d.year) // 1000 + int(d.year) // 100 % 10
            + int(d.year) % 100 // 10 + int(d.year) % 10)
        while number > 9:
            number = number // 10 + number % 10
        return cls(number - 1).name


#print(NumbersTypes.n1.value)  #0
#print(NumbersTypes(0).name)  #n1

#birthday = datetime.date(year=2000, month=1, day=4)
#print(NumbersTypes.get_number_id(birthday))  #n7

#print(NumbersTypes.relations_by_id.value[0][0])  #0.05

#print(PersonalitiesTypes(14).ru_name())  #Активист
#print(PersonalitiesTypes.to_abbreviation('Гексли')) #ENFP



