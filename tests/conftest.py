import allure
import pytest
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser
from src.api_requests import sending_api_request
from data.data import API_URL, LOGIN, PASSWORD

@pytest.fixture(scope='function', autouse=True)
def clean_cart():
    yield
    for i in range(len(browser.element('.cart').all('.cart-item-row'))):
        browser.element('[name=removefromcart]').click()
        browser.element('[name=updatecart]').click()


@pytest.fixture(scope='function')
def api_authorization():
    result = requests.post(
        url=API_URL + "/login",
        data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
        allow_redirects=False
    )
    cookie = result.cookies.get("NOPCOMMERCE.AUTH")
    allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="text")
    allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="text")
    return cookie


@pytest.fixture(scope='function')
def add_first_featured_product_to_cart(api_authorization):
    payload = ("product_attribute_74_5_26=81&"
               "product_attribute_74_6_27=83&"
               "product_attribute_74_3_28=86&"
               "product_attribute_74_8_29=89&"
               "addtocart_74.EnteredQuantity=1")

    with step("Добавление первого продукта через API"):
        result = sending_api_request(
            API_URL,
            '/addproducttocart/details/74/1',
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            cookies={"NOPCOMMERCE.AUTH": api_authorization},
            data=payload
        )

        assert result.status_code == 200
        assert result.json()['success'] == True


@pytest.fixture(scope='function')
def add_second_featured_product_to_cart(api_authorization):
    with step("Добавление второго продукта через API"):
        result = sending_api_request(
            API_URL,
            '/addproducttocart/catalog/31/1/1',
            cookies={"NOPCOMMERCE.AUTH": api_authorization}
        )

        assert result.status_code == 200
        assert result.json()['success'] == True


@pytest.fixture(scope='function')
def add_electronic_product_to_cart(api_authorization):
    with step("Добавление второго продукта через API"):
        result = sending_api_request(
            API_URL,
            '/addproducttocart/catalog/31/1/1',
            cookies={"NOPCOMMERCE.AUTH": api_authorization}
        )

        assert result.status_code == 200
        assert result.json()['success'] == True