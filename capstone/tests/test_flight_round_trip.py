from pages.flights_page_round_trip_search import FlightsPage
import os
import pytest

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
    Test Case: Round Trip Flight Booking

    This test automates the end-to-end workflow of booking a round trip flight.
    The test performs the following actions:
    1. Selects round trip option.
    2. Chooses departure and arrival cities.
    3. Selects departure and return dates.
    4. Selects passenger count and cabin class.
    5. Searches for available flights.
    6. Verifies search results and price visibility.
    7. Ensures no past dates are selected.
    8. Proceeds with booking the first available flight.
    9. Completes guest booking and passenger details.
    10. Accepts terms and confirms booking.
    11. Verifies booking success and downloads invoice.

    Parameters
    ----------
    driver : WebDriver
        Selenium WebDriver instance provided by pytest fixture.

    data : dict
        Test data containing departure and arrival cities
        loaded from Excel.
    """

    logger.info("Test started: Round Trip Flight Booking")

    flights = FlightsPage(driver)

    logger.info("Selecting round trip option")
    flights.select_round_trip()

    logger.info(f"Selecting departure city: {data['departure_city']}")
    flights.select_departure_city(data["departure_city"])

    logger.info(f"Selecting arrival city: {data['arrival_city']}")
    flights.select_arrival_city(data["arrival_city"])

    logger.info("Selecting departure date")
    flights.get_departure_date()

    logger.info("Selecting return date")
    flights.get_return_date()

    logger.info("Selecting passenger")
    flights.select_passenger_one()

    logger.info("Selecting cabin class Economy")
    flights.select_economy()

    logger.info("Clicking search flights")
    flights.click_search()

    logger.info("Verifying search results")
    flights.verify_search_results_displayed()

    logger.info("Verifying price displayed")
    flights.verify_price_displayed()

    logger.info("Validating no past date selected")
    flights.validate_no_past_date_selection()

    logger.info("Clicking first Book Now button")
    flights.click_first_book_now()

    booking = BookingPage(driver)

    logger.info("Selecting guest booking option")
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

    logger.info("Verifying booking success message")
    confirmation.verify_booking_success()

    logger.info("Downloading invoice")
    confirmation.download_invoice()

    download_folder = r"C:\Users\deepa\OneDrive\Desktop\Capstone\downloads"

    logger.info("Waiting for invoice download")
    confirmation.wait_for_invoice_download(download_folder)

    logger.info("Test completed successfully")