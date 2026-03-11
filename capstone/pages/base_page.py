from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def click(self, locator):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def type(self, locator, text):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.clear()
        element.send_keys(text)

    def wait_for_value(self, locator):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        self.wait.until(
            lambda driver: element.get_attribute("value") != ""
        )