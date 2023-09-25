import streamlit as st
import pandas as pd



def run_eda_app():
    st.subheader("From Exploratory Data Analysis")
    df=pd.read_csv("diabete_predict_app/data/diabetes_data_upload.csv")
    st.dataframe(df)