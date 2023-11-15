import streamlit as st
import pandas as pd
from db_fct import view_all_tasks,view_all_tasks_names,delete_task

def run_analytics_page():
    submenu = ["Delete Task","Analytics"]
    choice=st.sidebar.selectbox("SubMenu",submenu)

    if choice == "Delete Task":
        res= view_all_tasks()
        df = pd.DataFrame(res,columns=['Task Doer','Task','Task Status', 'Task Due Date'])
        st.dataframe(df)
        unique_list = [i[0] for i in view_all_tasks_names()]
        delete_task_name = st.selectbox("Task to Delete",unique_list)
        if st.button("Delete"):
            delete_task(delete_task_name)
            st.warning(f"{delete_task_name} deleted")

        with st.expander("Current Database"):
            res = view_all_tasks()
            new_df=pd.DataFrame(res,columns=['Task Doer','Task','Task Status', 'Task Due Date'])
            st.dataframe(new_df)

    else:
        st.subheader("Analytics")