







import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import os
import re
import io
import sqlite3


def image_Text(path):

  input_img = Image.open(path)
  input_arr = np.array(input_img)

  reader = easyocr.Reader(['en'])
  text = reader.readtext(input_arr, detail = 0)

  return text, input_img



def extract_data(result):

      ext_data={'Name': [], 'Designation': [], 'Company name': [], 'Contact': [], 'Email': [], 'Website': [],
               'Address': [], 'Pincode': []}
      ext_data['Name'].append(result[0])
      ext_data['Designation'].append(result[1])

      for i in range(2, len(result)):
          if (result[i].startswith('+')) or (result[i].replace('-', '').isdigit() and '-' in result[i]):
              ext_data['Contact'].append(result[i])
          elif '@' in result[i] and '.com' in result[i]:
              small = result[i].lower()
              ext_data['Email'].append(small)
          elif 'www' in result[i] or 'WWW' in result[i] or 'wwW' in result[i]:
              small = result[i].lower()
              ext_data['Website'].append(small)
          elif 'TamilNadu' in result[i] or 'Tamil Nadu' in result[i] or result[i].isdigit():
              ext_data['Pincode'].append(result[i])
          elif re.match(r'^[A-Za-z]', result[i]):
              ext_data['Company name'].append(result[i])
          else:
            removed_colon = re.sub(r'[,;]', '', result[i])
            ext_data['Address'].append(removed_colon)

      for key, value in ext_data.items():
        if len(value) > 0:
            concatenated_string = ' '.join(value)
            ext_data[key] = [concatenated_string]
        else:
            value = 'NA'
            ext_data[key] = [value]
      return ext_data







#streamlit part

st.set_page_config(layout="wide")
st.title(":orange[BizCardX] :violet[Extracting Business Card Data with OCR]")

options = st.sidebar.radio(("Pick your option"),("HOME","Upload", "Modify", "Delete" ) )

if options == "HOME":

  st.write("-------------------")     
  st.caption("## :green[Domain] : Digital Buisness Card")
  st.caption("## :red[Technologies used] : OCR, Streamlit GUI, Sqlite3,Pandas,Numpy")
  st.caption("## :violet[Overview] : The purpose of the project is to automate the process of extracting data from the bizzcard The extracted information should be displayed in a clean and organized manner, and users should be able to easily add it to the database with the click of a button and Allow the user to Read the data,Update the data and Allow the user to delete the data through the streamlit UI")

   

elif options == "Upload":
    image=st.file_uploader(label="upload image",type=['png', 'jpg', 'jpeg'], label_visibility="hidden")

    if image is not None:
      st.image(image,width=350,caption="your image")

      text, input_img = image_Text(image)

      ext_text = extract_data(text)

      if ext_text:
        st.success("Extracted Successfully")

      df = pd.DataFrame(ext_text)

      #converting to bytes

      img_Bytes = io.BytesIO()
      input_img.save(img_Bytes, format = "PNG")


      img_data = img_Bytes.getvalue()

      data = {"IMAGE":[img_data]}

      df_1 = pd.DataFrame(data)

      concat_df = pd.concat([df,df_1], axis = 1)
      st.dataframe(concat_df)

      mydb = sqlite3.connect("bizcards.db")
      cursor = mydb.cursor()

      #Create_query

      create_query = '''CREATE TABLE IF NOT EXISTS Business_Card(NAME VARCHAR(50),
                                                                DESIGNATION VARCHAR(100),
                                                                COMPANY_NAME VARCHAR(100),
                                                                CONTACT VARCHAR(35),
                                                                EMAIL VARCHAR(100),
                                                                WEBSITE TEXT,
                                                                ADDRESS TEXT,
                                                                PINCODE VARCHAR(100),
                                                                IMAGE TEXT)'''

      cursor.execute(create_query)
      mydb.commit()

      #insert Query:

      A = '''INSERT INTO Business_Card(NAME, DESIGNATION, COMPANY_NAME, CONTACT, EMAIL, WEBSITE, ADDRESS,PINCODE, IMAGE)

                VALUES (?,?,?,?,?,?,?,?,?)'''

      for index, i in concat_df.iterrows():
          B = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7],i[8])
          cursor.execute(A, B)
          mydb.commit()

      st.success('SUCCESSFULLY UPLOADED', icon="✅")

elif options == "Modify":

  method = st.radio("select the method", ["None", "Preview", "Modify"])

  if method == "None":
    st.write("")

  elif method =="Preview":

    mydb = sqlite3.connect("bizcards.db")
    cursor = mydb.cursor()

    #select Query

    select_query = "Select * from Business_Card"

    cursor.execute(select_query)
    table= cursor.fetchall()
    mydb.commit()

    table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE","ADDRESS","PINCODE", "IMAGE"))
    st.dataframe(table_df)

  elif method == "Modify":



    mydb = sqlite3.connect("bizcards.db")
    cursor = mydb.cursor()

    #select Query

    select_query = "Select * from Business_Card"

    cursor.execute(select_query)
    table= cursor.fetchall()
    mydb.commit()

    table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE","ADDRESS","PINCODE", "IMAGE"))
    st.dataframe(table_df)

    col1,col2 = st.columns(2)

    with col1:

      select_name = st.selectbox("select the name", table_df['NAME'])

    df_3= table_df[table_df["NAME"]==select_name]


    df_4 = df_3.copy()

    col1, col2 = st.columns(2)
    with col1 :
      modified_n = st.text_input('NAME', df_3["NAME"].unique()[0])
      modified_d = st.text_input('DESIGNATION', df_3["DESIGNATION"].unique()[0])
      modified_c = st.text_input('COMPANY_NAME', df_3["COMPANY_NAME"].unique()[0])
      modified_con = st.text_input('CONTACT', df_3["CONTACT"].unique()[0])

      df_4["NAME"]= modified_n
      df_4["DESIGNATION"]= modified_d
      df_4["COMPANY_NAME"]= modified_c
      df_4["CONTACT"]= modified_con


    with col2:


      modified_m = st.text_input('EMAIL', df_3["EMAIL"].unique()[0])
      modified_w = st.text_input('WEBSITE', df_3["WEBSITE"].unique()[0])
      modified_a = st.text_input('ADDRESS', df_3["ADDRESS"].unique()[0])
      modified_p = st.text_input('PINCODE', df_3["PINCODE"].unique()[0])
      modified_q = st.text_input('IMAGE', df_3["IMAGE"].unique()[0])
      df_4["EMAIL"]= modified_m
      df_4["WEBSITE"]= modified_w
      df_4["ADDRESS"]= modified_a
      df_4["PINCODE"]= modified_p
      df_4["IMAGE"]= modified_q
    st.dataframe(df_4)

    button_3 = st.button("Modify")

    if button_3:

      mydb = sqlite3.connect("bizcards.db")
      cursor = mydb.cursor()

      cursor.execute(f"Delete from Business_Card where NAME = '{select_name}'")

      A = '''INSERT INTO Business_Card(NAME, DESIGNATION, COMPANY_NAME, CONTACT, EMAIL, WEBSITE, ADDRESS,PINCODE, IMAGE)

                VALUES (?,?,?,?,?,?,?,?,?)'''

      for index, i in df_4.iterrows():
          B = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7],i[8])
          cursor.execute(A, B)
          mydb.commit()

      st.success('SUCCESSFULLY MODIFIED', icon="✅")


elif options == "Delete":

  mydb = sqlite3.connect("bizcards.db")
  cursor = mydb.cursor()

  col1, col2 = st.columns(2)

  with col1:
    cursor.execute("SELECT NAME FROM Business_Card")
    Y = cursor.fetchall()
    mydb.commit()

    names = []

    for i in Y:
      names.append(i[0])

    name_selected = st.selectbox("Select the name to delete", names)
  with col2:
    cursor.execute(f"SELECT DESIGNATION FROM Business_Card WHERE NAME = '{name_selected}'")
    Z = cursor.fetchall()
    mydb.commit()
    designation = []
    for j in Z:
      designation.append(j[0])
      designation_selected = st.selectbox("Select the designation of the chosen name", designation)

    st.markdown(" ")
    col_a, col_b, col_c = st.columns([5, 3, 3])
    with col_b:
        remove = st.button("Clik here to delete")
    if name_selected and designation_selected and remove:
      cursor.execute(f"DELETE FROM Business_Card WHERE NAME = '{name_selected}' AND DESIGNATION = '{designation_selected}'")
      mydb.commit()
      if remove:
        st.warning('DELETED', icon="⚠️")


































