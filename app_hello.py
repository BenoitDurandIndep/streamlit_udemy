import streamlit as st

name="Ben"

st.set_page_config(page_title="Hello world")

st.header("The header")
st.subheader("The subheader")
st.title("A nice title")
st.text(f"First Hello World {name}")
st.markdown("## This is a markdown")

if st.button("Submit"):
    st.write(f"Name : {name.upper()}")

if st.button("Submit",key="new02"):
    st.write(f"name : {name.lower()}")

status=st.radio("What is your status",("Active","Inactive"))
if status=="Active":
    st.success("You are active")
elif status=="Inactive":
    st.warning("Your are inactive")

if st.checkbox("Show/Hide"):
    st.text("Showing something")

with st.expander("Bob"):
    st.write(f"Hi Bob")

my_friends=["Bob","Julia","Rourou"]
choice=st.selectbox("Friend",my_friends)
st.write(f"You selected {choice}")

spoken_lang=("English","French","Spanish")
my_spoken_lang=st.multiselect("Spoken lang",spoken_lang,default="English")  

age=st.slider("Age",1,100,5)

color=st.select_slider("Choose color",options=["red","yellow","white","black"],value=("red","yellow"))

st.success("Sucess")
st.warning("A warning")
st.info("This is an info")
st.error("A bad error")
st.exception("I catch this")