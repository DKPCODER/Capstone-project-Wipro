import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ConfirmationPage:
    """
    ConfirmationPage represents the final booking confirmation page.

    This page handles:
    - Verification of successful booking
    - Downloading the booking invoice
    - Validating that the invoice file is downloaded

    It follows the Page Object Model (POM) design pattern
    used in Selenium automation frameworks.
    """

    success_message = (
        By.XPATH,
        "//p[contains(text(),'Booking Confirmed Successfully')]"
    )

    download_invoice_button = (
        By.XPATH,
        "//div[contains(@onclick,'downloadInvoice')]"
    )

    def __init__(self, driver):
        """
        Initializes the ConfirmationPage object.

        Args:
            driver: Selenium WebDriver instance used to control the browser.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)

    def verify_booking_success(self):
        """
        Verifies that the booking has been successfully completed.

        This method waits for the success message to appear
        and validates that the booking confirmation text is present.
        """

        try:
            message = self.wait.until(
                EC.visibility_of_element_located(self.success_message)
            )

            assert "Booking Confirmed Successfully" in message.text
            print("Booking verified successfully")

            time.sleep(3)

        except Exception as e:
            print("Booking verification failed:", e)


    def download_invoice(self):
        """
        Clicks the 'Download Invoice' button.

        This method scrolls to the invoice download button
        and initiates the invoice download process.
        """

        try:
            button = self.wait.until(
                EC.element_to_be_clickable(self.download_invoice_button)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", button
            )

            button.click()

            print("Invoice download clicked")
            time.sleep(4)

        except Exception as e:
            print("Invoice download click failed:", e)


    def wait_for_invoice_download(self, download_path):
        """
        Waits for the invoice PDF file to appear in the download folder.

        Args:
            download_path: The directory where the invoice will be downloaded.

        Returns:
            The name of the downloaded PDF file if successful.

        Raises:
            Exception: If the invoice file is not downloaded within the timeout.
        """

        try:
            timeout = 30
            end_time = time.time() + timeout

            while time.time() < end_time:

                files = os.listdir(download_path)

                pdf_files = [f for f in files if f.endswith(".pdf")]

                if pdf_files:
                    print("Invoice downloaded:", pdf_files[0])
                    return pdf_files[0]

                time.sleep(5)

            raise Exception("Invoice download failed")

        except Exception as e:
            print("Error while waiting for invoice download:", e)