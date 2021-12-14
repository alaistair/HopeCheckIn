import pandas as pd
import boto3, os
import src as helper
import streamlit as st

s3 = boto3.resource(
    service_name='s3',
    region_name='ap-southeast-2',
    aws_access_key_id=st.secrets[''],
    aws_secret_access_key=''
)

def create_labels(PATH, filename):
    # This script generates PNG images of all contacts in filename for printing.
    df_people = helper.load_table(PATH, filename)
    print(df_people)
    for index, row in df_people.iterrows():
        fullname = str(row['First Name']) + ' ' + str(row['Last Name'])
        print(str(index) + " " + fullname)
        helper.create_label(row['Member ID'], row['First Name'], PATH)
    helper.create_label('blank', "", PATH)

def main():
    # Check contents of AWS bucket
    #helper.check_AWS(s3)

    # Recreate all labels
    PATH = str(os.path.realpath('..')) + '/client-hope/data/'
    filename = 'all_people_directory_temp.csv'
    create_labels(PATH, filename)

if __name__ == '__main__':
    main()