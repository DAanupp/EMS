import streamlit as st
import pandas as pd
from dbc import cur, conn

# Function to load employee details from the emp_det view
# @st.cache_data
def load_employee_details():
    try:
        query = 'SELECT * FROM emp_det'
        cur.execute(query)
        employee_details = cur.fetchall()
        return pd.DataFrame(employee_details, columns=['EID', 'Name', 'Manager', 'Salary', 'DeptID', 'Department Name', 'Location'])
    except Exception as e:
        st.error(f'Error fetching employee details: {e}')
        return pd.DataFrame(columns=['EID', 'Name', 'Manager', 'Salary', 'DeptID', 'Department Name', 'Location'])

def app():
    st.title('Employee Details')

    # Load employee details from the view
    employee_df = load_employee_details()

    if not employee_df.empty:
        st.subheader('View Employee Details')
        emp_id = st.text_input('Enter Employee ID to get details')

        if emp_id:
            # Filter the DataFrame for the selected Employee ID
            try:
                emp_id = int(emp_id)  # Ensure the input is an integer
                employee_data = employee_df[employee_df['EID'] == emp_id]

                if not employee_data.empty:
                    st.write('**Employee Details:**')
                    st.dataframe(employee_data, use_container_width=True)
                else:
                    st.write('Employee ID not found.')
            except ValueError:
                st.error('Please enter a valid Employee ID.')
    else:
        st.write('No employee details available.')

