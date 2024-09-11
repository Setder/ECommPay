import requests
import pytest
from host import get_info_url
from jsonpath_ng import parse


def check_response_status_code(response: requests.Response, expected_status_code: int, message: str,):
    try:
        assert response.status_code == expected_status_code, f"{message}. Статус код: {response.status_code}"
    except AssertionError as e:
        pytest.fail(e)


def search_by_slug(response_data):
    # В этой функции мы ищем все сущности "slug"
    search_slug = parse('$..slug')
    urls_list = [match.value for match in search_slug.find(response_data)]
    assert urls_list, "Список Url пустой"
    return urls_list


def create_url_list():
    url = f'{get_info_url}/table-of-contents'
    response = requests.get(url)
    check_response_status_code(response, expected_status_code=200, message=f"Ошибка при поиске списка вкладок: {url}")
    response_data = response.json()

    # Ищем все URL И создаем из них список
    urls_list = search_by_slug(response_data)
    return urls_list