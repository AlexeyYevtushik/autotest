from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.menu_page import MenuPage
import pytest

# No BaseTest needed, use fixtures directly
pytestmark = pytest.mark.user(["visual_user"])

@pytest.mark.smoke
def test_visual_product_page(goto_page):
    """E2E: Visual check of product page"""
    page = goto_page()
    products_page = ProductsPage(page)
    products_page.check_page_image()  # Visual check of product page

@pytest.mark.smoke
def test_visual_cart_page(goto_page):
    """E2E: Visual check of cart page"""
    page = goto_page()
    products_page = ProductsPage(page)
    products_page.add_to_cart('sauce-labs-backpack')  # Add product to cart   
    products_page.open_cart()  # Open the cart
    cart_page = CartPage(page)
    cart_page.check_page_image()  # Visual check of cart page

@pytest.mark.smoke
def test_visual_checkout_page(goto_page):
    """E2E: Visual check of checkout page"""
    page = goto_page()
    products_page = ProductsPage(page)
    products_page.add_to_cart('sauce-labs-backpack')  # Add product to cart
    products_page.open_cart()  # Open the cart
    cart_page = CartPage(page)
    cart_page.checkout()  # Proceed to checkout
    checkout_page = CheckoutPage(page)
    checkout_page.check_page_image()  # Visual check of checkout page


@pytest.mark.smoke
def test_visual_menu_page(goto_page):
    """E2E: Visual check of menu page"""
    page = goto_page()
    products_page = ProductsPage(page)
    products_page.add_to_cart('sauce-labs-backpack')  # Add product to cart
    menu_page = MenuPage(page)
    menu_page.open_menu()  # Open the menu
    menu_page.check_page_image()  # Visual check of menu page
    

