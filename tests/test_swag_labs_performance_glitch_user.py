from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.menu_page import MenuPage
import pytest
# No BaseTest needed, use fixtures directly

@pytest.mark.smoke
def test_successful_login(goto_page):
    """E2E: Successful login as standard_user"""
    page = goto_page("")  # Go to the base page
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.login('performance_glitch_user', 'secret_sauce')  # Perform login
    products_page = ProductsPage(page)  # Create ProductsPage object
    expect(products_page.get_title()).to_have_text('Products')  # Assert successful login


@pytest.mark.smoke
def test_add_single_item_to_cart_and_checkout(goto_page):
    """E2E: Add 'Sauce Labs Backpack' to cart and checkout"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.add_to_cart('sauce-labs-backpack')  # Add backpack to cart
    products_page.open_cart()  # Open cart
    cart_page = CartPage(page)  # Create CartPage object
    cart_page.checkout()  # Click checkout
    checkout_page = CheckoutPage(page)  # Create CheckoutPage object
    checkout_page.fill_checkout_info('John', 'Doe', '12345')  # Fill checkout info
    checkout_page.finish()  # Finish checkout
    expect(checkout_page.get_confirmation()).to_have_text('Thank you for your order!')  # Assert order success


@pytest.mark.smoke
def test_remove_item_from_cart(goto_page):
    """E2E: Add and remove 'Sauce Labs Bike Light' from cart"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.add_to_cart('sauce-labs-bike-light')  # Add bike light to cart
    products_page.open_cart()  # Open cart
    cart_page = CartPage(page)  # Create CartPage object
    cart_page.remove_item('sauce-labs-bike-light')  # Remove bike light from cart
    cart_page.assert_cart_is_empty()  # Assert cart is empty


@pytest.mark.full_run
def test_sort_products_low_to_high(goto_page):
    """E2E: Sort products by price low to high and verify order changes"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.select_option('lohi')  # Sort by price low to high
    products_page.assert_first_item('Sauce Labs Onesie')  # Assert first item is the cheapest


@pytest.mark.full_run
def test_sort_products_high_to_low(goto_page):
    """E2E: Sort products by price high to low and verify order changes"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.select_option('hilo')  # Sort by price high to low
    products_page.assert_first_item('Sauce Labs Fleece Jacket')  # Assert first item is the most expensive


@pytest.mark.full_run
def test_sort_products_alphabetical(goto_page):
    """E2E: Sort products alphabetically and verify order changes"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.select_option('az')  # Sort alphabetically A-Z
    products_page.assert_first_item('Sauce Labs Backpack')  # Assert first item is alphabetically first


@pytest.mark.full_run
def test_sort_products_reverse_alphabetical(goto_page):
    """E2E: Sort products in reverse alphabetical order and verify order changes"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.select_option('za')  # Sort alphabetically Z-A
    products_page.assert_first_item('Test.allTheThings() T-Shirt (Red)')  # Assert first item is alphabetically last


@pytest.mark.smoke
def test_add_multiple_items_and_verify_cart_count(goto_page):
    """E2E: Add multiple items to cart and verify cart badge count"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.add_to_cart('sauce-labs-backpack')  # Add backpack to cart
    products_page.add_to_cart('sauce-labs-bike-light')  # Add bike light to cart
    products_page.add_to_cart('sauce-labs-bolt-t-shirt')  # Add bolt t-shirt to cart
    products_page.assert_number_on_badge(3)  # Assert cart badge shows 3


@pytest.mark.full_run
def test_checkout_with_missing_info(goto_page):
    """E2E: Try to checkout with missing info and verify error message"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.add_to_cart('sauce-labs-backpack')  # Add backpack to cart
    products_page.open_cart()  # Open cart
    cart_page = CartPage(page)  # Create CartPage object
    cart_page.checkout()  # Click checkout
    checkout_page = CheckoutPage(page)  # Create CheckoutPage object
    checkout_page.fill_checkout_info('', 'Doe', '12345')  # Leave first name blank
    checkout_page.assert_error_is_visible()  # Assert error is visible


@pytest.mark.smoke
def test_reset_app_state(goto_page): #update
    """E2E: Add item, reset app state, and verify cart is empty on Products page"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.add_to_cart('sauce-labs-backpack')  # Add backpack to cart
    products_page.open_cart()  # Open cart
    cart_page = CartPage(page)  # Create CartPage object
    cart_page.click_continue_shopping()  # Click continue shopping
    menu_page = MenuPage(page)  # Create MenuPage object
    menu_page.open_menu()  # Open menu
    menu_page.click_reset_app_state_on_products_page()  # Click reset app state


@pytest.mark.smoke
def test_reset_app_state_cart_on_cart_page(goto_page):
    """E2E: Add item, reset app state, and verify cart is empty on Products page"""
    page = goto_page()
    page.reload()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.add_to_cart('sauce-labs-backpack')  # Add backpack to cart
    products_page.open_cart()  # Open cart
    menu_page = MenuPage(page)  # Create MenuPage object
    menu_page.open_menu()  # Open menu
    menu_page.click_reset_app_state_on_cart_page()  # Click reset app state


@pytest.mark.smoke
def test_cart_continue_shopping(goto_page):
    """E2E: Go to cart, click 'Continue Shopping', and verify navigation to products page"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.open_cart()  # Open cart
    cart_page = CartPage(page)  # Create CartPage object
    cart_page.click_continue_shopping()  # Click continue shopping


@pytest.mark.full_run
def test_all_product_images_are_unique(goto_page):
    """E2E: Check that every product image on the inventory page is unique"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page) 
    products_page.check_images_unique()  # Check that all product images are unique


@pytest.mark.full_run
def test_product_names_and_descriptions_no_invalid_symbols(goto_page):
    """E2E: Ensure product names and descriptions do not contain invalid symbols like 'text.text()'"""
    page = goto_page()  # Go to inventory page
    product_page= ProductsPage(page)  # Create ProductsPage object
    product_page.assert_product_names_and_descriptions_no_invalid_symbols()  # Assert product names and descriptions do not contain invalid symbols
  

@pytest.mark.smoke
def test_logout(goto_page):
    """E2E: Login and logout"""
    page = goto_page()  # Go to inventory page
    menu_page = MenuPage(page)  # Create MenuPage object
    menu_page.open_menu()  # Open menu
    menu_page.logout()  # Click logout
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.expect_logged_out()  # Assert logged out



