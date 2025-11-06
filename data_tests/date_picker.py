from dataclasses import dataclass


@dataclass
class DatePickerFactory:
    month: str = None
    year: str = None
    day: str = None
    time: str = None
