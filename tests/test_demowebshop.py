from src.cart import Cart
from data.data import WEB_URL


cart = Cart()
def test_add_featured_products_to_cart(api_authorization, add_first_featured_product_to_cart, add_second_featured_product_to_cart):
    cart.open_page(WEB_URL)
    cart.set_cookie(api_authorization, WEB_URL)
    cart.open_cart()
    cart.number_of_positions(2)
    cart.check_quantity('1')


def test_electronic_product_to_cart(api_authorization, add_electronic_product_to_cart):
    cart.open_page(WEB_URL)
    cart.set_cookie(api_authorization, WEB_URL)
    cart.open_cart()
    cart.number_of_positions(1)
    cart.check_quantity('1')