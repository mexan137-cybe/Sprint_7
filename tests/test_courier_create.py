import allure
import pytest
import requests
from data.config import BASE_URL, COURIER_URL, COURIER_CREATED_WITHOUT_REQUIRED_FIELDS_MESSAGE, COURIER_CREATED_ALREADY_EXIST_MESSAGE
from utils.generators import generate_courier_registration_data as gc
from utils.generators import register_new_courier_and_return_login_password as rc


class TestCourierCreate:
    @allure.title("Курьера можно создать")
    def test_courier_created(self):
        response = requests.post(BASE_URL + COURIER_URL, data = gc())
        assert response.status_code == 201

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_courier_repeat_created(self):
        login, password, first_name = rc()
        payload = {'login': login, 'password': password, 'firstName': first_name}
        response = requests.post(BASE_URL + COURIER_URL, data = payload)
        assert response.status_code == 409

    @allure.title("Нельзя создать курьера без обязательного поля {missing_field}")
    @pytest.mark.parametrize("missing_field",["login","password"])
    def test_create_courier_without_required_fields_returns_error(self, missing_field):
        payload = gc()
        payload.pop(missing_field)
        response = requests.post(BASE_URL + COURIER_URL, data = payload)
        assert response.status_code == 400

    @allure.title("Успешный запрос возвращает сообщение")
    def test_courier_created_return_success_message(self):
        response = requests.post(BASE_URL + COURIER_URL, data = gc())
        assert response.json() == {"ok": True}

    @allure.title("Если нет обязательного поля {missing_field} возвращает сообщение об ошибке")
    @pytest.mark.parametrize("missing_field",["login","password"])
    def test_create_courier_without_required_fields_returns_error_message(self, missing_field):
        payload = gc()
        payload.pop(missing_field)
        response = requests.post(BASE_URL + COURIER_URL, data = payload)
        assert response.json()['message'] == COURIER_CREATED_WITHOUT_REQUIRED_FIELDS_MESSAGE

    @allure.title("Если создать пользователя с логином, который уже есть, возвращается сообщзение об ошибке")
    def test_courier_repeat_created_message(self):
        login, password, first_name = rc()
        payload = {'login': login, 'password': password, 'firstName': first_name}
        response = requests.post(BASE_URL + COURIER_URL, data = payload)
        assert response.json()['message'] == COURIER_CREATED_ALREADY_EXIST_MESSAGE
