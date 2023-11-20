import streamlit as st
import pandas as pd
from db_fct import view_all_tasks,view_all_tasks_names,delete_task
import plotly.express as px

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

TASK_DOER="Task Doer"
TASK_NAME="Task"
TASK_STATUS="Task Status"
TASK_DUE_DATE="Task Due Date"

def run_analytics_page():
    submenu = ["Delete Task","Analytics"]
    choice=st.sidebar.selectbox("SubMenu",submenu)

    if choice == "Delete Task":
        res= view_all_tasks()
        df = pd.DataFrame(res,columns=[TASK_DOER,TASK_NAME,TASK_STATUS, TASK_DUE_DATE])
        st.dataframe(df)
        unique_list = [i[0] for i in view_all_tasks_names()]
        delete_task_name = st.selectbox("Task to Delete",unique_list)
        if st.button("Delete"):
            delete_task(delete_task_name)
            st.warning(f"{delete_task_name} deleted")

        with st.expander("Current Database"):
            res = view_all_tasks()
            new_df=pd.DataFrame(res,columns=[TASK_DOER,TASK_NAME,TASK_STATUS, TASK_DUE_DATE])
            st.dataframe(new_df)

    else:
        st.subheader("Analytics")
        res= view_all_tasks()
        df = pd.DataFrame(res,columns=[TASK_DOER,TASK_NAME,TASK_STATUS, TASK_DUE_DATE])
    
        with st.expander("View all tasks"):
             st.dataframe(df)

        with st.expander("Task Doer Stats"):
            st.dataframe(df[TASK_DOER].value_counts())
            doer_df = df[TASK_DOER].value_counts().to_frame()
            doer_df = doer_df.reset_index()

            p1 = px.pie(doer_df,names=TASK_DOER,values='count')
            st.plotly_chart(p1)

        with st.expander("Task Stats"):
            st.dataframe(df[TASK_NAME].value_counts())
            task_df = df[TASK_NAME].value_counts().to_frame()
            task_df = task_df.reset_index()

            p2 = px.pie(task_df,names=TASK_NAME,values='count')
            st.plotly_chart(p2)

