from datetime import date
from typing import List

from fastapi import HTTPException
from sqlalchemy import or_, and_
from starlette import status

from src.db.pairs import pairs
from src.controllers.base import BaseController

from src.person_tests.numbers_types import NumbersTypes
from src.person_tests.personalities16_types import PersonalitiesTypes
from src.person_tests.socionic_types import SocionicTypes
from src.person_tests.zodiac_signs import ZodiacSigns
from src.schemas.pairs import PairUpdate, PairCreate, Pair


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

    @classmethod
    async def like_user(cls, user_id: int, curr_user: dict, liked: bool):
        pair_exist = await cls.get_pairs(first_user=user_id, second_user=curr_user['id'])
        if not pair_exist:
            return await cls.create_pair(
                PairCreate(
                    first_user=user_id, second_user=curr_user['id'],
                    like=False if liked is False else None
                )
            )
        new_like = None
        pair_exist = Pair(**dict(pair_exist[0].items()))
        if pair_exist.like is True:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="Already liked!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif pair_exist.like is None:
            # TODO отправить сообщения о взаимной симпатии
            print(f'User {curr_user["id"]} liked user {user_id}')
            new_like = liked
        elif pair_exist.like is False:
            # TODO доабвлять записи в таблицу фильтров
            print(f'User {curr_user["id"]} disliked user {user_id}')
            new_like = False
        return await cls.update_pair(
            pair_exist.id, PairUpdate(like=new_like, determined_date=date.today())
        )

    @classmethod
    async def get_pairs(
            cls, pair_id: int = None,
            first_user: int = None,
            second_user: int = None
    ) -> List[Pair]:
        query = pairs.select()
        if pair_id:
            query = pairs.select().where(pairs.c.id == pair_id)
        elif first_user and second_user:
            query = pairs.select().where(or_(
                and_(pairs.c.first_user == first_user, pairs.c.second_user == second_user),
                and_(pairs.c.first_user == second_user, pairs.c.second_user == first_user)
            ))
        elif first_user or second_user:
            query = pairs.select().where(or_(
                pairs.c.first_user == (first_user or second_user),
                pairs.c.second_user == (first_user or second_user)
            ))
        return await cls.db.fetch_all(query)

    @classmethod
    async def create_pair(cls, pair: PairCreate):
        if pair.like is not None:
            pair.determined_date = date.today()
        query = pairs.insert().values(
            first_user=pair.first_user,
            second_user=pair.second_user,
            like=pair.like,
            determined_date=pair.determined_date
        )
        return await cls.db.execute(query)

    @classmethod
    async def update_pair(cls, pair_id, pair: PairUpdate):
        if pair.like:
            pair.determined_date = date.today()
        query = pairs.update().where(
            pairs.c.id == pair_id
        ).values(
            like=pair.like,
            determined_date=pair.determined_date
        )
        return await cls.db.execute(query)
