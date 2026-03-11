import pandas as pd
import os


def read_excel_data():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path = os.path.join(base_dir, "data", "flight_data_single_sample.xlsx")

    df = pd.read_excel(path)

    return df.to_dict(orient="records")