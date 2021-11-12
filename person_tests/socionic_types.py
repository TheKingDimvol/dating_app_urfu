from enum import Enum

class SocionicTypes(Enum):
    ENTP = 0
    ISFP = 1
    ESFJ = 2
    INTJ = 3
    ENFJ = 4
    ISTJ = 5
    ESTP = 6
    INFP = 7
    ESFP = 8
    INTP = 9
    ENTJ = 10
    ISFJ = 11
    ESTJ = 12
    INFJ = 13
    ENFP = 14
    ISTP = 15

    relations_by_id = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # отношения дон
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # отношения дюма
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # и тд
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    type_name = {
        'ENTP': 'Дон Кихот',
        'ISFP': 'Дюма',
        'ESFJ': 'Гюго',
        'INTJ': 'Робеспьер',
        'ENFJ': 'Гамлет',
        'ISTJ': 'Максим Горький',
        'ESTP': 'Жуков',
        'INFP': 'Есенин',
        'ESFP': 'Наполеон',
        'INTP': 'Бальзак',
        'ENTJ': 'Джек Лондон',
        'ISFJ': 'Драйзер',
        'ESTJ': 'Штирлиц',
        'INFJ': 'Достоевский',
        'ENFP': 'Гексли',
        'ISTP': 'Габен'
    }

    type_get_abbreviation = {
        'дон кихот': 'ENTP',
        'дюма': 'ISFP',
        'гюго': 'ESFJ',
        'робеспьер': 'INTJ',
        'гамлет': 'ENFJ',
        'максим горький': 'ISTJ',
        'жуков': 'ESTP',
        'eсенин': 'INFP',
        'наполеон': 'ESFP',
        'бальзак': 'INTP',
        'джек лондон': 'ENTJ',
        'драйзер': 'ISFJ',
        'штирлиц': 'ESTJ',
        'достоевский': 'INFJ',
        'гексли': 'ENFP',
        'габен': 'ISTP'
    }

    def ru_name(self):
        return SocionicTypes.type_name.value[self.name]

    @classmethod
    def to_abbreviation(cls, type: str):
        try:
            return cls.type_get_abbreviation.value[type.lower()]
        except(KeyError):
            return None


#print(SocionicTypes.ENFP.name)  #ENFP
#print(SocionicTypes(14).name)  #ENFP
#print(SocionicTypes.ENFP.ru_name())  #Гексли
#print(SocionicTypes(14).ru_name())  #Гексли
#print(SocionicTypes.to_abbreviation('Гексли')) #ENFP



