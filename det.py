import streamlit as st
import pandas as pd
from dbc import cur

def app():
    st.subheader('View Employee Details')

    #all emp
    if st.button('View Details of All Employees'):
        cur.execute('SELECT * FROM emp_det order by eid')
        res = cur.fetchall()
        st.write(pd.DataFrame(res, columns=['EMPID', 'NAME', 'MGR', 'SALARY', 'DEPTNO', 'DEPT_NAME', 'CITY'])) 
    
    # specific emp
    if st.button('View Details of Specific Employee'):
        st.session_state.show_input = True
    
    if st.session_state.get('show_input', False):
        id = st.text_input('Enter Employee ID')
        if st.button('Get details'):
            if id:
                try:
                    cur.execute('SELECT * FROM emp_det WHERE eid = %s', (id,))
                    res1 = cur.fetchall()
                    if res1:
                        st.write(pd.DataFrame(res1, columns=['EMPID', 'NAME', 'MGR', 'SALARY', 'DEPTNO', 'DEPT_NAME', 'CITY']))
                    else:
                        st.write("No employee found with the provided ID.")
                except Exception as e:
                    st.write(f"An error occurred: {e}")

