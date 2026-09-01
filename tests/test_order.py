import allure
import requests
import pytest
from utils.generators import generate_order_data as go
from data.config import Urls, Message

class TestOrderCreate:
    @allure.title("Создание заказа с различными цветами")
    @pytest.mark.parametrize("color",[["BLACK"],["GREY"],["BLACK", "GREY"],None])
    def test_order_created_with_color(self, color):
        payload = go(color)
        with allure.step("Отправка запроса на получение заказов из системы"):
            response = requests.post(Urls.BASE_URL + Urls.ORDERS_URL, json= payload, timeout= 2)
        assert response.status_code == 201

    @allure.title("При успешном создании заказа возвращается track")
    def test_order_created_response(self):
        with allure.step("Отправка запроса на получение заказов из системы"):
            response = requests.post(Urls.BASE_URL + Urls.ORDERS_URL, json= go(), timeout= 2)
        assert "track" in response.json()

    @allure.title("Получение списка заказов")
    def test_order_list_return(self):
        with allure.step("Отправка запроса на получение заказов из системы"):
            response = requests.get(Urls.BASE_URL + Urls.ORDERS_URL, timeout= 2)
        r = response.json()
        assert len(r['orders']) > 0
