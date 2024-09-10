import streamlit as st
import pandas as pd
from dbc import cur, conn

def app():
    
    # Display existing departments
    try:
        query = 'SELECT * FROM dept'
        cur.execute(query)
        departments = cur.fetchall()
        
        if departments:
            st.subheader('Existing Departments')
            dept_df = pd.DataFrame(departments, columns=['DeptID', 'DName', 'Loc'])
            dept_df=dept_df.reset_index(drop=True)
            st.dataframe(dept_df)
        else:
            st.write('No departments found.')
    except Exception as e:
        st.error(f'Error fetching departments: {e}')
    
    # Input fields for department details
    st.subheader('Add Department')
    deptid = st.text_input('Enter Department ID')
    dname = st.text_input('Enter Department Name')
    loc = st.text_input('Enter Location')

    try:
        if st.button('Insert'):
            # Validate inputs
            if deptid and dname and loc:
                # SQL query to insert a new department record
                query = 'INSERT INTO dept (deptid, dname, loc) VALUES (%s, %s, %s)'
                val = (deptid, dname, loc)
                cur.execute(query, val)
                conn.commit()
                st.success('Record inserted successfully!')
            else:
                st.error('Please fill in all fields.')
    except Exception as e:
        st.error(f'An error occurred: {e}')
