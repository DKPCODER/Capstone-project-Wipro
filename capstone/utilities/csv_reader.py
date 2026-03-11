import csv
import os


def read_csv_data():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path = os.path.join(base_dir, "data", "guest_data.csv")

    data = []

    with open(path, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            data.append(row)

    return data