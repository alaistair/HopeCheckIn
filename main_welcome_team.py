import numpy as np
import pandas as pd
from src.core import print_label
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import src
from datetime import datetime

def main():

    PATH = str(os.path.realpath('..')) + '/HopeCheckIn/'
    DATA_PATH = PATH + 'data/'
    st.set_page_config(layout="wide")
    st.title("Hope Anglican Welcome Team Print Station")

    # Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
    # after it's been refreshed 100 times.
    st_autorefresh(interval=2000, limit=1800, key="counter")    

    df_people = src.load_table_no_cache("s3://hope-bucket/all_people_directory.csv")
    df_checked_in = df_people[pd.to_datetime(df_people["Checked In"]) >= pd.to_datetime("01/01/2020 12:00:00 PM", format="%d/%m/%Y %I:%M:%S %p")]
    df_checked_in = df_checked_in.sort_values(by="Checked In")

    for index, row in df_checked_in.iterrows():
        left, centre, right = st.columns(3)
        left.write(row["Last Name"] + " " + row["First Name"])
        if centre.button("Print", key=row["Member ID"]+'print'):
            print_label(row["Member ID"])
            
            right.write("Printed")
    #src.save_table(DATA_PATH, df_people, "all_people_directory.csv")

if __name__ == '__main__':
    main()