import random 
from datetime import date, timedelta

SURNAMES = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов",
            "Михайлов", "Новиков", "Фёдоров", "Морозов", "Волков", "Алексеев", "Лебедев",
            "Семёнов", "Егоров", "Павлов", "Козлов", "Степанов", "Николаев"]

PATRONYMICS = [("Александрович", "Александровна"), ("Дмитриевич", "Дмитриевна"),
               ("Сергеевич", "Сергеевна"), ("Андреевич", "Андреевна"),
               ("Алексеевич", "Алексеевна"), ("Михайлович", "Михайловна"),
               ("Иванович", "Ивановна"), ("Николаевич", "Николаевна"),
               ("Владимирович", "Владимировна"), ("Павлович", "Павловна"),
               ("Олегович", "Олеговна"), ("Юрьевич", "Юрьевна")]

MALE_NAMES = ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Артём",
              "Илья", "Кирилл", "Михаил", "Никита", "Матвей", "Роман", "Егор", "Тихон"]
FEMALE_NAMES = ["Анастасия", "Мария", "Анна", "Виктория", "Екатерина", "Наталья", "Марина",
                "Полина", "Дарья", "Алиса", "Ксения", "Софья", "Елизавета", "Вера", "Ульяна"]

LETTERS = "АБВГДЕКМНОРСТУХ"

def random_person(rng: random.Random):
    male = rng.random() < 0.5
    surname = rng.choice(SURNAMES)
    patronymic = rng.choice(PATRONYMICS)
    first = date(1950, 1, 1)
    days = (date(2008, 12, 31) - first).days
    birth = first + timedelta(days=rng.randrange(days))
    return {
        "surname": surname if male else surname + "а",
        "name": rng.choice(MALE_NAMES if male else FEMALE_NAMES),
        "patronymic": patronymic[0] if male else patronymic[1],
        "birth_date": birth.strftime("%d.%m.%Y"),
        "number": "".join(rng.choices(LETTERS, k=2)) + " " +
        str(rng.randrange(10**6, 10**7))
    }