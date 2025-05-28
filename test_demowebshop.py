import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser
from selene.support.conditions import have,be
import allure


WEB_URL = 'https://demowebshop.tricentis.com'
API_URL = 'https://demowebshop.tricentis.com'
LOGIN = 'artem.sh@gmail.com'
PASSWORD = 'Vjzbz##dGa@T98'

def test_add_one_product_to_cart():
    with step("Login with API"):
        result = requests.post(
            url=API_URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with step("Get cookie from API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    payload = "product_attribute_74_5_26=81&product_attribute_74_6_27=83&product_attribute_74_3_28=86&product_attribute_74_8_29=89&addtocart_74.EnteredQuantity=1"

    with step("Add product from API"):
        api_response = requests.post(API_URL + '/addproducttocart/details/74/1', headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies={"NOPCOMMERCE.AUTH": cookie}, data=payload)
        assert api_response.status_code == 200
        assert api_response.json()['success'] == True


    with step("Set cookie from API"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL)



    with step("Check cart"):
        browser.element('#topcartlink').click()
        browser.element('.cart').all('.cart-item-row').should(have.size(3))
        browser.all('.qty-input').should(have.values('1'))
        pass
