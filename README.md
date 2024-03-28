# Bizcard-Project


# Business Card Extraction using Streamlit, Sqlite3, Pandas, and NumPy, Opencv

## Overview
This project is a simple application built with Streamlit for extracting information from business cards. It utilizes SQL for storing extracted data, and Pandas and NumPy for data manipulation and analysis.


## Features

- **Streamlit Interface:** Interactive web application built using Streamlit for easy usability.
- **Business Card Extraction:** Extracts relevant information such as name, phone number, email, etc., from uploaded business card images.
- **SQL Database Integration:** Stores extracted data in a SQL database for future reference and analysis.
- **Data Manipulation with Pandas and NumPy:** Utilizes Pandas and NumPy for data manipulation and analysis tasks.

## Installation
1. install the  required packages:
   
2. import pandas as pd
    import numpy as np
    import streamlit as st
    from streamlit_option_menu import option_menu
    import easyocr
    from PIL import Image
    import os
    import re
    import io
    import sqlite3

 

## Usage
1. Start the Streamlit application:
    ```
    streamlit run app.py
    ```
2. Upload a business card image using the provided interface.
3. The application will extract relevant information from the image and display it.
4. Extracted data will be stored in the SQL database for future reference.
5. if anything need to change the data we can edit and modify the data's.
6. if need to delete the details it also be done.

## Dependencies
- Streamlit
- Sqlite3
- OpenCV
- Pandas
- NumPy

## Contributing
Contributions are welcome! Please feel free to open an issue or submit a pull request.





