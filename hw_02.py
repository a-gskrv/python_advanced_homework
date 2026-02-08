'''
Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных,
обработки вложенных структур и сериализации. Система должна обрабатывать данные в формате JSON.

Задачи:
Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.

Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic,
валидирует данные, и в случае успеха
сериализует объект обратно в JSON и возвращает его.

Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.

Написать несколько примеров JSON строк для проверки различных сценариев валидации:
успешные регистрации и случаи, когда валидация не проходит (например возраст не соответствует статусу занятости).

Валидация:
Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.

'''

from pydantic import (
    Field,
    field_validator,
    model_validator,
    BaseModel,
    EmailStr)


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("name")
    @classmethod
    def check_name(cls, value: str) -> str:
        text_without_space = value.replace(" ", "")
        if not text_without_space.isalpha():
            raise ValueError("Name must contain only letters")
        return value

    @model_validator(mode="after")
    def check_age_and_employed(self):
        if self.is_employed:
            if not (18 < self.age < 65):
                raise ValueError(
                    "If user is employed, age must be between 18 and 65"
                )
        return self


def json_to_obj(json_str):
    try:
        user = User.model_validate_json(json_str)
        # print(user)
        return user.model_dump_json()
    except Exception as e:
        return e


list_json = []

json_input_01 = """{
    "name": "John Doe",
    "age": 50,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_input_02 = """{
    "name": "Anna Doe",
    "age": 10,
    "email": "anna.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_input_03 = """{
    "name": "John 000 Doe",
    "age": 10,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_input_04 = """{
    "name": "Ann2a Doe",
    "age": 10,
    "email": "anna.doe(a)example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_input_05 = """{
    "name": "John Doe",
    "age": 10,
    "email": "john.doe@example.com",
    "is_employed": false,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

list_json.append(json_input_01)
list_json.append(json_input_02)
list_json.append(json_input_03)
list_json.append(json_input_04)
list_json.append(json_input_05)

if __name__ == "__main__":
    for i, json_str in enumerate(list_json, start=1):
        print(f"\n{i}: {"*" * 50}")
        result = json_to_obj(json_str)
        print(result)
