import pytest
import requests
import allure
from host import url_on_fe
from host import get_info_url
from utils import check_response_status_code
from utils import create_url_list


# Тут хотелось бы сделать фикстурой, но нам нужна параметризация, а вызывать фикстуру в @pytest.mark.parametrize нельзя
@allure.feature('api test')
@allure.story("Create Url list")
def url_list():
    urls_list = create_url_list()
    return urls_list


list_url = create_url_list()


@allure.feature('api test')
@allure.story("Check page opening")
@pytest.mark.parametrize('route', list_url)
def test_opening_pages(route):
    url = f'{get_info_url}/nodes/{route}'
    response = requests.get(url)
    check_response_status_code(response, expected_status_code=200, message=f"Ошибка при открытии: {url}")

    # Проверяем Summary на наличие текста
    response_data = response.json()
    summary = response_data['summary']
    assert isinstance(summary, str), f"Summary имеет отличный от строки тип данных. Summary: {summary}"
    assert len(summary) > 0, f'Отсутствует summary на странице {url_on_fe}{route}'
