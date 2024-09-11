import streamlit as st
import mysql.connector
from dbc import cur,conn

def app():
    import streamlit as st
import pandas as pd
from dbc import cur, conn

# Function to load and return department data
@st.cache_data
def load_departments():
    try:
        query = 'SELECT deptid, dname FROM dept'
        cur.execute(query)
        departments = cur.fetchall()
        return pd.DataFrame(departments, columns=['DeptID', 'DName'])
    except Exception as e:
        st.error(f'Error fetching departments: {e}')
        return pd.DataFrame(columns=['DeptID', 'DName'])

def app():
    st.write('Add New Employee')
    
    # Display existing departments for selection
    dept_df = load_departments()
    if not dept_df.empty:
        st.subheader('Select Department for New Employee')
        # Create a dictionary for department selection
        department_options = dept_df.set_index('DeptID')['DName'].to_dict()
        selected_deptid = st.selectbox('Select Department', options=department_options.keys(), format_func=lambda x: department_options[x])
    else:
        st.write('No departments available. Please add departments first.')

    # Input fields for employee details
    st.subheader('Insert a new record')
    eid = st.text_input('Enter Employee ID')
    name = st.text_input('Enter Employee Name')
    mgr = st.text_input('Enter Manager Name (Optional)')
    sal = st.number_input('Enter Salary', min_value=0)
    
    try:
        if st.button('Insert'):
            # Validate inputs
            if eid and name and selected_deptid:
                # SQL query to insert a new employee record
                query = 'INSERT INTO emp (eid, name, mgr, sal, deptid) VALUES (%s, %s, %s, %s, %s)'
                val = (eid, name, mgr, sal, selected_deptid)
                cur.execute(query, val)
                conn.commit()
                st.success('Record inserted successfully!')
                
                #Clear the input fields after insertion
                # st.text_input('Enter Employee ID', value='', key='eid')
                # st.text_input('Enter Employee Name', value='', key='name')
                # st.text_input('Enter Manager ID (Optional)', value='', key='mgr')
                # st.number_input('Enter Salary', min_value=0, value=0, key='sal')
            else:
                st.error('Please fill in all required fields.')
    except Exception as e:
        st.error(f'An error occurred: {e}')
