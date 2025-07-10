from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.menu_page import MenuPage
import pytest
from pathlib import Path

# No BaseTest needed, use fixtures directly

@pytest.mark.smoke
def test_successful_login(goto_page):
    """E2E: Successful login as standard_user"""
    page = goto_page("")  # Go to the base page
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.login('standard_user', 'secret_sauce')  # Perform login by standard_user
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.expect_title_contains_text('Products')  # Assert successful login
    

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
    checkout_page.expect_confirmation_to_have_text('Thank you for your order!')  # Assert order success
    
    
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
def test_reset_app_state(goto_page): 
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
def test_product_names_have_no_invalid_symbols(goto_page):
    """E2E: Ensure product names do not contain invalid symbols like 'text.text()'"""
    page = goto_page()  # Go to inventory page
    product_page= ProductsPage(page)  # Create ProductsPage object
    product_page.assert_product_names_have_no_invalid_symbols()  # Assert product names do not contain invalid symbols

@pytest.mark.full_run
def test_product_descriptions_have_no_invalid_symbols(goto_page):
    """E2E: Ensure product descriptions do not contain invalid symbols like 'text.text()'"""
    page = goto_page()  # Go to inventory page
    product_page= ProductsPage(page)  # Create ProductsPage object
    product_page.assert_product_descriptions_have_no_invalid_symbols()  # Assert product names do not contain invalid symbols


@pytest.mark.smoke
def test_click_menu_all_items(goto_page):
    """E2E: Click menu and verify 'All Items' is selected"""
    page = goto_page()  # Go to inventory page
    menu_page = MenuPage(page)  # Create MenuPage object
    menu_page.open_menu()  # Open menu
    menu_page.click_all_items()  # Click 'All Items'

@pytest.mark.smoke
def test_click_menu_all_items_on_cart_page(goto_page):
    """E2E: Click menu and verify 'All Items' is selected on cart page"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.add_to_cart('sauce-labs-backpack')  # Add backpack to cart
    products_page.open_cart()  # Open cart
    menu_page = MenuPage(page)  # Create MenuPage object
    menu_page.open_menu()  # Open menu
    menu_page.click_all_items()  # Click 'All Items'

@pytest.mark.smoke
def test_click_about(goto_page):
    """E2E: Click 'About' link in menu and verify navigation to about page"""
    page = goto_page()  # Go to inventory page
    menu_page = MenuPage(page)  # Create MenuPage object
    menu_page.open_menu()  # Open menu
    menu_page.click_about()  # Click 'About' link

@pytest.mark.full_run
def test_click_facebook_button(goto_page):
    """E2E: Click Facebook button in footer and verify navigation to Facebook page"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.click_facebook_button()  # Click Facebook button


@pytest.mark.full_run
def test_click_x_button(goto_page):
    """E2E: Click X button in footer and verify navigation to X page"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.click_x_button()  # Click X button

@pytest.mark.full_run
def test_click_linkedin_button(goto_page):
    """E2E: Click LinkedIn button in footer and verify navigation to LinkedIn page"""
    page = goto_page()  # Go to inventory page
    products_page = ProductsPage(page)  # Create ProductsPage object
    products_page.click_linkedin_button()  # Click LinkedIn button

@pytest.mark.smoke
def test_logout(goto_page):
    """E2E: Login and logout"""
    page = goto_page()  # Go to inventory page
    menu_page = MenuPage(page)  # Create MenuPage object
    menu_page.open_menu()  # Open menu
    menu_page.logout()  # Click logout
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.expect_logged_out()  # Assert logged out


@pytest.mark.smoke
def test_unsuccessful_login_locked_out_user(goto_page):
    """E2E: Unsuccessful login as locked_out_user"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.login('locked_out_user', 'secret_sauce')  # Try to login as locked_out_user
    login_page.expect_login_error("Epic sadface: Sorry, this user has been locked out.")  # Assert error is visible and text correct


@pytest.mark.full_run
def test_unsuccessful_login_invalid_user(goto_page):
    """E2E: Unsuccessful login with invalid user"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.login('invalid_user', 'secret_sauce')  # Try to login with invalid user
    login_page.expect_login_error("Epic sadface: Username and password do not match any user in this service")  # Assert error is visible and text correct


@pytest.mark.full_run
def test_unsuccessful_login_invalid_password(goto_page):
    """E2E: Unsuccessful login with invalid password"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.login('standard_user', 'wrong_password')  # Try to login with wrong password
    login_page.expect_login_error("Epic sadface: Username and password do not match any user in this service")  # Assert error is visible


@pytest.mark.full_run
def test_unsuccessful_login_empty_fields(goto_page):
    """E2E: Unsuccessful login with empty username and password fields"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.login('', '')  # Try to login with empty fields
    login_page.expect_login_error("Epic sadface: Username is required")  # Assert error is visible and text correct 


@pytest.mark.full_run
def test_unsuccessful_login_empty_username(goto_page):
    """E2E: Unsuccessful login with empty username field"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.login('', 'secret_sauce')  # Try to login with empty username
    login_page.expect_login_error("Epic sadface: Username is required")  # Assert error is visible and text correct


@pytest.mark.full_run
def test_unsuccessful_login_empty_password(goto_page):
    """E2E: Unsuccessful login with empty password field"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)  # Create LoginPage object
    login_page.login('standard_user', '')  # Try to login with empty password
    login_page.expect_login_error("Epic sadface: Password is required")  # Assert error is visible and text correct

@pytest.mark.smoke
def test_capture_expected_screenshots(goto_page):
    """
    Capture and save screenshots for each main page object to tests/expected_screenshots.
    """
    screenshots_dir = Path('tests/expected_screenshots')
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Login Page
    page = goto_page("")
    login_page = LoginPage(page)
    login_page.page.screenshot(path=str(screenshots_dir / 'login_page_expected.png'), full_page=True)

    # Products Page
    login_page.login('standard_user', 'secret_sauce')
    products_page = ProductsPage(page)
    products_page.page.screenshot(path=str(screenshots_dir / 'products_page_expected.png'), full_page=True)

    # Cart Page
    products_page.add_to_cart('sauce-labs-backpack')
    products_page.open_cart()
    cart_page = CartPage(page)
    cart_page.page.screenshot(path=str(screenshots_dir / 'cart_page_expected.png'), full_page=True)

    # Checkout Page
    cart_page.checkout()
    checkout_page = CheckoutPage(page)
    checkout_page.page.screenshot(path=str(screenshots_dir / 'checkout_page_expected.png'), full_page=True)

    # Menu Page (open menu on products page)
    page = goto_page()
    menu_page = MenuPage(page)
    menu_page.open_menu()
    menu_page.page.screenshot(path=str(screenshots_dir / 'menu_page_expected.png'), full_page=True)
    menu_page.close_menu()


