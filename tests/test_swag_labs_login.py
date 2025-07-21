from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.menu_page import MenuPage
import pytest
from pathlib import Path

pytestmark = pytest.mark.user(["standard_user"])



@pytest.mark.full_run
def test_unsuccessful_login_locked_out_user(goto_page):
    """E2E: Unsuccessful login as locked_out_user"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)
    login_page.login('locked_out_user', 'secret_sauce')  # Try to login as locked_out_user
    login_page.expect_login_error("Epic sadface: Sorry, this user has been locked out.")  # Assert error is visible and text correct


@pytest.mark.full_run
def test_unsuccessful_login_invalid_user(goto_page):
    """E2E: Unsuccessful login with invalid user"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)
    login_page.login('invalid_user', 'secret_sauce')  # Try to login with invalid user
    login_page.expect_login_error("Epic sadface: Username and password do not match any user in this service")  # Assert error is visible and text correct


@pytest.mark.full_run
def test_unsuccessful_login_invalid_password(goto_page):
    """E2E: Unsuccessful login with invalid password"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)
    login_page.login('standard_user', 'wrong_password')  # Try to login with wrong password
    login_page.expect_login_error("Epic sadface: Username and password do not match any user in this service")  # Assert error is visible


@pytest.mark.full_run
def test_unsuccessful_login_empty_fields(goto_page):
    """E2E: Unsuccessful login with empty username and password fields"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)
    login_page.login('', '')  # Try to login with empty fields
    login_page.expect_login_error("Epic sadface: Username is required")  # Assert error is visible and text correct 


@pytest.mark.full_run
def test_unsuccessful_login_empty_username(goto_page):
    """E2E: Unsuccessful login with empty username field"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)
    login_page.login('', 'secret_sauce')  # Try to login with empty username
    login_page.expect_login_error("Epic sadface: Username is required")  # Assert error is visible and text correct


@pytest.mark.full_run
def test_unsuccessful_login_empty_password(goto_page):
    """E2E: Unsuccessful login with empty password field"""
    page = goto_page("")  # Go to inventory page
    login_page = LoginPage(page)
    login_page.login('standard_user', '')  # Try to login with empty password
    login_page.expect_login_error("Epic sadface: Password is required")  # Assert error is visible and text correct

@pytest.mark.smoke
def test_capture_expected_screenshots(goto_page):
    """
    Capture and save screenshots for each main page object to tests/expected_screenshots.
    """
    screenshots_dir = Path('tests/tmp')
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Login Page
    page = goto_page("")
    login_page = LoginPage(page)

    # Products Page
    login_page.login('standard_user', 'secret_sauce')
    menu_page = MenuPage(page)
    menu_page.open_menu()
    menu_page.page.screenshot(path=str(screenshots_dir / 'menu_page_expected.png'), full_page=True)
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



