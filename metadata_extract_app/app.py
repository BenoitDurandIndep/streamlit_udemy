# launch with streamlit run metadata_extract_app/app.py
import os
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
from PIL import Image
import exifread  # For images
import seaborn as sns
from PyPDF2 import PdfReader  # For PDF
import mutagen  # For audio
from datetime import datetime as dt
import base64
import sqlite3

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

st.set_page_config(layout="wide")

# HTML
metadata_wiki = """Metadata is defined as the data providing information about one or more aspects of the data"""
HTML_BANNER = """
    <div style="background-color:#464E5F;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">MetaData Extractor App</h1>
    </div>
"""


# Functions
@st.cache_resource
def load_image(image_file):
    img = Image.open(image_file)
    return img


# Function to get human readable time
def get_readable_time(mytime):
    return dt.fromtimestamp(mytime).strftime("%Y-%m-%d %H:%M")


# Function to download
def make_download(data: pd.DataFrame):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()
    st.markdown("### ** Download CSV File **")
    mydate_str = dt.now().strftime("%Y-%m-%d %H:%M")
    filename = f"metadata_result_{mydate_str}.csv"
    href = f"<a href='data:file/csv;base64,{b64}' download='{filename}'>Click here</a>"
    st.markdown(href, unsafe_allow_html=True)


# Database Management
conn = sqlite3.connect("data.db")
c = conn.cursor()


def create_uploaded_filetable():
    req = "CREATE TABLE IF NOT EXISTS filesstable(filename TEXT, filetype TEXT, filesize TEXT,uploadeddate TIMESTAMP)"
    c.execute(req)


def add_file_details(filename, filetype, filesize, uploadeddate):
    req = "INSERT INTO filesstable(filename,filetype,filesize,uploadeddate) VALUES (?,?,?,?)"
    c.execute(req, (filename, filetype, filesize, uploadeddate))
    conn.commit()


def view_all_data():
    req = "SELECT * FROM filesstable"
    c.execute(req)
    data = c.fetchall()
    return data


# App Structure
def main():
    # st.title("Metadata Extraction App")
    stc.html(HTML_BANNER)

    menu = ["Home", "Image", "Audio", "DocumentFiles", "Analytics", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_uploaded_filetable()

    if choice == "Home":
        st.subheader("Home")
        st.image(load_image("metadata_extract_app/images/upload.jpg"))
        st.write(metadata_wiki)
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.expander("Get Image Metadata"):
                st.info(
                    "Image Metadata"
                )  # https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
                st.markdown(":frame_with_picture:")
                st.text("Upload jpeg, jpg, png images")
        with col2:
            with st.expander("Get Audio Metadata"):
                st.info("Audio Metadata")
                st.markdown(":loud_sound:")
                st.text("Upload mp3, ogg")
        with col3:
            with st.expander("Get Documents Metadata"):
                st.info("Documents Metadata")
                st.markdown(":page_facing_up:")
                st.text("Upload pdf,docx")
    elif choice == "Image":
        st.subheader("Image MetaData Extraction")
        image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        if image_file is not None:
            statinfo = os.stat(image_file.readable())

            file_details_combined = {
                "FileName": image_file.name,
                "FileSize": image_file.size,
                "FileType": image_file.type,
                "Accessed_Time": get_readable_time(statinfo.st_atime),
                "Creation_Time": get_readable_time(statinfo.st_ctime),
                "Modified_Time": get_readable_time(statinfo.st_mtime),
            }
            df_file_details = pd.DataFrame(
                list(file_details_combined.items()), columns=["Meta Tags", "Value"]
            )

            with st.expander("File Stats"):
                st.dataframe(df_file_details.astype(str))

            add_file_details(
                image_file.name, image_file.type, image_file.size, dt.now()
            )

            c1, c2, c3 = st.columns(3)
            with c1:
                with st.expander("View Image"):
                    img = load_image(image_file=image_file)
                    st.image(img, width=250)

            with c2:
                with st.expander("Default JPEG"):
                    st.info("Using PILLOW")
                    img = load_image(image_file=image_file)
                    img_details = {
                        "format": img.format,
                        "format_desc": img.format_description,
                        "size": img.size,
                        "height": img.height,
                        "width": img.width,
                        "info": img.info,
                    }

                    df_img_details_def = pd.DataFrame(
                        list(img_details.items()), columns=["Meta Tags", "Value"]
                    )
                    st.dataframe(df_img_details_def.astype(str))

            with c3:
                with st.expander("Exifread tool"):
                    meta_tags = exifread.process_file(image_file)
                    df_meta_tags_exi = pd.DataFrame(
                        list(meta_tags.items()), columns=["Meta Tags", "Value"]
                    )
                    st.dataframe(df_meta_tags_exi.astype(str))

            with st.expander("Download results"):
                final_df = pd.concat(
                    [df_file_details, df_img_details_def, df_meta_tags_exi]
                )
                st.dataframe(final_df.astype(str))
                make_download(final_df)

    elif choice == "Audio":
        st.subheader("Audio MetaData Extraction")
        # File Upload
        audio_file = st.file_uploader("Upload audio", type=["mp3", "ogg"])

        if audio_file is not None:
            col1, col2 = st.columns(2)

            with col1:
                st.audio(audio_file.read())

            with col2:
                statinfo = os.stat(audio_file.readable())

                file_details_combined = {
                    "FileName": audio_file.name,
                    "FileSize": audio_file.size,
                    "FileType": audio_file.type,
                    "Accessed_Time": get_readable_time(statinfo.st_atime),
                    "Creation_Time": get_readable_time(statinfo.st_ctime),
                    "Modified_Time": get_readable_time(statinfo.st_mtime),
                }
                df_file_details = pd.DataFrame(
                    list(file_details_combined.items()), columns=["Meta Tags", "Value"]
                )

                with st.expander("File Stats"):
                    st.dataframe(df_file_details.astype(str))

            add_file_details(
                audio_file.name, audio_file.type, audio_file.size, dt.now()
            )

            with st.expander("Metadata with Mutagen"):
                meta_tags = mutagen.File(audio_file)
                df_audio_details = pd.DataFrame(
                    list(meta_tags.items()), columns=["Meta Tags", "Value"]
                )
                st.dataframe(df_audio_details.astype(str))

            with st.expander("Download results"):
                final_df = pd.concat([df_file_details, df_audio_details])
                st.dataframe(final_df.astype(str))
                make_download(final_df)

    elif choice == "DocumentFiles":
        st.subheader("DocumentFiles MetaData Extraction")

        text_file = st.file_uploader("Upload File", type=["PDF"])

        if text_file is not None:
            dcol1, dcol2 = st.columns(2)

            statinfo = os.stat(text_file.readable())

            file_details_combined = {
                "FileName": text_file.name,
                "FileSize": text_file.size,
                "FileType": text_file.type,
                "Accessed_Time": get_readable_time(statinfo.st_atime),
                "Creation_Time": get_readable_time(statinfo.st_ctime),
                "Modified_Time": get_readable_time(statinfo.st_mtime),
            }
            df_file_details = pd.DataFrame(
                list(file_details_combined.items()), columns=["Meta Tags", "Value"]
            )

            add_file_details(text_file.name, text_file.type, text_file.size, dt.now())

            with dcol1:
                with st.expander("File Stats"):
                    st.dataframe(df_file_details.astype(str))

            with dcol2:
                with st.expander("MetaData"):
                    pdf_file = PdfReader(text_file)
                    pdf_info = pdf_file.metadata
                    df_pdf_details = pd.DataFrame(
                        list(pdf_info.items()), columns=["Meta Tags", "Value"]
                    )
                    st.dataframe(df_pdf_details.astype(str))

            with st.expander("Download results"):
                final_df = pd.concat([df_file_details, df_pdf_details])
                st.dataframe(final_df.astype(str))
                make_download(final_df)

    elif choice == "Analytics":
        st.subheader("Analytics")
        all_uplooaded_files = view_all_data()

        df = pd.DataFrame(
            all_uplooaded_files,
            columns=["Filename", "FileType", "FileSize", "UploadedDate"],
        )

        with st.expander("Monitor"):
            st.success("View all uploaded files")
            st.dataframe(df.astype(str))

        with st.expander("Distribution of types"):
            fig = plt.figure()
            sns.countplot(x=df["FileType"])
            st.pyplot(fig)

    else:
        st.subheader("About")


if __name__ == "__main__":
    main()
