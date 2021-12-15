from enum import Enum


# TODO: доделать для всех знаков
class ZodiacSigns(Enum):
    aries = 0
    taurus = 1
    gemini = 2
    cancer = 3
    leo = 4
    virgo = 5
    libra = 6
    scorpio = 7
    sagittarius = 8
    capricorn = 9
    aquarius = 10
    pisces = 11

    relations_by_id = [
        [.9, .05, 1, .15, 1, .9, .6, .75, 1, .15, .8, .15],
        [.05, 1, .5, 1, .5, 1, .5, 1, .05, 1, .05, .9],
        [1, .5, .6, .15, 1, .2, 1, .15, .75, .1, 1, .1],
        [.15, 1, .15, 1, .5, 1, .05, 1, .15, .8, .05, 1],
        [1, .5, 1, .2, 1, .5, 1, .7, 1, .8, .7, .2],
        [.9, 1, .2, 1, .5, .6, .4, 1, .5, 1, .5, .7],
        [.6, .5, 1, .05, 1, .4, .9, .4, 1, .7, 1, .5],
        [.75, 1, .15, 1, .7, 1, .4, .9, .15, 1, .4, 1],
        [1, .05, .75, .15, 1, .5, 1, .15, .7, .05, 1, .15],
        [.15, 1, .1, .8, .8, 1, .7, 1, .05, 1, .15, 1],
        [.8, .05, 1, .05, .7, .5, 1, .4, 1, .15, .8, .1],
        [.15, .9, .1, 1, .2, .7, .5, 1, .15, 1, .1, .75]
    ]

    _signs_ruen = {
        'овен': 'aries',
        'телец': 'taurus',
        'близнецы': 'gemini',
        'рак': 'cancer',
        'лев': 'leo',
        'дева': 'virgo',
        'весы': 'libra',
        'скорпион': 'scorpio',
        'стрелец': 'sagittarius',
        'козерог': 'capricorn',
        'водолей': 'aquarius',
        'рыбы': 'pisces'
    }
    signs_enru = {
        'aries': 'овен',
        'taurus': 'телец',
        'gemini': 'близнецы',
        'cancer': 'рак',
        'leo': 'лев',
        'virgo': 'дева',
        'libra': 'весы',
        'scorpio': 'скорпион',
        'sagittarius': 'стрелец',
        'capricorn': 'козерог',
        'aquarius': 'водолей',
        'pisces': 'рыбы'
    }

    def ru(self):
        return ZodiacSigns.signs_enru.value[self.name]

    @classmethod
    def translate_to_eng(cls, sign: str):
        try:
            return cls._signs_ruen.value[sign.lower()]
        except KeyError:
            return None

    @classmethod
    def determine_sign(cls, day, month):
        if (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return cls.capricorn.value
        elif (month == 1 and day >= 20) or (month == 2 and day <= 17):
            return cls.aquarius.value
        elif (month == 2 and day >= 18) or (month == 3 and day <= 19):
            return cls.pisces.value
        elif (month == 3 and day >= 20) or (month == 4 and day <= 19):
            return cls.aries.value
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return cls.taurus.value
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return cls.gemini.value
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return cls.cancer.value
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return cls.leo.value
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return cls.virgo.value
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return cls.libra.value
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return cls.scorpio.value
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return cls.sagittarius.value


# print(ZodiacSigns.aries.name)  # Вернет - 'aries'
# print(ZodiacSigns['aries'].name)  # Вернет - 'aries'

# print(ZodiacSigns.aries.value)  # Вернет - 0
# print(ZodiacSigns['aries'].value)  # Вернет - 0

# # Получить русское значение по английскому
# print(ZodiacSigns.aries.ru())  # Вернет - 'овен'
# print(ZodiacSigns['aries'].ru())  # Вернет - 'овен'

# # Получить английское значение по русскому
# print(ZodiacSigns.translate_to_eng('овен'))  # Вернет - 'aries' или Null, если нет такого

# # Получить английское значение по id
# print(ZodiacSigns(0).name)  # Вернет - 'aries'