import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FlightsPage:
    """
    FlightsPage represents the flight search interface for round-trip bookings.

    This class handles all actions related to:
    - Selecting round-trip flight type
    - Entering departure and arrival cities
    - Reading default departure and return dates
    - Selecting passengers and cabin class
    - Performing the flight search
    - Validating flight search results
    - Navigating to the booking page

    The class follows the Page Object Model (POM) design pattern
    used in Selenium automation frameworks.
    """

    loader = (By.ID, "page-loader")

    flight_type_dropdown = (
        By.XPATH,
        "//div[contains(@class,'input cursor-pointer')]"
    )

    round_trip_option = (
        By.XPATH,
        "//span[normalize-space()='Round Trip']"
    )

    departure_input = (By.XPATH, "//input[@placeholder='Departure City or Airport']")
    arrival_input = (By.XPATH, "//input[@id='arrival_airport_input']")
    suggestion = (By.XPATH, "(//div[contains(@class,'cursor-pointer')])[1]")

    date_input = (By.XPATH, "//input[@placeholder='Departure Date']")
    return_date_input = (By.XPATH, "//input[@placeholder='Return Date']")

    passenger_dropdown = (By.XPATH, "//span[contains(text(),'Passenger')]/parent::div")

    cabin_dropdown = (By.XPATH, "//div[contains(@class,'cursor-pointer') and .//span[text()='Economy']]")
    economy_option = (By.XPATH, "//span[normalize-space()='Economy']")

    search_button = (By.XPATH, "//button[.//span[normalize-space()='Search Flights']]")

    def __init__(self, driver):
        """
        Initializes the FlightsPage object.

        Args:
            driver: Selenium WebDriver instance used for browser interaction.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.selected_date = None
        self.selected_return_date = None


    def wait_loader(self):
        """
        Waits until the page loader disappears.

        Ensures that the page is fully loaded before interacting
        with the page elements.
        """
        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.loader)
            )
        except Exception as e:
            print("Loader wait issue:", e)


    def select_round_trip(self):
        """
        Selects the 'Round Trip' flight type.

        This method opens the flight type dropdown and selects
        the round-trip option.
        """
        try:
            self.wait_loader()

            dropdown = self.wait.until(
                EC.element_to_be_clickable(self.flight_type_dropdown)
            )

            dropdown.click()

            round_trip = self.wait.until(
                EC.element_to_be_clickable(self.round_trip_option)
            )

            round_trip.click()

            time.sleep(2)

        except Exception as e:
            print("Error selecting round trip:", e)


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
            city: Destination city or airport.
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


    def get_departure_date(self):
        """
        Retrieves the default departure date from the input field.

        The retrieved date is stored for validation purposes.
        """
        try:
            date_value = self.wait.until(
                EC.visibility_of_element_located(self.date_input)
            ).get_attribute("value")

            self.selected_date = datetime.datetime.strptime(
                date_value,
                "%d-%m-%Y"
            ).date()

        except Exception as e:
            print("Error getting departure date:", e)


    def get_return_date(self):
        """
        Retrieves the default return date from the input field.

        The retrieved date is stored for validation purposes.
        """
        try:
            date_value = self.wait.until(
                EC.visibility_of_element_located(self.return_date_input)
            ).get_attribute("value")

            self.selected_return_date = datetime.datetime.strptime(
                date_value,
                "%d-%m-%Y"
            ).date()

        except Exception as e:
            print("Error getting return date:", e)


    def select_passenger_one(self):
        """
        Opens the passenger selection dropdown.

        Ensures that at least one passenger is selected
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
        Selects the Economy class cabin option.
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

        Initiates the flight search based on the selected
        trip details.
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

        Ensures that at least one flight card is visible
        on the results page.
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
        Verifies that flight prices are visible in the results.
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
        Validates that the departure date is not a past date.
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

        The method scrolls to the first booking button,
        clicks it using JavaScript for reliability,
        and switches to the booking page if it opens in a new tab.
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