import streamlit as st
from dbc import cur, conn
import pandas as pd

def get_employee_details(emp_id):
    try:
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

def fire_employee(emp_id):
    try:
        cur.execute("DELETE FROM emp WHERE eid = %s", (emp_id,))
        conn.commit()
        st.success("Employee record deleted successfully.")
    except Exception as e:
        st.error(f"Error: {e}")

def app():
    st.title('Fire Employee')

    emp_id = st.text_input('Enter Employee ID')

    if emp_id:
        # Display employee details
        st.subheader('Employee Details')
        employee_df = get_employee_details(emp_id)
        if not employee_df.empty:
            st.dataframe(employee_df, use_container_width=True)
            
            # Confirmation workflow
            if 'confirm' not in st.session_state:
                st.session_state.confirm = False

            if st.button('Fire Employee'):
                st.session_state.confirm = True
            
            if st.session_state.confirm:
                st.warning("Are you sure you want to fire this employee?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button('Yes, Fire Employee'):
                        fire_employee(emp_id)
                        st.session_state.confirm = False
                with col2:
                    if st.button('No, Cancel'):
                        st.session_state.confirm = False
                        st.info("Employee was not fired.")
    else:
        st.info("Please enter an Employee ID to proceed.")

