import streamlit as st
from dbc import cur, conn
import pandas as pd

def get_employee_details(emp_id):
    try:
        # Fetch the employee details
        query = """
        SELECT * FROM emp_det WHERE eid = %s
        """
        cur.execute(query, (emp_id,))
        employee = cur.fetchone()
        if employee:
            return pd.DataFrame([employee], columns=['EID', 'Name', 'Manager', 'Salary', 'DeptID', 'Department Name', 'Location'])
        else:
            st.error("Employee ID not found.")
            return pd.DataFrame(columns=['EID', 'Name', 'Manager', 'Salary', 'DeptID', 'Department Name', 'Location'])
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame(columns=['EID', 'Name', 'Manager', 'Salary', 'DeptID', 'Department Name', 'Location'])

def update_employee_salary(emp_id, hike_percent):
    try:
        # Call the stored procedure
        cur.callproc('UpdateEmployeeSalary', [emp_id, hike_percent])

        # Fetch and print the result from the stored procedure
        for result in cur.stored_results():
            message = result.fetchone()[0]
            st.success(message)
        
        # Commit the transaction
        conn.commit()
    except Exception as e:
        st.error(f"Error: {e}")

def app():
    st.title('Employee Salary Hike')

    # Fetch employee IDs for the selection box
    try:
        # Fetch all employee IDs
        cur.execute("SELECT eid FROM emp")
        emp_ids = [row[0] for row in cur.fetchall()]

        if emp_ids:
            emp_id = st.selectbox('Select Employee ID', emp_ids)

            # Select box for hike percentage
            hike_percent = st.selectbox(
                'Select Hike Percentage',
                [5, 10, 15, 20, 25, 30]  # Example percentages
            )

            if st.button('Give Hike'):
                update_employee_salary(emp_id, hike_percent)

                # Display employee details after update
                st.subheader('Employee Details')
                employee_df = get_employee_details(emp_id)
                if not employee_df.empty:
                    st.dataframe(employee_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")
