import numpy as np
import pandas as pd
import streamlit as st
import s3fs
import csv

fs = s3fs.S3FileSystem(anon=False, 
                       key=st.secrets["AWS_ACCESS_KEY_ID"], 
                       secret=st.secrets["AWS_SECRET_ACCESS_KEY"])


#for bucket in s3.buckets.all():
#    st.write(bucket.name)



@st.cache(allow_output_mutation=True)
def load_table(filename):
    try:
        return pd.read_csv(filename)
    except Exception:
        print('Error reading: ' + filename)
    return 0

def load_table_no_cache(filename):
    try:
        return pd.read_csv(filename)
    except Exception:
        print('Error reading: ' + filename)
    return 0

def save_table(filename, table):
    try:
        table.to_csv(filename, index=False)
    except Exception:
        print('Error writing: ' + filename)
    return 0

def reset_all_people_directory(DATA_PATH, filename):
    df_people = load_table(DATA_PATH, 'all_people_directory.csv')
    drop_columns = ["Checked In", "Printed"]
    for column in drop_columns:
        try:
            df_people = df_people.drop(columns = [column])
        except:
            print("Can't drop " + column)

    df_people["Checked In"] = pd.to_datetime("01/01/1970 12:00:00 PM", format="%d/%m/%Y %I:%M:%S %p")
    df_people["Printed"] = 0
    save_table(DATA_PATH, df_people, filename)

def check_AWS(s3):
    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)
    # Print out object names
    for obj in s3.Bucket('hope-bucket').objects.all():
        print(obj)
