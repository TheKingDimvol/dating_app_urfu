from enum import Enum

class City(Enum):
    Moscow = 0
    Yekaterinburg = 1

    city_name = {
        'Moscow': 'Москва',
        'Yekaterinburg': 'Екатеринбург'
    }

    def ru_name(self):
        return City.city_name.value[self.name]


#print(City.Moscow.name)  #Moscow
#print(City(1).name)  #Yekaterinburg
#print(City.Moscow.ru_name())  #Москва