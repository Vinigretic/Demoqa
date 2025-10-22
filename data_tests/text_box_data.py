from dataclasses import dataclass


@dataclass  # add methods to the class - __init__, __repr__, __eq__, __asdict__
class PersonFactory:
    full_name: str = None
    email: str = None
    current_address: str = None
    permanent_address: str = None


# Data for the email field
email_categories = {
    "valid": [
        "user@gmail.com",
        "first.last@gmail.com",
        "user123@gmail.com",
        "user@gmail.co.uk",
        "a@b.co",
        # "a" * 64 + "@" + ".".join(["b" * 63, "c" * 63, "d" * 61]),  # 254 symbols put down the page
    ],
    "invalid_cases": {
        "invalid": [
            "userexample.com",
            "user@",
            "user @gmail.com",
            "юзер@почта.укр",
            "user@gmail.com' OR '1'='1",
            ".user@gmail.com",
            "user.@gmail.com",
            "user+test@gmail.com",
            # "a" * 64 + "@" + ".".join(["b" * 63, "c" * 63, "d" * 62]),  # 255 symbols put down the page
        ],
        "edge": [
            "user@[192.168.1.1]",
            r"user\n@gmail.com",
            "user\\n@gmail.com",
            "user@gmaіl.com",  # # The Latin i was replaced by the Cyrillic і
            "John\u200B@gmaіl.com",  # zero-width space
            "user\u2007@gmail.com",  # figure space
        ],
        "security": [
            "'; DROP TABLE users;--@gmail.com",
            "admin' --@gmail.com",
            "admin' OR 1=1;--@gmail.com",
            "<script>alert('XSS')</script>@gmail.com",
            "<img src=x onerror=alert(1)>@gmail.com",
            "<a href='javascript:alert('XSS')'>Click me</a>@gmail.com",
            "<svg onload=alert(1)>@gmail.com",
            "<div style='width:expression(alert('XSS'));'@gmail.com>",
        ]
    }
}

full_name_categories = {
    "valid": [
        "John Doe",
        "Anna Maria",
        "Jean-Luc",
        "O'Connor",
        "Іван Петренко",  # cyrillic
        "User123",
        "A",  # minimum length
        "A" * 255,  # maximum length
        " John ",  # spaces at the edges
        # "𝓙𝓸𝓱𝓷",  # decorative Unicode
        "John\u200B",  # zero-width space
        "Іvan Petrenko"  # spoofing: cyrillic І instead of latin
    ],
    "invalid": [
        # "", # empty line
        " ",  # space
        "123456",  # only numbers
        "@#$%",  # special characters
    ],
    "security": [
        "<script>",  # HTML-tag
        "<script>alert('XSS')</script>",  # XSS-injection
        "'; DROP TABLE users;--",  # SQL-injection
    ]

}
address_cases = {
    "valid": [
        "123 Main St",  # english address
        "вул. Сумська, 10",  # ukrainian address
        "Line1\\nLine2",  # multi-line address
        "A",
        "A" * 1000,
        "123\\tMain",
        " 123 Main St ",
        "123\u200BMain",
    ],
    "invalid": [
        # "",
        " ",
        "@#$%",
    ],
    "security": [
        "'; DROP TABLE users;--",
        "<script>alert('XSS')</script>",
        "<div>123</div>",
        "<b>Bold Address</b>",
    ]
}
