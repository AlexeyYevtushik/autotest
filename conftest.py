import pytest
import base64

from utils.read_config import AppConfiguration
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session",autouse=True)
def browser_resources():
    configuration = AppConfiguration.get_app_configuration()
    common_info = AppConfiguration.get_common_info()
    base_url = common_info["Url"]

    headless = eval(configuration["Headless"])
    slow_mo = float(configuration["SlowMo"])
    launch_options = {
        "headless": headless,
        "slow_mo": slow_mo,
        "args": [
            '--start-maximized',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-gpu',
        ]
    }
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(**launch_options)
    context_options = {'base_url': base_url}
    browser_context = browser.new_context(**context_options, no_viewport=True)
    browser_context.set_default_navigation_timeout(float(configuration["DefaultNavigationTimeout"]))
    browser_context.set_default_timeout(float(configuration["DefaultTimeout"]))
    page = browser_context.new_page()
    yield page, browser, playwright
    # Teardown will be handled in a separate fixture


@pytest.fixture(scope="session")
def teardown_browser(browser_resources):
    yield
    page, browser, playwright = browser_resources
    try:
        page.close()
    except Exception:
        pass
    try:
        browser.close()
    except Exception:
        pass
    try:
        playwright.stop()
    except Exception:
        pass


@pytest.fixture(scope="session", autouse=True)
def browser_page(browser_resources):
     page, _, _ = browser_resources
     base_url = AppConfiguration.get_common_info()["Url"]
     page.goto(base_url, timeout=int(AppConfiguration.get_app_configuration()["DefaultNavigationTimeout"]))
     page.wait_for_selector('input[data-test="username"]:not([disabled])', state='visible', timeout=int(AppConfiguration.get_app_configuration()["DefaultTimeout"]))
     yield page
        # This fixture is used to ensure the page is always initialized before tests run



# @pytest.fixture(scope="session")
# def logged_page(browser_resources):
#     page, _, _ = browser_resources
#     base_url = AppConfiguration.get_common_info()["Url"]
#     if not (page.url.endswith('inventory.html') and page.locator('.inventory_list').is_visible()):
#         page.goto(base_url)
#         page.wait_for_selector('input[data-test="username"]:not([disabled])', state='visible')
#         from pages.login_page import LoginPage
#         login_page = LoginPage(page)
#         login_page.login('standard_user', 'secret_sauce')
#         page.wait_for_selector('.inventory_list', state='visible')
#     if not page.url.endswith('inventory.html'):
#         page.goto(base_url + 'inventory.html')
#         page.wait_for_selector('.inventory_list', state='visible')
#     yield page


# @pytest.fixture(scope="function")
# def back_to_home_screen(browser_resources):
#     page, _, _ = browser_resources
#     yield page
#     if not (page.url.endswith('inventory.html') and page.locator('.inventory_list').is_visible()):
#         page.goto(base_url)
#         page.wait_for_selector('input[data-test="username"]:not([disabled])', state='visible')
#         from pages.login_page import LoginPage
#         login_page = LoginPage(page)
#         login_page.login('standard_user', 'secret_sauce')
#         page.wait_for_selector('.inventory_list', state='visible')
#     if not page.url.endswith('inventory.html'):
#         base_url = AppConfiguration.get_common_info()["Url"]
#         print(base_url + 'inventory.html')
#         page.goto(base_url + 'inventory.html')
#         page.wait_for_selector('.inventory_list', state='visible')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    screenshot_bytes = ''
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')

        # Try to get the page from the test class instance
        page = getattr(item.instance, "page", None)
        if (report.failed or xfail) and page is not None and pytest_html is not None:
            screenshot_bytes = page.screenshot()
            extra.append(pytest_html.extras.image(base64.b64encode(screenshot_bytes).decode(), ''))

        if hasattr(report, 'extras'):
            report.extras = extra