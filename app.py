"""
Created on Thur 04/01/2024

@author: Timme
"""

import numpy as np
import pandas as pd
import streamlit as st
import os
import shutil
from datetime import datetime

st.set_page_config(layout="wide")

st.markdown(" # Image Descriptor")
st.text("You can add descriptions to your images. \nThese  images can either be uploaded  or \ncaptured with your camera.")

col1,col2,col3 = st.columns([1,4,2.5])
selected_image_method = col1.selectbox("Select Image Method:", ["Upload Image", "Capture Image"])

if selected_image_method == "Upload Image":
    col2.markdown(" ## Upload an Image")
    image = col2.file_uploader('Upload Image',label_visibility='collapsed')
elif selected_image_method == "Capture Image":
    col2.markdown(" ## Capture Image")
    image = col2.camera_input('Capture Image',label_visibility='collapsed')

if not image:
    col3.markdown("**No image Found**")
else:
    # col1.clear()
    col3.markdown("**Image recieved succesfully**")
    col3.image(image)
    col2.markdown("## Describe the image")
    image_description = col2.text_input('Image Description')
    col3.text(image_description)

    if image_description:
        BASE_PATH = 'described_image'
        current_datetime = datetime.now()
        img_file_name = ('_'.join(image_description.split())[:15]+ '_' +
                         current_datetime.strftime("%y_%m_%d_%H_%M_%S")+
                         '.png')
        img_save_path = f'./{BASE_PATH}/images'
        os.makedirs(img_save_path, exist_ok=True)

        zip_filename_ = 'data'
        zip_filename = f'{zip_filename_}.zip'

        img_full_path = os.path.join(img_save_path,img_file_name)

        with open(img_full_path, 'wb') as f:
            f.write(image.read())
        
        pd.DataFrame({'image_filename':[img_file_name],'description':[image_description]}).to_csv(f'{BASE_PATH}/Descriptions.csv')

        shutil.make_archive(zip_filename_, 'zip', BASE_PATH)

        col3.download_button(
            label='Download your Descripted Image',
            data=open(zip_filename, 'rb').read(),
            key="download_button",
            file_name=zip_filename,
            )
