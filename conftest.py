import allure
import pytest
import requests
from allure_commons.types import AttachmentType
from selene import browser


@pytest.fixture(scope='function', autouse=True)
def clean_cart():
    yield
    for i in range(len(browser.element('.cart').all('.cart-item-row'))):
        browser.element('[name=removefromcart]').click()
        browser.element('[name=updatecart]').click()