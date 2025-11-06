import random

from faker import Faker

from data_tests.date_picker import DatePickerFactory

fake = Faker('en_US')
Faker.seed()


def generated_date_time():
    return DatePickerFactory(
        month=fake.month_name(),
        year=str(random.randint(2020, 2030)),
        day=fake.day_of_month(),
        time=generate_time_15min_step()
    )


def generate_time_15min_step():
    # There are 96 15-minute intervals per day (24 * 4)
    intervals = random.randint(0, 95)
    hours = intervals // 4
    minutes = (intervals % 4) * 15
    return f"{hours:02d}:{minutes:02d}"
