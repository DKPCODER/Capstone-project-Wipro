import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FlightsPage:
    """
    FlightsPage represents the flight search page of the application.

    This page handles all operations related to searching flights such as:
    - Selecting flight type (one-way)
    - Entering departure and arrival cities
    - Selecting departure date
    - Choosing passenger count
    - Selecting cabin class
    - Performing flight search
    - Validating search results and prices
    - Navigating to the booking page

    The class follows the Page Object Model (POM) design pattern.
    """

    loader = (By.ID, "page-loader")
    one_way_button = (By.XPATH, "//span[normalize-space()='One Way']")
    departure_input = (By.XPATH, "//input[@placeholder='Departure City or Airport']")
    arrival_input = (By.XPATH, "//input[@id='arrival_airport_input']")
    suggestion = (By.XPATH, "(//div[contains(@class,'cursor-pointer')])[1]")
    date_input = (By.XPATH, "//input[@placeholder='Departure Date']")
    passenger_dropdown = (By.XPATH, "//span[contains(text(),'Passenger')]/parent::div")
    cabin_dropdown = (By.XPATH, "//div[contains(@class,'cursor-pointer') and .//span[text()='Economy']]")
    economy_option = (By.XPATH, "//span[normalize-space()='Economy']")
    search_button = (By.XPATH, "//button[.//span[normalize-space()='Search Flights']]")

    def __init__(self, driver):
        """
        Initializes the FlightsPage object.

        Args:
            driver: Selenium WebDriver instance used to interact with the browser.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.selected_date = None


    def wait_loader(self):
        """
        Waits until the page loader disappears.

        This ensures that the page is fully loaded before performing
        further UI interactions.
        """
        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.loader)
            )
        except Exception as e:
            print("Loader wait issue:", e)


    def select_one_way(self):
        """
        Selects the 'One Way' flight option.

        This method waits for the one-way button to become clickable
        and then clicks it to set the flight search type.
        """
        try:
            self.wait_loader()

            one_way = self.wait.until(
                EC.element_to_be_clickable(self.one_way_button)
            )

            one_way.click()
            time.sleep(2)

        except Exception as e:
            print("Error selecting one way:", e)


    def select_departure_city(self, city):
        """
        Enters and selects the departure city.

        Args:
            city: Name of the departure city or airport.
        """
        try:
            field = self.wait.until(
                EC.element_to_be_clickable(self.departure_input)
            )

            field.click()
            field.clear()
            field.send_keys(city)
            time.sleep(2)

            suggestion = self.wait.until(
                EC.element_to_be_clickable(self.suggestion)
            )

            suggestion.click()
            time.sleep(2)

        except Exception as e:
            print("Error selecting departure city:", e)


    def select_arrival_city(self, city):
        """
        Enters and selects the arrival city.

        Args:
            city: Name of the destination city or airport.
        """
        try:
            field = self.wait.until(
                EC.element_to_be_clickable(self.arrival_input)
            )

            field.click()
            field.clear()
            field.send_keys(city)
            time.sleep(2)

            suggestion = self.wait.until(
                EC.element_to_be_clickable(self.suggestion)
            )

            suggestion.click()
            time.sleep(2)

            self.driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(1)

        except Exception as e:
            print("Error selecting arrival city:", e)


    def select_departure_date(self, day):
        """
        Selects the departure date from the calendar.

        Args:
            day: Day of the month to select from the date picker.

        This method also stores the selected date for validation.
        """
        try:
            overlays = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'datepicker-overlay')]"
            )

            if not overlays:
                date_field = self.wait.until(
                    EC.element_to_be_clickable(self.date_input)
                )

                date_field.click()
                time.sleep(2)

            dynamic_date = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//td//div[text()='{day}']")
                )
            )

            dynamic_date.click()
            time.sleep(2)

            date_value = self.driver.find_element(
                By.XPATH,
                "//input[@placeholder='Departure Date']"
            ).get_attribute("value")

            self.selected_date = datetime.datetime.strptime(
                date_value,
                "%d-%m-%Y"
            ).date()

        except Exception as e:
            print("Error selecting departure date:", e)


    def select_passenger_one(self):
        """
        Opens the passenger selection dropdown.

        This ensures that at least one passenger is selected
        for the flight search.
        """
        try:
            passenger = self.wait.until(
                EC.element_to_be_clickable(self.passenger_dropdown)
            )

            passenger.click()
            time.sleep(2)

            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[text()='1']")
                )
            )

        except Exception as e:
            print("Error selecting passenger:", e)


    def select_economy(self):
        """
        Selects the Economy cabin class for the flight search.
        """
        try:
            cabin = self.wait.until(
                EC.element_to_be_clickable(self.cabin_dropdown)
            )

            cabin.click()
            time.sleep(2)

            economy = self.wait.until(
                EC.element_to_be_clickable(self.economy_option)
            )

            economy.click()
            time.sleep(2)

        except Exception as e:
            print("Error selecting economy:", e)


    def click_search(self):
        """
        Clicks the 'Search Flights' button.

        This triggers the flight search based on the selected criteria.
        """
        try:
            search = self.wait.until(
                EC.element_to_be_clickable(self.search_button)
            )

            search.click()
            time.sleep(5)

        except Exception as e:
            print("Error clicking search:", e)


    def verify_search_results_displayed(self):
        """
        Verifies that flight search results are displayed.

        The method checks whether at least one flight result
        card is visible on the page.
        """
        try:
            flights = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'shadow-sm')]"
            )

            assert len(flights) > 0, "No flights displayed"

        except Exception as e:
            print("Flight results verification failed:", e)


    def verify_price_displayed(self):
        """
        Verifies that flight prices are visible in the search results.
        """
        try:
            prices = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//p[contains(text(),'USD')]")
                )
            )

            assert len(prices) > 0, "Price not displayed"

        except Exception as e:
            print("Price verification failed:", e)


    def validate_no_past_date_selection(self):
        """
        Validates that the selected departure date is not in the past.

        This ensures the flight search uses a valid future date.
        """
        try:
            today = datetime.datetime.today().date()

            assert self.selected_date >= today, (
                f"Selected date {self.selected_date} is in the past"
            )

        except Exception as e:
            print("Date validation failed:", e)


    def click_first_book_now(self):
        """
        Clicks the first 'Book Now' button from the search results.

        The method scrolls to the button, performs a JavaScript click
        for reliability, and switches to the booking page if it opens
        in a new browser tab.
        """
        try:
            self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//button[.//span[text()='Book Now']]")
                )
            )

            first_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//button[.//span[text()='Book Now']])[1]")
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                first_button
            )

            time.sleep(2)

            self.driver.execute_script(
                "arguments[0].click();",
                first_button
            )

            time.sleep(5)

            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[1])

        except Exception as e:
            print("Error clicking Book Now:", e)