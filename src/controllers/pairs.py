from src.db.users import users
from src.controllers.base import BaseController

from src.person_tests.numbers_types import NumbersTypes
from src.person_tests.personalities16_types import PersonalitiesTypes
from src.person_tests.socionic_types import SocionicTypes
from src.person_tests.zodiac_signs import ZodiacSigns

class PairController(BaseController):
    """Класс для создания списка для свайпера
    """
    @classmethod
    async def get_list_for_swipe(cls, user_id):

        def to_converter(person):
            names = ["id", "name", "age", "city", "number", "zodiac_sign", "socionic_type", "sixteen_pers_type"]
            couple = [pair for pair in zip(names, range(len(names)))]
            return {k: person.get(key=i) for k, i in couple}

        def relation(person1, person2, cl):
            return int(cl.relations_by_id.value[person1][person2] * 100)

        def total_percentage(*args):
            return round((sum(args)/len(args)))

        query = '''SELECT id, name, age, city, number, zodiac_sign, socionic_type, sixteen_pers_type  
        FROM users
        WHERE id = :user_id
        '''
        person = await cls.db.fetch_all(query=query, values={"user_id": user_id})
        # people = [{id, name, age, city, number, zodiac_sign, socionic_type, sixteen_pers_type}]
        people = []
        people.append(to_converter(person[0]))
        query = '''SELECT id, name, age, city, number, zodiac_sign, socionic_type, sixteen_pers_type  
                FROM users
                WHERE id <> :user_id AND age BETWEEN :main_age - 5 AND :main_age +5 
                    AND city = :main_city
                '''
        applicants = await cls.db.fetch_all(query=query, values={"user_id": user_id, "main_age": people[0]["age"],
                                                                 "main_city": people[0]["city"]})
        for i in range(len(applicants)):
            people.append(to_converter(applicants[i]))

        for i in range(1, len(people)):
            people[i]['socio'] = relation(people[0]['socionic_type'], people[i]['socionic_type'],
                                                SocionicTypes)
            people[i]['pers'] = relation(people[0]['sixteen_pers_type'], people[i]['sixteen_pers_type'],
                                          PersonalitiesTypes)
            people[i]['nr'] = relation(people[0]['number'], people[i]['number'],
                                         NumbersTypes)
            people[i]['zs'] = relation(people[0]['zodiac_sign'], people[i]['zodiac_sign'],
                                         ZodiacSigns)
            people[i]['percent'] = total_percentage(people[i]['socio'], people[i]['pers'],
                                                    people[i]['nr'], people[i]['zs'])
            people[i]["socionic_type"] = SocionicTypes(people[i]["socionic_type"]).ru_name()
            people[i]["sixteen_pers_type"] = PersonalitiesTypes(people[i]["sixteen_pers_type"]).ru_name()

        print(type(people[1]["number"]))
        return people[1:]


