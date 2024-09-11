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
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        pytest.exit(e)

    # Ищем все URL И создаем из них список
    return search_by_slug(response.json())