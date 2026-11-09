# 🎓 Student Management System (Streamlit Frontend)

A modern, responsive, and completely API-driven **Student Management Portal** built with Python and Streamlit. This application allows educational institutions or course managers to easily handle student records via secure CRUD (Create, Read, Update, Delete) operations.

---

## ✨ Features

- **📊 Interactive Dashboard:** View live KPI metrics at a glance, including total active students, average age, and unique course tracks.
- **🔍 Advanced Data Grid:** Display all student records in an interactive, searchable, and filterable data table.
- **➕ Student Registration:** A clean form layout to onboard new students with names, ages, courses, and letter grades.
- **✏️ Profile Customization:** Select any student from a dropdown menu to instantly overwrite or patch their profile details.
- **❌ Safe Record Deletion:** Features an explicit confirmation mechanism to prevent accidental data wipes.
- **📥 CSV Data Export:** Download the entire student registry into a standard Excel-compatible CSV file with a single click.

---

## 🛠️ Requirements & Installation

Before running this project, ensure you have **Python 3.8+** installed on your system.

1. Install the required external Python dependencies using `pip`:
```bash
pip install streamlit requests pandas
```

2. Save the application code into a file named `app.py`.

---

## 🚀 How to Run

Open your terminal or Command Prompt (CMD), navigate to the folder containing your script, and execute the following command:

```bash
streamlit run app.py
```

Streamlit will automatically spin up a local development server and open the web dashboard in your default browser at `http://localhost:8501`.

---

## 📂 Project Architecture

The application code is highly organized and split into two primary contexts:
1. **Mock API Backend:** Built using Streamlit's `st.session_state` to safely mimic the behavior of a live REST API layer right out of the box without demanding a database server setup.
2. **Streamlit UI Frontend:** Utilizes clean sidebar navigation, context-rich multi-panel layouts, and built-in error validation flags.

---

## 🔧 Connecting to a Live Production API

To tie this client layer seamlessly to a production backend environment (e.g., FastAPI, Django, Flask, or Node.js), swap out the local mock state calls inside the `MockStudentAPI` static methods for real HTTP methods utilizing the imported `requests` library:

```python
# Simply configure your live server context:
BASE_URL = "https://your-production-domain.com"
```
