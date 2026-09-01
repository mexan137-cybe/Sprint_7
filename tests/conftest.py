import pytest
import requests
from data.config import Urls

@pytest.fixture
def delete_courier():
    couriers = []
    yield couriers
    for x in couriers:
        response = requests.post(Urls.BASE_URL + Urls.COURIER_LOGIN_URL, json = x)
        if response.status_code == 200:
            id = response.json().get("id")
            requests.delete(f"{Urls.BASE_URL}{Urls.COURIER_URL}/{id}")