from faker import Faker
import requests
import string
import random
from data.config import Urls

fake = Faker('ru_RU')

def generate_courier_registration_data():
    data = {'login': fake.user_name(), 'password': fake.password(), 'firstName': fake.first_name()}
    return data

def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(Urls.BASE_URL + Urls.COURIER_URL, data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass 

def generate_order_data(color = None):
    order = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": f"{fake.city()}, {fake.street_address()}, д. {fake.building_number()}",
        "metroStation": fake.random_int(min=1, max=25),
        "phone": fake.phone_number(),
        "rentTime": fake.random_int(min=1, max=7),
        "deliveryDate": str(fake.date_this_year()),
        "comment": fake.sentence(),
    }
    if color is not None:
        order["color"] = color
    return order