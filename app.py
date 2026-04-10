import streamlit as st
import pandas as pd

# ---------------- SESSION INIT ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------- STUDENT DATA (5 SUBJECTS) ----------------
students = {
    "101": {
        "name": "Rahul",
        "data": {
            "MATHEMETICS": [80, 75, 90],
            "PHYSICS": [30, 40, 35],
            "CHEMISTRY": [60, 55, 65],
            "DSA": [45, 50, 40],
            "PYTHON": [25, 30, 35]
        }
    },
    "102": {
        "name": "Anjali",
        "data": {
            "MATHEMATICS": [50, 55, 60],
            "PHYSICS": [70, 75, 80],
            "CHEMISTRY": [40, 45, 50],
            "DSA": [65, 70, 75],
            "PYTHON": [55, 60, 65]
        }
    }
}

# ---------------- FUNCTIONS ----------------
def calculate_performance(student):
    return {t: sum(s)/len(s) for t, s in student["data"].items()}

# ---------------- LOGIN ----------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = st.session_state.users
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

    st.write("New user?")
    if st.button("Go to Register"):
        st.session_state.page = "register"
        st.rerun()

# ---------------- REGISTER ----------------
def register():
    st.title("📝 Register")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Register"):
        users = st.session_state.users
        if username in users:
            st.warning("User already exists ⚠️")
        else:
            users[username] = password
            st.session_state.users = users
            st.success("Registered successfully 🎉")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# ---------------- HOME ----------------
def home():
    st.title("🏠 Home Page")
    st.write("Welcome to AI Study Assistant 🎓")

    if st.button("Open Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("📊 Student Dashboard")

    student_id = st.text_input("Enter Student ID")

    if student_id == "":
        st.info("Please enter Student ID")
        return

    if student_id in students:
        student = students[student_id]

        st.subheader(f"👤 {student['name']}")

        # Subject selection (5 subjects)
        subjects = list(student["data"].keys())
        selected_subject = st.selectbox("Choose Subject", subjects)

        scores = student["data"][selected_subject]
        avg = sum(scores) / len(scores)

        st.write(f"📘 {selected_subject} Scores:", scores)
        st.write(f"⭐ Average:", round(avg, 2))

        # Chart
        df = pd.DataFrame({
            "Attempt": list(range(1, len(scores) + 1)),
            "Score": scores
        })

        st.line_chart(df.set_index("Attempt"))

        # Weak topic detection
        if avg < 50:
            st.error(f"⚠️ Weak in {selected_subject}")
            st.write(f"💡 Practice more {selected_subject}")
        else:
            st.success(f"Good in {selected_subject} 🎉")

    else:
        st.error("Student not found ❌")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- ROUTING ----------------
page = st.session_state.page

if page == "login":
    login()

elif page == "register":
    register()

elif page == "home":
    if st.session_state.logged_in:
        home()
    else:
        st.session_state.page = "login"
        st.rerun()

elif page == "dashboard":
    if st.session_state.logged_in:
        dashboard()
    else:
        st.session_state.page = "login"
        st.rerun()

else:
    st.session_state.page = "login"
    st.rerun()