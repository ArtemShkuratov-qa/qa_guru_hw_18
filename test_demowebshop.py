import json
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser
from selene.support.conditions import have
from jsonschema import validate
import allure


WEB_URL = 'https://demowebshop.tricentis.com'
API_URL = 'https://demowebshop.tricentis.com'
LOGIN = 'artem.sh@gmail.com'
PASSWORD = 'Vjzbz##dGa@T98'



def test_add_featured_products_to_cart():
    payload = ("product_attribute_74_5_26=81&"
               "product_attribute_74_6_27=83&"
               "product_attribute_74_3_28=86&"
               "product_attribute_74_8_29=89&"
               "addtocart_74.EnteredQuantity=1")


    with step("Авторизация через API"):
        result = requests.post(
            url=API_URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="text")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="text")


    with step("Получение авторизационной куки"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")


    with step("Усатновка авторизационной куки"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL)


    with step("Добавление первого продукта через API"):
        api_response = requests.post(API_URL + '/addproducttocart/details/74/1', headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies={"NOPCOMMERCE.AUTH": cookie}, data=payload)

        with open('schemas/add_product_schema.json') as file:
            schema = json.load(file)
        validate(instance=api_response.json(), schema=schema)
        assert api_response.status_code == 200
        assert api_response.json()['success'] == True
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="text")
        allure.attach(body=json.dumps(api_response.json(), indent=4, ensure_ascii=True), name="Response", attachment_type=AttachmentType.JSON, extension="json")


    with step("Добавление второго продукта через API"):
        api_response = requests.post(API_URL + '/addproducttocart/catalog/31/1/1', cookies={"NOPCOMMERCE.AUTH": cookie})

        with open('schemas/add_product_schema.json') as file:
            schema = json.load(file)
        validate(instance=api_response.json(), schema=schema)
        assert api_response.status_code == 200
        assert api_response.json()['success'] == True
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="text")
        allure.attach(body=json.dumps(api_response.json(), indent=4, ensure_ascii=True), name="Response", attachment_type=AttachmentType.JSON, extension="json")


    with step("Проверка корзины"):
        browser.element('#topcartlink').click()
        browser.element('.cart').all('.cart-item-row').should(have.size(2))
        browser.element('.qty-input').should(have.value('1'))


def test_add_one_product_to_cart():
    with step("Авторизация через API"):
        result = requests.post(
            url=API_URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")


    with step("Получение авторизационной куки"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")


    with step("Усатновка авторизационной куки"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL)


    with step("Добавление продукта через API"):
        api_response = requests.post(API_URL + '/addproducttocart/catalog/43/1/1', headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies={"NOPCOMMERCE.AUTH": cookie})

        with open('schemas/add_product_schema.json') as file:
            schema = json.load(file)
        validate(instance=api_response.json(), schema=schema)
        assert api_response.status_code == 200
        assert api_response.json()['success'] == True
        allure.attach(body=json.dumps(api_response.json(), indent=4, ensure_ascii=True), name="Response", attachment_type=AttachmentType.JSON, extension="json")


    with step("Проверка корзины"):
        browser.element('#topcartlink').click()
        browser.element('.cart').all('.cart-item-row').should(have.size(1))
        browser.element('.qty-input').should(have.value('1'))