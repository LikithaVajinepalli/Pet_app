import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5001"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")   # remove this line to watch the browser
    options.add_argument("--window-size=1280,900")
    # Selenium 4.6+ finds the matching ChromeDriver itself (Selenium Manager),
    # so webdriver-manager is no longer needed.
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_home_page_loads_with_stats(driver):
    driver.get(BASE_URL + "/")
    assert "Pet Rescue" in driver.title
    page = driver.page_source
    assert "Total" in page
    assert "Available" in page
    assert "Adopted" in page


def test_view_pets_page_loads(driver):
    driver.get(BASE_URL + "/pets")
    assert driver.title == "All Pets"
    assert driver.find_element(By.TAG_NAME, "table")


def test_add_pet_and_view(driver):
    driver.get(BASE_URL + "/add")
    driver.find_element(By.NAME, "name").send_keys("Selenium Test Pet")
    driver.find_element(By.NAME, "type").send_keys("Dog")
    driver.find_element(By.TAG_NAME, "button").click()

    WebDriverWait(driver, 5).until(EC.url_contains("/pets"))
    table = driver.find_element(By.TAG_NAME, "table").text
    assert "Selenium Test Pet" in table
    assert "Dog" in table
