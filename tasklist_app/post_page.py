import streamlit as st
import pandas as pd
from datetime import datetime as dt
from db_fct import create_table,add_data,view_all_tasks,view_all_tasks_names,get_task_by_name,edit_task_data

LIST_STATUS=["Todo","Doing","Done","Uncertain"]
ADD_TASK="Add Task"
EDIT_TASK="Edit Task"

def run_task_page():
    st.subheader("Post and update Tasks")

    create_table()

    submenu=st.sidebar.selectbox("SubMenu",[ADD_TASK,EDIT_TASK])

    if submenu==ADD_TASK:
        st.subheader(ADD_TASK)
        col1,col2=st.columns(2)
        
        with col1:
            task_doer=st.text_input("Task Doer")
            task_name=st.text_area("Task")

        with col2:
            task_status = st.selectbox("Status",LIST_STATUS)
            task_due_date=st.date_input("Task Due Date")

        if st.button(ADD_TASK):
            add_data(task_doer=task_doer,task_name=task_name,task_status=task_status,task_due_date=task_due_date)
            st.success(f"Added: {task_name}")

        res=view_all_tasks()
        st.write(res)

    elif submenu == EDIT_TASK:
        st.subheader("Update/Edit Task")
        list_tasks = [i[0] for i in view_all_tasks_names()]
        selected_task=st.selectbox("Task",list_tasks)
        task_res=get_task_by_name(selected_task)

        if task_res:
            task_doer= task_res[0][0]
            task_name= task_res[0][1]
            task_status= task_res[0][2]
            task_due_date= dt.strptime(task_res[0][3],"%Y-%m-%d")

            col1,col2=st.columns(2)
            
            with col1:
                new_task_doer=st.text_input("Task Doer",task_doer)
                new_task_name=st.text_area("Task",task_name)

            with col2:
                new_task_status = st.selectbox("Status",LIST_STATUS,index=int(pd.Index(LIST_STATUS).get_indexer([task_status])[0]))
                new_task_due_date=st.date_input("Task Due Date",value=task_due_date)

            if st.button("Update Task"):
                edit_task_data(new_task_doer,new_task_name,new_task_status,new_task_due_date,task_doer,task_name,task_status)
                st.success(f"Updated: {new_task_name}")

            res=view_all_tasks()
            st.write(res)