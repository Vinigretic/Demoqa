from faker import Faker

from data_tests.text_box_data import PersonFactory

fake = Faker('en_US')
Faker.seed()  # Faker.seed(42), 42 - starting point for the random number generator


def _generate_person(overrides=None):
    generated = {
        "full_name": f"{fake.first_name()} {fake.last_name()}",
        "email": fake.email(),
        "current_address": fake.address(),
        "permanent_address": fake.address()
    }
    if overrides:
        generated.update(overrides)
    return PersonFactory(**generated)


def person_all_fields():
    return _generate_person()


def person_partial(field: str) -> PersonFactory:
    person_data = {key: None for key in ("full_name", "email", "current_address", "permanent_address")}
    person_data[field] = _generate_person().__dict__[field]
    return PersonFactory(**person_data)


def person_missing(field: str):
    return _generate_person({field: None})


def person_email_validation(field: str):
    return _generate_person({"email": field})


def person_empty():
    return PersonFactory()


def person_full_name_validation(field: str):
    return _generate_person({"full_name": field})


def person_current_address_validation(field: str):
    return _generate_person({"current_address": field})


def person_permanent_address_validation(field: str):
    return _generate_person({"permanent_address": field})
