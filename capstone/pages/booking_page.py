import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class BookingPage:
    """
    BookingPage represents the flight booking form page.

    This class handles all actions related to the booking process such as:
    - Selecting guest booking
    - Filling guest personal details
    - Entering passenger information
    - Accepting terms and conditions
    - Confirming the booking

    The class follows the Page Object Model (POM) design pattern.
    """

    guest_booking = (By.XPATH, "//div[contains(.,'Guest Booking')]")
    title_dropdown = (By.XPATH, "//select[@x-model='primary_guest.title']")

    first_name = (By.XPATH, "//input[@placeholder='Enter First Name']")
    last_name = (By.XPATH, "//input[@placeholder='Enter Last Name']")
    email = (By.XPATH, "//input[@x-model='primary_guest.email']")
    phone = (By.XPATH, "//input[@placeholder='Enter Phone Number']")

    passport = (By.XPATH, "//input[@placeholder='6 - 15 Numbers']")

    nationality_dropdown = (
        By.XPATH,
        "//select[@x-model='formData.passengers.adult_0.nationality']"
    )

    terms_checkbox = (By.ID, "terms_accepted")

    confirm_booking = (By.XPATH, "//button[contains(.,'Confirm Booking')]")

    def __init__(self, driver):
        """
        Initializes the BookingPage object.

        Args:
            driver: Selenium WebDriver instance used to interact with the browser.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)


    def select_guest_booking(self):
        """
        Selects the 'Guest Booking' option.

        This method scrolls to the guest booking element and clicks it
        to allow the user to proceed without logging into an account.
        """

        try:
            guest = self.wait.until(
                EC.element_to_be_clickable(self.guest_booking)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", guest
            )

            time.sleep(2)
            guest.click()
            time.sleep(3)

        except Exception as e:
            print("Error selecting guest booking:", e)


    def fill_guest_details(self, title, first, last, email, phone):
        """
        Fills the primary guest personal information.

        Args:
            title: Guest title (Mr, Mrs, etc.)
            first: First name of the guest
            last: Last name of the guest
            email: Email address of the guest
            phone: Contact phone number
        """

        try:
            title_el = self.wait.until(
                EC.visibility_of_element_located(self.title_dropdown)
            )

            Select(title_el).select_by_visible_text(title)

            self.wait.until(
                EC.visibility_of_element_located(self.first_name)
            ).send_keys(first)

            self.wait.until(
                EC.visibility_of_element_located(self.last_name)
            ).send_keys(last)

            self.wait.until(
                EC.visibility_of_element_located(self.email)
            ).send_keys(email)

            self.wait.until(
                EC.visibility_of_element_located(self.phone)
            ).send_keys(phone)

        except Exception as e:
            print("Error filling guest details:", e)


    def fill_passenger_details(self, nationality, passport):
        """
        Fills passenger-specific travel details.

        Args:
            nationality: Passenger nationality
            passport: Passport number of the passenger
        """

        try:
            nationality_el = self.wait.until(
                EC.visibility_of_element_located(self.nationality_dropdown)
            )

            Select(nationality_el).select_by_visible_text(nationality)

            passport_el = self.wait.until(
                EC.visibility_of_element_located(self.passport)
            )

            passport_el.send_keys(passport)

            time.sleep(2)

        except Exception as e:
            print("Error filling passenger details:", e)


    def accept_terms(self):
        """
        Accepts the terms and conditions checkbox.

        This step is mandatory before confirming the booking.
        The method ensures the checkbox is selected before proceeding.
        """

        try:
            checkbox = self.wait.until(
                EC.presence_of_element_located(self.terms_checkbox)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", checkbox
            )

            time.sleep(2)

            if not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)

        except Exception as e:
            print("Error accepting terms:", e)


    def confirm_booking_click(self):
        """
        Clicks the 'Confirm Booking' button.

        This method scrolls to the confirmation button and triggers
        the final booking action.
        """

        try:
            button = self.wait.until(
                EC.element_to_be_clickable(self.confirm_booking)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", button
            )

            time.sleep(2)
            button.click()
            time.sleep(5)

        except Exception as e:
            print("Error confirming booking:", e)