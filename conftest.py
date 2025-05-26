import pytest
import base64

from utils.read_config import AppConfiguration
from playwright.sync_api import sync_playwright


@pytest.fixture()
def setup(request):
    configuration = AppConfiguration.get_app_configuration()
    common_info = AppConfiguration.get_common_info()
    base_url = common_info["Url"]

    # Browser options
    headless = eval(configuration["Headless"])  # convert to bool
    slow_mo = float(configuration["SlowMo"])
    launch_options = {
        "headless": headless,
        "slow_mo": slow_mo,
        "args": [
            '--start-maximized',
            '--disable-dev-shm-usage',  # Helps with memory issues in Docker/CI
            '--no-sandbox',  # Required for running Chrome in containers
            '--disable-gpu',  # Optional: helps with headless mode in some environments
        ]
    }

    # Start Playwright
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(**launch_options)

    context_options = {'base_url': base_url}

    # Browser context settings
    browser_context = browser.new_context(**context_options, no_viewport=True)
    browser_context.set_default_navigation_timeout(float(configuration["DefaultNavigationTimeout"]))
    browser_context.set_default_timeout(float(configuration["DefaultTimeout"]))

    # Create Page
    page = browser_context.new_page()

    request.cls.page = page
    page.goto(base_url)

    yield page
    page.close()
    browser.close()
    playwright.stop()

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
        if (report.failed or xfail) and page is not None:
            screenshot_bytes = page.screenshot()
            extra.append(pytest_html.extras.image(base64.b64encode(screenshot_bytes).decode(), ''))

        report.extras = extra