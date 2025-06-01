import allure
from selene import browser, have


class Cart():

    @allure.step('Открываем страницу магазина')
    def open_page(self, value):
        browser.open(value)


    @allure.step('Устанавливаем авторизационную куку')
    def set_cookie(self, cookie_value, page_url):
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie_value})
        browser.open(page_url)


    @allure.step('Переходим в корзину')
    def open_cart(self):
        browser.element('#topcartlink').click()


    @allure.step('Проверяем количество добавленных позиций')
    def number_of_positions(self, value):
        browser.element('.cart').all('.cart-item-row').should(have.size(value))


    @allure.step('Проверяем количество товара в каждой из позиций')
    def check_quantity(self, value):
        browser.element('.qty-input').should(have.value(value))