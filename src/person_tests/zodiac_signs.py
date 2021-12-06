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
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # отношения овна
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # отношения тельца
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # и тд
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
        except(KeyError):
            return None


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