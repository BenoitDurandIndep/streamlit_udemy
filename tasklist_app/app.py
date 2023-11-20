# launch with streamlit run tasklist_app/app.py

import streamlit as st
from post_page import run_task_page
from manage_page import run_analytics_page
from home_page import run_home_page

def main():
    st.title("Simple Tasklist App")

    menu=["Home", "Task","Manage","About"]
    choice =st.sidebar.selectbox("Menu",menu)

    if choice=="Home":
        run_home_page()

    elif choice=="Task":
        run_task_page()

    elif choice=="Manage":
        run_analytics_page()

    else:
        st.subheader("About")



if __name__=='__main__'    :
    main()