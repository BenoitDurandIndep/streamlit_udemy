import sqlite3

con = sqlite3.connect("data.db", check_same_thread=False)
c=con.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS TASK(TASK_DOER VARCHAR(100), TASK_NAME TEXT ,TASK_STATUS VARCHAR(20),TASK_DUE_DATE DATE )")

def add_data(task_doer,task_name,task_status,task_due_date):
    c.execute("INSERT INTO TASK(TASK_DOER,TASK_NAME,TASK_STATUS,TASK_DUE_DATE) VALUES (?,?,?,?)",(task_doer,task_name,task_status,task_due_date))
    con.commit()

def view_all_tasks():
    c.execute("SELECT TASK_DOER,TASK_NAME,TASK_STATUS,TASK_DUE_DATE FROM TASK")   
    data = c.fetchall()
    return data 

def view_all_tasks_names():
    c.execute("SELECT DISTINCT TASK_NAME FROM TASK")   
    data = c.fetchall()
    return data 

def get_task_by_name(task_name:str):
    c.execute(f"SELECT TASK_DOER,TASK_NAME,TASK_STATUS,TASK_DUE_DATE FROM TASK WHERE TASK_NAME='{task_name}'")   
    data = c.fetchall()
    return data 

def edit_task_data(new_task_doer,new_task_name,new_task_status,new_task_due_date,
                   task_doer,task_name,task_status):
    c.execute("UPDATE TASK SET TASK_DOER=?,TASK_NAME=?,TASK_STATUS=?,TASK_DUE_DATE=? WHERE TASK_DOER=? AND TASK_NAME=? AND TASK_STATUS=?",
              (new_task_doer,new_task_name,new_task_status,new_task_due_date,task_doer,task_name,task_status))
    con.commit()
    return c.fetchall()

def delete_task(task_name):
    c.execute("DELETE FROM TASK WHERE TASK_NAME=?",(task_name,))
    con.commit()