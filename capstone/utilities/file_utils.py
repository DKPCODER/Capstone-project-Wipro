import os
import time

def verify_file_download(download_folder, file_extension=".pdf", timeout=30):

    end_time = time.time() + timeout

    while time.time() < end_time:

        files = os.listdir(download_folder)

        for file in files:
            if file.endswith(file_extension):
                print("Downloaded file:", file)
                return True

        time.sleep(1)

    raise Exception("File download failed")