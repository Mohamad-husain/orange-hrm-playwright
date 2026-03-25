import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from data.constants import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    yield page


@pytest.fixture
def admin_login(page):
    """Login once and return logged-in page"""
    login = LoginPage(page)
    login.navigate()
    login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    page.wait_for_load_state("networkidle")
    return page