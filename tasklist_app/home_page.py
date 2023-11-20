import streamlit as st
import pandas as pd
from datetime import datetime as dt
from db_fct import view_all_tasks,view_all_tasks_names,get_task_by_name,get_task_by_doer

def run_home_page():
    st.subheader("Home Page")
    
    choice=st.sidebar.selectbox("SubMenu",["My Task","Search"])

    with st.expander("View all tasks"):
        res= view_all_tasks()
        df = pd.DataFrame(res,columns=['Task Doer','Task','Task Status', 'Task Due Date'])
        st.dataframe(df)

    if choice == "My Task":
        c1,c2 = st.columns([1,3])

        with c1:
            st.info("Task List")
            list_of_tasks = [i[0] for i in view_all_tasks_names()]
            selected_task = st.selectbox("Your Task",list_of_tasks)

        with c2:
            st.info("Details")
            task_res = get_task_by_name(selected_task)
            # st.write(task_res)
            task_doer = task_res[0][0]
            task_name = task_res[0][1]
            task_status= task_res[0][2]
            task_due_date= dt.strptime(task_res[0][3],"%Y-%m-%d")
            st.write(f"Task Doer : {task_doer}")
            st.text(f"Task : {task_name}")
            st.text(f"Task Status : {task_status}")
            st.write(f"Task Due Date : {task_due_date}")

    else:
        st.subheader("Search Task")
        search_term = st.text_input("Search Term")
        search_choice = st.radio("Field To Search",("Task Doer","Task Name"))
        if st.button("Search"):
            if search_choice=="Task Doer":
                search_result=get_task_by_doer(search_term,strict=False)
                st.write(search_result)
            else:
                search_result=get_task_by_name(search_term,strict=False)
                st.write(search_result)

