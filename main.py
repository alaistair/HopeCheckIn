import numpy as np
import pandas as pd
import streamlit as st
import os
import src
from datetime import datetime
from pandas.util import hash_pandas_object
from PIL import Image
from streamlit_autorefresh import st_autorefresh

import boto3
s3 = boto3.resource(
    service_name='s3',
    region_name=st.secrets["AWS_DEFAULT_REGION"],
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

def main():
    PATH = str(os.path.realpath('..')) + '/HopeCheckIn/'
    DATA_PATH = PATH + 'data/'
    df_people = src.load_table_no_cache("s3://hope-bucket/all_people_directory.csv")

    st.set_page_config(page_title="Hope Anglican Check in", layout="centered")

    # Remove hamburger menu
    st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    left_padding, logo, right_padding = st.columns(3)
    image = Image.open("data/Hope-Logo-White.png")
    left_padding.write("")
    logo.image(image)
    right_padding.write("")

    check_in_label = st.empty()
    check_in_label.write("### Check in")

    lastname_input = st.empty()
    lastname = lastname_input.text_input("Please enter your surname to check in", "", key = "lastname_input")

    family_container_list = []
    families, family_container_list = src.write_families(df_people, lastname, family_container_list)

    if families and st.button('Finished checking in'):
        check_in_label.write(" ")
        lastname_input.write("## Welcome to Hope!")
        lastname = ""
        
        for family_container in family_container_list:
            # family_container_list: [[family_text, [family1_checkbox]], [family_text, [family2_checkbox]], ...]
            # family1_container: ["People in this family", [person1_container], [person2_container], ...]
            # person1_container: ["Person name", person1_checkbox]
            for person_container in family_container:
                for content in person_container:
                    content.write(" ")



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
            #st.write(df_new)
            df_people = df_people.append(df_new)
        #done = st.button("Done")

    src.save_table("s3://hope-bucket/all_people_directory.csv", df_people)

if __name__ == '__main__':
    main()
