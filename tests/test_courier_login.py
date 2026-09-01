import allure
import pytest
import requests
from data.config import BASE_URL, COURIER_LOGIN_URL, COURIER_LOGIN_NOT_FOUND_MESSAGE, COURIER_LOGIN_MISSING_FIELDS_MESSAGE
from utils.generators import generate_courier_registration_data as gc
from utils.generators import register_new_courier_and_return_login_password as rc


class TestCourierLogin:
    @allure.title("Курьера может авторизоваться")
    def test_courier_login(self):
        login, password, first_name = rc()
        payload = {'login': login, 'password': password}
        response = requests.post(BASE_URL + COURIER_LOGIN_URL, data = payload)
        assert response.status_code == 200

    @allure.title("При авторизации курьера возвращается id")
    def test_courier_login_message(self):
        login, password, first_name = rc()
        payload = {'login': login, 'password': password}
        response = requests.post(BASE_URL + COURIER_LOGIN_URL, data = payload)
        assert "id" in response.json()
        
    @allure.title("Нельзя авторизоваться курьером без обязательного поля {missing_field}")
    @pytest.mark.parametrize("missing_field",["login","password"])
    def test_login_courier_without_required_fields_returns_error(self, missing_field):
        payload = gc()
        payload.pop('firstName', None)
        payload.pop(missing_field)
        response = requests.post(BASE_URL + COURIER_LOGIN_URL, json = payload, timeout = 2)
        assert response.status_code == 400

    @allure.title("Возвращается ошибка при авторизоации курьером без обязательного поля {missing_field}")
    @pytest.mark.parametrize("missing_field",["login","password"])
    def test_login_courier_without_required_fields_returns_message(self, missing_field):
        payload = gc()
        payload.pop('firstName', None)
        payload.pop(missing_field)
        response = requests.post(BASE_URL + COURIER_LOGIN_URL, json = payload, timeout = 2)
        assert response.json()['message'] == COURIER_LOGIN_MISSING_FIELDS_MESSAGE

    @allure.title("Несуществующая пара логин-пароль возвращает ошибку")
    def test_courier_login_invalid_credentinal_message(self):
        payload = gc()
        payload.pop('firstName', None)
        response = requests.post(BASE_URL + COURIER_LOGIN_URL, json = payload, timeout = 2)
        assert response.json()['message'] == COURIER_LOGIN_NOT_FOUND_MESSAGE

    @allure.title("Несуществующая пара логин-пароль возвращает код 404")
    def test_courier_login_invalid_credentinal_code(self):
        payload = gc()
        payload.pop('firstName', None)
        response = requests.post(BASE_URL + COURIER_LOGIN_URL, json = payload, timeout = 2)
        assert response.status_code == 404, f"Сервер вернул {response.status_code} вместо 404"
        