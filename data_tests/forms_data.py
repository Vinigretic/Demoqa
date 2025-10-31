from dataclasses import dataclass

from generator.upload_download_generator import FileFactory


@dataclass
class StudentFormFactory(FileFactory):
    first_name: str = None
    last_name: str = None
    email: str = None
    phone_number: str = None
    data_birthday: str = None
    subjects: str = None
    current_address: str = None
    state: str = None
    city: str = None
    gender: str = None
    hobbies: str = None
    picture: str = None
