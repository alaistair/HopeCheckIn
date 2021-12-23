import numpy as np
import pandas as pd
import streamlit as st
import os
from datetime import datetime

from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
from PIL import Image, ImageFont, ImageDraw

def search_families(df_people, lastname):
    """ Return a DataFrame of all families with 'lastname'.
    """
    # Get all people with lastname
    lastnames = df_people[df_people['Last Name'].str.lower() == lastname.lower()]
    # Get unique families
    unique_families = lastnames['Family Members'].drop_duplicates()
    return [
        df_people[df_people['Family Members'] == unique_family]
        for unique_family in unique_families
    ]

def display_family(family, df_people, family_container):
    """ For a given family, list each each member as well as check in box.
        When check in box clicked, record in df_people and show print button. 
        When print clicked, print label.
    """

    for person in family['First Name']:

        left, right = st.columns(2)
        with left:
            person_name = st.empty()
            person_name.write(person)
        member_id = family[family['First Name']==person]['Member ID']
        member_row = member_id.index[0]

        checked_in_already = pd.to_datetime(df_people.loc[member_row, "Checked In"]) >= pd.to_datetime("01/01/2020 12:00:00 PM", format="%d/%m/%Y %I:%M:%S %p")
        with right:
            person_checkbox = st.empty()
            if person_checkbox.checkbox('Check in', value=checked_in_already, key=person+'in'):
                df_people.at[member_row, 'Checked In'] = datetime.now(tz=None)
            else:
                df_people.at[member_row, 'Checked In'] = pd.to_datetime("01/01/1970 12:00:00 PM", format="%d/%m/%Y %I:%M:%S %p")

        person_container = [person_name, person_checkbox]
        family_container.append(person_container)

    return family_container

def write_families(df_people, lastname, family_container_list):
    families = search_families(df_people, lastname)
    for family in families:
        family_container = []
        family_container_list.append(family_container)

        left, _, right = st.columns(3)
        with left:
            family_text = st.empty()
            left.write("##### People in this family")

        #my_family = right.button("This is my family", key=hash_pandas_object(family))
        display_family(family, df_people, family_container)
        st.write("--------")

    return families, family_container_list


def add_newcomer(df_people):
    st.write("### Newcomer details")
    lastname = st.text_input("Last name", key = "newcomer_lastname")
    firstname = st.text_input("First name", key = "newcomer_firstname")

    phone = st.text_input("Phone", key = "newcomer_phone")
    save = st.button("Save")
    if save:
        df_new = pd.DataFrame({"First Name": firstname,
                               "Last Name": lastname,
                               "Checked In": phone},
                               index=[0])
        st.write(df_new)
        return df_people.append(df_new)
    else:
        return 0

def add_row(DATA_PATH, table, filename):
    TABLE_PATH = DATA_PATH + filename
    try:
        #with open(TABLE_PATH, 'a') as f:
         #   writer = csv.writer(f)
          #  writer.writerow(table)
        table.to_csv(TABLE_PATH, mode='a', header=False)
    except Exception:
        print('Error writing: ' + TABLE_PATH)
    return 0


def create_label(member_ID, name, PATH):
    # test: brother_ql print -l 29x90 temp.png
    dimensions = (991, 306) # to fit 29x90mm labels

    img = Image.new('RGB', dimensions, color = (255, 255, 255))
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 156)
    d = ImageDraw.Draw(img)
    d.text((80, 70), str(name), font=font, fill=(0, 0, 0))
    filename = PATH + '/name_images/' + member_ID + '.png'
    img.save(filename)

def print_label(member_id):
    """ For a given member_id, search for image and print."""

    PATH = str(os.path.realpath('..')) + '/HopeCheckIn/'
    DATA_PATH = PATH + 'data/name_images/'
    FILE_PATH = DATA_PATH + str(member_id) + '.png'
    try:
        im = Image.open(FILE_PATH)
        #backend = 'pyusb'
        backend = 'network'
        model = 'QL-810W'
        printer = 'tcp://192.168.20.19' #wifi enables
        #printer = 'usb://0x04f9:0x209c/000F1Z393514'

        qlr = BrotherQLRaster(model)
        qlr.exception_on_warning = True

        instructions = convert(
            qlr=qlr, 
            images=[im],    #  Takes a list of file names or PIL objects.
            label='29x90', 
            rotate='90',    # 'Auto', '0', '90', '270'
            threshold=70.0,    # Black and white threshold in percent.
            dither=False, 
            compress=False, 
            red=False,    # Only True if using Red/Black 62 mm label tape.
            dpi_600=False, 
            hq=True,    # False for low quality.
            cut=True
        )
        send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)
    except:
        raise ValueError('Print error for ' + FILE_PATH)

    

