
import streamlit as st
import pandas as pd
import requests

# -----------------------------------------------------------------------------
# 1. MOCK API BACKEND (Simulating a real FastAPI/Flask Student Management API)
# -----------------------------------------------------------------------------
# Streamlit runs top-to-bottom on every interaction. We use st.session_state 
# to keep our mock API data persistent across UI updates.
if "mock_api_db" not in st.session_state:
    st.session_state["mock_api_db"] = {
        1: {"id": 1, "name": "Alice Smith", "age": 20, "course": "Computer Science", "grade": "A"},
        2: {"id": 2, "name": "Bob Jones", "age": 22, "course": "Data Science", "grade": "B"},
        3: {"id": 3, "name": "Charlie Brown", "age": 21, "course": "Mathematics", "grade": "A-"}
    }
    st.session_state["mock_id_counter"] = 4

class MockStudentAPI:
    """
    This wrapper handles API communications. If you deploy a real backend API,
    replace the internal logic of these functions with actual requests.get() / post() calls.
    """
    BASE_URL = "https://example.com" # Change to your live API endpoint

    @staticmethod
    def get_all_students():
        # Live equivalent: return requests.get(MockStudentAPI.BASE_URL).json()
        return list(st.session_state["mock_api_db"].values())

    @staticmethod
    def create_student(name: str, age: int, course: str, grade: str):
        # Live equivalent: return requests.post(MockStudentAPI.BASE_URL, json={...}).json()
        new_id = st.session_state["mock_id_counter"]
        student = {"id": new_id, "name": name, "age": age, "course": course, "grade": grade}
        st.session_state["mock_api_db"][new_id] = student
        st.session_state["mock_id_counter"] += 1
        return {"status": "success", "student": student}

    @staticmethod
    def update_student(student_id: int, name: str, age: int, course: str, grade: str):
        # Live equivalent: return requests.put(f"{MockStudentAPI.BASE_URL}/{student_id}", json={...}).json()
        if student_id in st.session_state["mock_api_db"]:
            student = {"id": student_id, "name": name, "age": age, "course": course, "grade": grade}
            st.session_state["mock_api_db"][student_id] = student
            return {"status": "success", "student": student}
        return {"status": "error", "message": "Student not found"}

    @staticmethod
    def delete_student(student_id: int):
        # Live equivalent: return requests.delete(f"{MockStudentAPI.BASE_URL}/{student_id}").json()
        if student_id in st.session_state["mock_api_db"]:
            del st.session_state["mock_api_db"][student_id]
            return {"status": "success", "message": "Student deleted"}
        return {"status": "error", "message": "Student not found"}


# -----------------------------------------------------------------------------
# 2. STREAMLIT FRONTEND UI
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Student Management System", layout="wide", page_icon="🎓")
st.title("🎓 Student Management Portal (API Driven)")
st.write("Manage student records securely through CRUD operations syncing with your backend API.")

# Fetch data via API context wrapper
students_list = MockStudentAPI.get_all_students()
df = pd.DataFrame(students_list)

# Layout Setup: Left Sidebar for Actions, Right Area for Records & Dashboard
menu = ["📊 Dashboard & View", "➕ Add Student", "✏️ Update Student", "❌ Delete Student"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# --- PANEL 1: DASHBOARD & VIEW RECORDS ---
if choice == "📊 Dashboard & View":
    st.subheader("Student Database Records")
    
    if not df.empty:
        # Display key summary KPI blocks
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Active Students", len(df))
        col2.metric("Average Student Age", f"{df['age'].mean():.1f} yrs")
        col3.metric("Unique Programs/Courses", df["course"].nunique())
        
        # Interactive searchable UI dataframe view
        st.dataframe(df.set_index("id"), use_container_width=True)
        
        # CSV Data Export Utility
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Database to CSV",
            data=csv_data,
            file_name="student_records.csv",
            mime="text/csv"
        )
    else:
        st.info("The student registry database is currently empty.")

# --- PANEL 2: ADD NEW STUDENT ---
elif choice == "➕ Add Student":
    st.subheader("Register a New Student")
    
    with st.form("add_student_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=120, value=20)
        course = st.text_input("Course / Program")
        grade = st.selectbox("Current Letter Grade", ["A+", "A", "A-", "B+", "B", "B-", "C", "D", "F"])
        
        submitted = st.form_submit_button("Submit API Request")
        
        if submitted:
            if name.strip() == "" or course.strip() == "":
                st.error("Name and Course fields cannot be left blank.")
            else:
                response = MockStudentAPI.create_student(name, age, course, grade)
                if response.get("status") == "success":
                    st.success(f"Success! {name} has been given ID #{response['student']['id']}.")
                    st.rerun()

# --- PANEL 3: UPDATE EXISTING RECORD ---
elif choice == "✏️ Update Student":
    st.subheader("Modify Student Information")
    
    if not df.empty:
        student_to_update = st.selectbox(
            "Select Student Profile to Edit", 
            options=students_list, 
            format_func=lambda x: f"ID: {x['id']} | {x['name']}"
        )
        
        # Populate input forms with current values fetched from target student profile
        with st.form("update_student_form"):
            updated_name = st.text_input("Full Name", value=student_to_update["name"])
            updated_age = st.number_input("Age", min_value=1, max_value=120, value=student_to_update["age"])
            updated_course = st.text_input("Course / Program", value=student_to_update["course"])
            updated_grade = st.selectbox(
                "Current Letter Grade", 
                ["A+", "A", "A-", "B+", "B", "B-", "C", "D", "F"],
                index=["A+", "A", "A-", "B+", "B", "B-", "C", "D", "F"].index(student_to_update["grade"])
            )
            
            save_changes = st.form_submit_button("Save Updates via API")
            
            if save_changes:
                res = MockStudentAPI.update_student(student_to_update["id"], updated_name, updated_age, updated_course, updated_grade)
                if res.get("status") == "success":
                    st.success("Record updated successfully.")
                    st.rerun()
    else:
        st.info("No records available to edit.")

# --- PANEL 4: DELETE STUDENT RECORD ---
elif choice == "❌ Delete Student":
    st.subheader("De-register Student Record")
    
    if not df.empty:
        student_to_delete = st.selectbox(
            "Select Student Profile to Remove", 
            options=students_list, 
            format_func=lambda x: f"ID: {x['id']} | {x['name']} ({x['course']})"
        )
        
        st.warning(f"Are you sure you want to permanently delete {student_to_delete['name']}?")
        confirm_delete = st.button("Confirm Hard Delete")
        
        if confirm_delete:
            res = MockStudentAPI.delete_student(student_to_delete["id"])
            if res.get("status") == "success":
                st.success(f"Record for ID #{student_to_delete['id']} cleared.")
                st.rerun()
    else:
        st.info("No student data available to wipe.")
