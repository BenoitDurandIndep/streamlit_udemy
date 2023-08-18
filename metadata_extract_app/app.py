#launch with streamlit run metadata_extract_app/app.py
import os
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
from PIL import Image
import exifread # For images
import seaborn as sns
from PyPDF2 import PdfReader # For PDF
import mutagen # For audio

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

# HTML
metadata_wiki="""Metadata is defined as the data providing information about one or more aspects of the data"""
HTML_BANNER="""
    <div style="background-color:#464E5F;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">MetaData Extractor App</h1>
    </div>
"""

#App Structure
def main():
    # st.title("Metadata Extraction App")
    stc.html(HTML_BANNER)

    menu = ["Home","Image","Audio","DocumentFiles","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice=="Home":
        st.subheader("Home")
    elif choice=="Image":
        st.subheader("Image MetaData Extraction")
    elif choice=="Audio":
        st.subheader("Audio MetaData Extraction")
    elif choice=="DocumentFiles":
        st.subheader("Document MetaData Extraction")
    else:
        st.subheader("About")

if __name__ == '__main__':
    main()

