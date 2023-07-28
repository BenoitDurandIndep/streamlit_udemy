import os
import streamlit as st
import streamlit.components as stc
import pandas as pd
from PIL import Image
from PyPDF2 import PdfReader
import docx2txt
import  logging
import base64
import time

logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter=logging.Formatter("%(levelname)s %(asctime)s.%(msecs)03d - %(message)s")

file_handler = logging.FileHandler("activity.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class FileDownloader(object):
    """Class to download an object as a file 

    Args:
        object (_type_): the object to download

    Returns:
        _type_: a FileDownloader
    """

    def __init__(self,data,filename="myfile",fileext="txt") -> None:
        super(FileDownloader,self).__init__()
        self.data=data
        self.filename=filename
        self.fileext=fileext
        self.timestr=time.strftime("%Y%m%d-%H%M%S")

    def download(self):
        b64=base64.b64encode(self.data.encode()).decode()
        new_filename=f"{self.filename}_{self.timestr}.{self.fileext}"
        st.markdown("#### Dowlnload File ####")
        href=f"<a href='data:file/{self.fileext};base64,{b64}' download='{new_filename}'>Click here</a>"
        st.markdown(href,unsafe_allow_html=True)



@st.cache
def load_image(image_file):
    return Image.open(image_file)


def read_pdf(file):
    pdfReader = PdfReader(file)
    count = len(pdfReader.pages)
    all_page_text = ""
    for i in range(count):
        page = pdfReader.pages[i]
        all_page_text += page.extract_text()
    return all_page_text

def save_uploaded_file(uploadedfile):
    with open(os.path.join("tempdir",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("File saved")

def main():
    st.title("File Upload tutorial")

    menu = ["Home", "Dataset", "Documents","Download", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        logger.info("Home")

        image_file = st.file_uploader(
            "Upload Images", type=["png", "jpg", "jpeg"])
        if image_file is not None:
            file_details = {"filename": image_file.name,
                            "filetype": image_file.type, "filesize": image_file.size}
            st.write(file_details)
            st.image(load_image(image_file), width=250)

            save_uploaded_file(image_file)

    elif choice == "Dataset":
        st.subheader("Dataset")
        logger.info("Dataset")
        
        data_file = st.file_uploader("Upload csv", type=["csv"])
        if data_file is not None:
            file_details = {"filename": data_file.name,
                            "filetype": data_file.type, "filesize": data_file.size}
            st.write(file_details)
            df = pd.read_csv(data_file)
            st.dataframe(df)

            save_uploaded_file(data_file)

    elif choice == "Documents":
        st.subheader("Documents")
        logger.info("Documents")

        docx_file = st.file_uploader(
            "Upload document", type=["pdf", "docx", "txt"])
        if st.button("Process"):
            if docx_file is not None:
                file_details = {"filename": docx_file.name,
                                "filetype": docx_file.type, "filesize": docx_file.size}
                st.write(file_details)
                if docx_file.type == "text/plain":
                    raw_text = str(docx_file.read(), "utf-8")
                    st.text(raw_text)
                elif docx_file.type == "application/pdf":
                    raw_text = read_pdf(docx_file)
                    st.write(raw_text)
                else:
                    raw_text = docx2txt.process(docx_file)
                    st.write(raw_text)

            save_uploaded_file(docx_file)
    elif choice =="Download":
        st.subheader("Download text")
        logger.info("Download")


        my_text=st.text_area("Your message")
        if st.button("Save"):
            st.write(my_text)
            download=FileDownloader(my_text).download()


if __name__ == '__main__':
    main()
