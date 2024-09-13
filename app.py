import streamlit as st
from streamlit_option_menu import option_menu
import add,add_dept,promote,fire,det

st.title("Employee Management System")

with st.sidebar:
    app = option_menu(
        menu_title='EMS',
        options=["Add Employee", "Employee Details", "Add Department", "Promote Employee", "Fire Employee"],
        icons=["person-plus", "info-circle", "building", "arrow-up-circle", "person-x"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )

if app == "Add Employee":
    add.app()
elif app == "Employee Details":
    det.app()
elif app == "Add Department":
    add_dept.app()
elif app == "Promote Employee":
    promote.app()
elif app == "Fire Employee":
    fire.app()
