from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.menu_page import MenuPage
# No BaseTest needed, use fixtures directly

def test_successful_login(goto_page):
    """E2E: Successful login as standard_user"""
    page = goto_page("")
    login_page = LoginPage(page)
    login_page.login('standard_user', 'secret_sauce')
    products_page = ProductsPage(page)
    expect(products_page.get_title()).to_have_text('Products')


def test_add_single_item_to_cart_and_checkout(goto_page):
    """E2E: Add 'Sauce Labs Backpack' to cart and checkout"""
    page = goto_page()
    products_page = ProductsPage(page)
    products_page.add_to_cart('sauce-labs-backpack')
    products_page.open_cart()
    cart_page = CartPage(page)
    cart_page.checkout()
    checkout_page = CheckoutPage(page)
    checkout_page.fill_checkout_info('John', 'Doe', '12345')
    checkout_page.finish()
    expect(checkout_page.get_confirmation()).to_have_text('Thank you for your order!')


def test_remove_item_from_cart(goto_page):
    """E2E: Add and remove 'Sauce Labs Bike Light' from cart"""
    page = goto_page()
    products_page = ProductsPage(page)
    products_page.add_to_cart('sauce-labs-bike-light')
    products_page.open_cart()
    cart_page = CartPage(page)
    cart_page.remove_item('sauce-labs-bike-light')
    assert cart_page.is_cart_empty()


def test_sort_products_low_to_high(goto_page):
    """E2E: Sort products by price low to high and verify order changes"""
    page = goto_page()
    products_page = ProductsPage(page)
    # Sort by price low to high
    products_page.select_option('lohi')
    products_page.page.wait_for_selector('.inventory_item', state='visible')
    first_item = products_page.page.locator('.inventory_item').first
    assert 'Sauce Labs Onesie' in first_item.inner_text()


def test_add_multiple_items_and_verify_cart_count(goto_page):
    """E2E: Add multiple items to cart and verify cart badge count"""
    page = goto_page()
    products_page = ProductsPage(page)
    products_page.add_to_cart('sauce-labs-backpack')
    products_page.add_to_cart('sauce-labs-bike-light')
    products_page.add_to_cart('sauce-labs-bolt-t-shirt')
    badge = page.locator('.shopping_cart_badge')
    assert badge.inner_text() == '3'
    

def test_checkout_with_missing_info(goto_page):
    """E2E: Try to checkout with missing info and verify error message"""
    page = goto_page()
    products_page = ProductsPage(page)
    products_page.add_to_cart('sauce-labs-backpack')
    products_page.open_cart()
    cart_page = CartPage(page)
    cart_page.checkout()
    checkout_page = CheckoutPage(page)
    checkout_page.fill_checkout_info('', 'Doe', '12345')
    error = page.locator('*[data-test="error"]')
    assert error.is_visible()



def test_reset_app_state(goto_page): #update
    """E2E: Add item, reset app state, and verify cart is empty"""
    page = goto_page('cart.html')
    cart_page = CartPage(page)
    cart_page.click_continue_shopping()
    menu_page = MenuPage(page)
    menu_page.open_menu()
    page.click('//a[@data-test="reset-sidebar-link"]')
    assert not page.locator('.shopping_cart_badge').is_visible()



def test_cart_continue_shopping(goto_page):
    """E2E: Go to cart, click 'Continue Shopping', and verify navigation to products page"""
    page = goto_page()
    products_page = ProductsPage(page)
    products_page.open_cart()
    cart_page = CartPage(page)
    cart_page.click_continue_shopping()
    assert 'inventory.html' in page.url


def test_logout(goto_page):
    """E2E: Login and logout"""
    page = goto_page()
    menu_page = MenuPage(page)
    menu_page.open_menu()
    menu_page.logout()
    expect(page.locator('input[data-test="login-button"]')).to_be_visible()


def test_unsuccessful_login_locked_out_user(goto_page):
    """E2E: Unsuccessful login as locked_out_user"""
    page = goto_page()
    login_page = LoginPage(page)
    login_page.login('locked_out_user', 'secret_sauce')
    expect(login_page.get_error()).to_be_visible()
