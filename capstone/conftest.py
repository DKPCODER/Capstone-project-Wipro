import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions


from webdriver_manager.firefox import GeckoDriverManager

from utilities.logger import get_logger
from utilities.screenshot import capture_screenshot

logger = get_logger()

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")


@pytest.fixture
def driver():

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    chrome_options = Options()

    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-gpu")

    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }

    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    logger.info("Browser launched")

    driver.get("https://phptravels.net/flights")

    logger.info("Application opened")

    yield driver

    logger.info("Closing browser")
    driver.quit()



#
# firefox_options = FirefoxOptions()
#
# firefox_options.set_preference("browser.download.folderList", 2)
# firefox_options.set_preference("browser.download.dir", DOWNLOAD_DIR)
# firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
# firefox_options.set_preference("pdfjs.disabled", True)
#
# service = FirefoxService(GeckoDriverManager().install())
#
# driver = webdriver.Firefox(service=service, options=firefox_options)


def pytest_runtest_setup(item):
    logger.info(f"STARTING TEST: {item.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call":

        driver = item.funcargs.get("driver")

        if report.failed:

            if driver:
                path = capture_screenshot(driver, item.name)

                logger.error(f"TEST FAILED: {item.name}")
                logger.error(f"Screenshot saved: {path}")

        elif report.passed:

            logger.info(f"TEST PASSED: {item.name}")