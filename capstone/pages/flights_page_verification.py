from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FlightsPage:

    search_flights_text = (By.XPATH, "//span[normalize-space()='Search Flights']")

    def __init__(self, driver):
        self.driver = driver

    def get_current_url(self):
        return self.driver.current_url

    def get_page_title(self):
        return self.driver.title

    def is_search_flights_visible(self):
        wait = WebDriverWait(self.driver,10)
        element = wait.until(
            EC.visibility_of_element_located(self.search_flights_text)
        )
        return element.is_displayed()