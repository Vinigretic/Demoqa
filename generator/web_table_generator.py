import random

from faker import Faker

from data_tests.web_table_data import PersonTableFactory

fake = Faker('en_US')
Faker.seed()


def generated_person_web_table():
    return PersonTableFactory(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        age=random.randint(18, 65),
        salary=random.randint(8000, 300000),
        department = fake.job()[:21],
    )

