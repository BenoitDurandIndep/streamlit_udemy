import streamlit as st
import pandas as pd
from PIL import Image
from PyPDF2 import PdfReader
#import pdfplumber
import docx2txt

def load_image(image_file):
    return Image.open(image_file)

def read_pdf(file):
    pdfReader=PdfReader(file)
    count=len(pdfReader.pages)
    all_page_text=""
    for i in range(count):
        page=pdfReader.pages[i]
        all_page_text+=page.extract_text()
    return all_page_text

def main():
    st.title("File Upload tutorial")

    menu = ["Home", "Dataset", "Documents", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        image_file = st.file_uploader(
            "Upload Images", type=["png", "jpg", "jpeg"])
        if image_file is not None:
            file_details = {"filename": image_file.name,
                            "filetype": image_file.type, "filesize": image_file.size}
            st.write(file_details)

            st.image(load_image(image_file), width=250)
    elif choice == "Dataset":
        st.subheader("Dataset")
        data_file = st.file_uploader("Upload csv", type=["csv"])
        if data_file is not None:
            file_details = {"filename": data_file.name,
                            "filetype": data_file.type, "filesize": data_file.size}
            st.write(file_details)
            df = pd.read_csv(data_file)
            st.dataframe(df)

    elif choice=="Documents":
        st.subheader("Documents")
        docx_file=st.file_uploader("Upload document",type=["pdf","docx","txt"])
        if st.button("Process"):
            if docx_file is not None:
                file_details = {"filename": docx_file.name,
                            "filetype": docx_file.type, "filesize": docx_file.size}
                st.write(file_details)
                if docx_file.type=="text/plain":
                    raw_text=str(docx_file.read(),"utf-8")
                    st.text(raw_text)
                elif docx_file.type=="application/pdf":
                    raw_text= read_pdf(docx_file)
                    st.write(raw_text)
                else:
                    raw_text=docx2txt.process(docx_file)
                    st.write(raw_text)




if __name__ == '__main__':
    main()
