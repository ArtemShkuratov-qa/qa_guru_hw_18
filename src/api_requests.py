import requests
from utils.attach_function import response_logging, response_attaching


def sending_api_request(base_api_url, endpoint, **kwargs):
    url = f"{base_api_url}{endpoint}"
    response = requests.post(url, **kwargs)
    response_logging(response) # логирование запроса и ответа
    response_attaching(response) # добавление аттачей
    return response