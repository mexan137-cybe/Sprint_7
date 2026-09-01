import allure
import requests
import pytest
from utils.generators import generate_order_data as go
from data.config import BASE_URL, ORDERS_URL

class TestOrderCreate:
    @allure.title("Создание заказа с различными цветами")
    @pytest.mark.parametrize("color",[["BLACK"],["GREY"],["BLACK", "GREY"],None])
    def test_order_created_with_color(self, color):
        payload = go(color)
        response = requests.post(BASE_URL + ORDERS_URL, json= payload, timeout= 2)
        assert response.status_code == 201

    @allure.title("При успешном создании заказа возвращается track")
    def test_order_created_response(self):
        response = requests.post(BASE_URL + ORDERS_URL, json= go(), timeout= 2)
        assert "track" in response.json()

    @allure.title("Получение списка заказов")
    def test_order_list_return(self):
        response = requests.get(BASE_URL + ORDERS_URL, timeout= 2)
        r = response.json()
        assert len(r['orders']) > 0

