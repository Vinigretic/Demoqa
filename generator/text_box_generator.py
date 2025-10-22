from faker import Faker

from data_tests.text_box_data import PersonFactory

fake = Faker('en_US')
Faker.seed()  # Faker.seed(42), 42 - starting point for the random number generator


# def generated_person():
#     yield PersonFactory(
#         full_name= f"{fake.first_name()} {fake.last_name()}",
#         email= fake.email(),
#         current_address= fake.address(),
#         permanent_address= fake.address(),
#     )

def person_all_fields():
    return PersonFactory(
        full_name=f"{fake.first_name()} {fake.last_name()}",
        email=fake.email(),
        current_address=fake.address(),
        permanent_address=fake.address()
    )


def person_partial(field: str) -> PersonFactory:
    # generate fields
    generated = {
        "full_name": f"{fake.first_name()} {fake.last_name()}",
        "email": fake.email(),
        "current_address": fake.address(),
        "permanent_address": fake.address()
    }
    # Leave only specified field, rest - None
    person_data = {}
    for key in generated:
        if key == field:
            person_data[key] = generated[key]
        else:
            person_data[key] = None

    return PersonFactory(
        full_name=person_data["full_name"],
        email=person_data["email"],
        current_address=person_data["current_address"],
        permanent_address=person_data["permanent_address"]
    )


def person_missing(field: str):
    generated = {
        "full_name": f"{fake.first_name()} {fake.last_name()}",
        "email": fake.email(),
        "current_address": fake.address(),
        "permanent_address": fake.address()
    }
    # Remove specified filed, rest - valid
    person_data = {}
    for key in generated:
        if key == field:
            person_data[key] = None
        else:
            person_data[key] = generated[key]

    return PersonFactory(
        full_name=person_data["full_name"],
        email=person_data["email"],
        current_address=person_data["current_address"],
        permanent_address=person_data["permanent_address"]
    )


def person_email_validation(field: str):
    return PersonFactory(
        full_name=f"{fake.first_name()} {fake.last_name()}",
        email=field,
        current_address=fake.address(),
        permanent_address=fake.address()
    )


def person_empty():
    return PersonFactory()


def person_full_name_validation(field: str):
    return PersonFactory(
        full_name=field,
        email=fake.email(),
        current_address=fake.address(),
        permanent_address=fake.address()
    )


def person_current_address_validation(field: str):
    return PersonFactory(
        full_name=f"{fake.first_name()} {fake.last_name()}",
        email=fake.email(),
        current_address=field,
        permanent_address=fake.address()
    )


def person_permanent_address_validation(field: str):
    return PersonFactory(
        full_name=f"{fake.first_name()} {fake.last_name()}",
        email=fake.email(),
        current_address=fake.address(),
        permanent_address=field
    )
