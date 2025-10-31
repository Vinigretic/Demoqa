import random

from faker import Faker

from data_tests.forms_data import StudentFormFactory

fake = Faker('en_US')
Faker.seed()


def full_student_form_fields():
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
    states_cities = {
        "NCR": ["Delhi", "Gurgaon", "Noida"],
        "Uttar Pradesh": ["Agra", "Lucknow", "Merrut"],
        "Haryana": ["Karnal", "Panipat"],
        "Rajasthan": ["Jaipur", "Jaiselmer"]
    }
    state = random.choice(list(states_cities.keys()))
    city = random.choice(states_cities[state])
    picture = StudentFormFactory.create_temp_txt()

    return StudentFormFactory(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        data_birthday=birth_date.strftime("%d %b %Y"),
        phone_number=fake.msisdn()[:10],
        current_address=fake.address(),
        gender=random.choice(["male", "female", "other"]),
        subjects=random.choice(
            ["Maths", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Hindi", "Commerce",
             "Accounting", "Economics"]),
        hobbies=random.choice(["sport", "reading", "music"]),
        state=state,
        city=city,
        picture=picture,
    )
