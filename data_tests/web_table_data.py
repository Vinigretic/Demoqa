from dataclasses import dataclass


@dataclass
class PersonTableFactory:
    first_name: str = None
    last_name: str = None
    email: str = None
    age: int = None
    salary: int = None
    department: str = None
