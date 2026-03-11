import os
import time
from datetime import datetime
import os


def capture_screenshot(driver, test_name):
    time.sleep(2)
    project_root = os.path.dirname(os.path.dirname(__file__))
    screenshot_folder = os.path.join(project_root, "screenshots")

    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"{test_name}_{timestamp}.png"

    file_path = os.path.join(screenshot_folder, file_name)

    driver.get_screenshot_as_file(file_path)

    return file_path