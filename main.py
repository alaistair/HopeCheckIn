import numpy as np
import pandas as pd
import streamlit as st
import os
import src
from datetime import datetime
from pandas.util import hash_pandas_object


import boto3
s3 = boto3.resource(
    service_name='s3',
    region_name=st.secrets["region_name"],
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)



def main():
    PATH = str(os.path.realpath('..')) + '/HopeCheckIn/'
    DATA_PATH = PATH + 'data/'
    st.set_page_config(layout="wide")
    st.title("Hope Check in")

    #df_people = src.load_table(DATA_PATH + 'all_people_directory.csv')
    s3 = boto3.client('s3')
    #obj = s3.get_object(Bucket="s3://hope-bucket/all_people_directory.csv", Key='key')


    df_people = src.load_table("s3://hope-bucket/all_people_directory.csv")
    st.write(df_people)
    #src.reset_all_people_directory(DATA_PATH, 'all_people_directory.csv')
    #st.stop()

    #st.write(df_people.astype(str))

    lastname = st.text_input("Please enter your last name", "", key = "lastname")
    families = src.search_families(df_people, lastname)
    st.write("--------")

    for family in families:
        left, _, right = st.columns(3)
        left.write("##### People in this family")
        right.button("This is my family", key=hash_pandas_object(family))

        #my_family = right.button("This is my family", key=family)
        src.display_family(family, df_people)
        st.write("--------")

    if 'newcomer' not in st.session_state:
        st.session_state.newcomer = 0
    if st.session_state.newcomer == 0:
        st.session_state.newcomer = st.button("New to Hope?")
    if st.session_state.newcomer:

        st.write("### Newcomer details")
        lastname = st.text_input("Last name", key = "newcomer_lastname")
        firstname = st.text_input("First name", key = "newcomer_firstname")

        phone = st.text_input("Phone", key = "newcomer_phone")
        save = st.button("Save")
        if save:
            df_new = pd.DataFrame({"Member ID": firstname+lastname,
                                   "First Name": firstname,
                                   "Last Name": lastname,
                                   "Mobile Number": phone,
                                   "Family Members": firstname,
                                   "Family Relationship": 'Primary',
                                   "Checked In": datetime.now(tz=None),
                                   "Printed": 0},
                                index=[0])
            st.write(df_new)
            df_people = df_people.append(df_new)
        done = st.button("Done")

    #src.save_table(DATA_PATH + "all_people_directory.csv", df_people)
    src.save_table("s3://hope-bucket/all_people_directory.csv", df_people)

if __name__ == '__main__':
    main()