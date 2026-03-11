import os
import pytest

from pages.flight_page_one_way import FlightsPage
from pages.booking_page import BookingPage
from pages.confirmation_page import ConfirmationPage
from utilities.excel_reader import read_excel_data
from utilities.csv_reader import read_csv_data
from utilities.logger import get_logger


logger = get_logger()

data = read_excel_data()
guest_data = read_csv_data()[0]


@pytest.mark.parametrize("data", data)
def test_departure_arrival_date(driver, data):
    """
    Test Case: One Way Flight Booking

    This test automates the end-to-end workflow of booking a one-way flight.
    The test performs the following steps:

    1. Selects the one-way flight option.
    2. Chooses departure and arrival cities using test data from Excel.
    3. Selects the departure date.
    4. Selects passenger count and cabin class (Economy).
    5. Searches for available flights.
    6. Verifies that search results and flight prices are displayed.
    7. Validates that the selected date is not in the past.
    8. Proceeds with booking the first available flight.
    9. Completes guest booking and passenger details using CSV data.
    10. Accepts terms and confirms the booking.
    11. Verifies booking confirmation and downloads the invoice.

    Parameters
    ----------
    driver : WebDriver
        Selenium WebDriver instance provided by pytest fixture.

    data : dict
        Test data containing departure city, arrival city,
        and departure day loaded from Excel.
    """

    logger.info("Test started: One Way Flight Booking")

    flights = FlightsPage(driver)

    logger.info("Selecting one way flight")
    flights.select_one_way()

    logger.info(f"Selecting departure city: {data['departure_city']}")
    flights.select_departure_city(data["departure_city"])

    logger.info(f"Selecting arrival city: {data['arrival_city']}")
    flights.select_arrival_city(data["arrival_city"])

    logger.info(f"Selecting departure date: {data['departure_day']}")
    flights.select_departure_date(data["departure_day"])

    logger.info("Selecting passenger count")
    flights.select_passenger_one()

    logger.info("Selecting cabin class Economy")
    flights.select_economy()

    logger.info("Clicking search flights")
    flights.click_search()

    logger.info("Verifying search results displayed")
    flights.verify_search_results_displayed()

    logger.info("Verifying price displayed")
    flights.verify_price_displayed()

    logger.info("Validating selected date is not in the past")
    flights.validate_no_past_date_selection()

    logger.info("Clicking first Book Now button")
    flights.click_first_book_now()

    booking = BookingPage(driver)

    logger.info("Selecting guest booking")
    booking.select_guest_booking()

    logger.info("Filling guest details")
    booking.fill_guest_details(
        guest_data["title"],
        guest_data["first_name"],
        guest_data["last_name"],
        guest_data["email"],
        guest_data["phone"]
    )

    logger.info("Filling passenger details")
    booking.fill_passenger_details(
        guest_data["nationality"],
        guest_data["passport"]
    )

    logger.info("Accepting terms and conditions")
    booking.accept_terms()

    logger.info("Confirming booking")
    booking.confirm_booking_click()

    confirmation = ConfirmationPage(driver)

    logger.info("Verifying booking success")
    confirmation.verify_booking_success()

    logger.info("Downloading invoice")
    confirmation.download_invoice()

    download_folder = os.path.join(os.getcwd(), "downloads")

    logger.info("Waiting for invoice to download")
    confirmation.wait_for_invoice_download(download_folder)

    logger.info("Test completed successfully")