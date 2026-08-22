import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import sqlite3

st.header("Student Mental health Tracker")

#TO REMEMBER USER NAME
if "user" not in st.session_state:
    st.session_state.user = None

# Database Connection
conn = sqlite3.connect("mentalhealth.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()

# Mood Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS moods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    mood TEXT
)
""")
# Journal Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS journal(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    entry TEXT
)
""")


conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
)
""")

conn.commit()

# Page Settings
st.set_page_config(page_title="Mindful")



#Sidebar Menu
page = st.sidebar.selectbox(
    "Menu",
    [
        "Login",
        "Register",
        "Home",
        "Mood Tracker",
        "Journal",
        "Mood Analytics",
        "Meditation",
        "Profile",
        "Emergency Help"
    ]
)
if st.session_state.user:
    st.sidebar.write("Logged in as:", st.session_state.user)

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

#Register page
if page == "Register":

    st.header("📝 Register/create new account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        try:
            cursor.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (name, email, password)
            )
            conn.commit()
            st.success("Registration Successful")

        except sqlite3.IntegrityError:
            st.error("Email already registered. Please Login.")
#login page
elif page == "Login":

    st.header("🔐 Login/for existing user")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        )

        user = cursor.fetchone()

        if user:
            st.session_state.user = user[1]     # Name
            st.session_state.email = user[2]    # Email

            st.success("Login Successful")
                    

        else:
            st.error("Invalid Login")

if st.session_state.user is None and page not in ["Login", "Register"]:
    st.warning("Please Login First")
    st.stop()           

# HOME PAGE
elif page == "Home":

    if st.session_state.user:

        st.header(f"Hello {st.session_state.user} 👋")

        st.info(
            "🌟 Daily Quote: Small progress is still progress."
        )

    else:
        st.warning("Please Login First")

# MOOD TRACKER PAGE
elif page == "Mood Tracker":

    st.header("Mood Tracker")

    mood = st.radio(
        "How are you feeling today?",
        [
            "😊 Happy",
            "😐 Okay",
            "😔 Sad",
            "😣 Stressed"
        ]
    )

    if st.button("Save Mood"):

        cursor.execute(
            "INSERT INTO moods(email,mood) VALUES(?,?)",
            (st.session_state.email, mood)
        )

        conn.commit()

        st.success("Mood Saved Successfully")

    st.subheader("Mood History")

    cursor.execute(
        "SELECT mood FROM moods WHERE email=?",
        (st.session_state.email,)
    )

    moods = cursor.fetchall()

    for item in moods:
        st.write(item[0])

# JOURNAL PAGE
elif page == "Journal":

    st.header("Journal")

    entry = st.text_area(
        "How was your day?"
    )

    if st.button("Save Journal"):

        cursor.execute(
            "INSERT INTO journal(entry) VALUES(?)",
            (entry,)
        )

        conn.commit()

        st.success("Journal Saved Successfully")

    st.subheader("Previous Entries")

    cursor.execute(
        "SELECT entry FROM journal"
    )

    entries = cursor.fetchall()
    if entries:
        for item in entries:
            st.write("•", item[0])
    else:
        st.write("No Journal Entries Found")

# PROFILE PAGE
elif page == "Profile":

    st.header("👤 My Profile")

    st.write("Name:", st.session_state.user)
    st.write("Email:", st.session_state.email)

    # Mood Count
    cursor.execute(
        "SELECT COUNT(*) FROM moods WHERE email=?",
        (st.session_state.email,)
    )

    mood_count = cursor.fetchone()[0]

    # Journal Count
    cursor.execute(
        "SELECT COUNT(*) FROM journal WHERE email=?",
        (st.session_state.email,)
    )

    journal_count = cursor.fetchone()[0]

    st.write("😊 Total Mood Entries:", mood_count)
    st.write("📖 Total Journal Entries:", journal_count)

    st.subheader("Account")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.email = None
        st.success("Logged Out Successfully")

#Meditation Page
elif page == "Meditation":

    st.header("🧘 Meditation")

    option = st.selectbox(
        "Choose Meditation",
        [
            "5 Minute Meditation",
            "10 Minute Breathing Exercise",
            "Sleep Relaxation"
        ]
    )

    st.write("Selected:", option)

    if st.button("Start"):
        st.success("Meditation Started")

# Emergency Help Page
elif page == "Emergency Help":

    st.header("🚨 Emergency Help")

    st.error("Need Support?")

    st.write("📞 AASRA Helpline")
    st.write("9820466726")

    st.write("📞 iCALL Helpline")
    st.write("9152987821")

    st.write("📞 College Counselor")
    st.write("Please contact your college's counseling center for local support.")
    st.info("If you are in immediate danger, contact your local emergency services.")


# Mood Analytics Page
elif page == "Mood Analytics":

    st.header("📊 Mood Analytics")

    cursor.execute(
        "SELECT mood FROM moods WHERE email=?",
        (st.session_state.email,)
    )

    moods = cursor.fetchall()

    if moods:

        mood_list = [m[0] for m in moods]

        df = pd.DataFrame(
            mood_list,
            columns=["Mood"]
        )

        mood_count = df["Mood"].value_counts()

        fig, ax = plt.subplots()

        mood_count.plot(
            kind="bar",
            ax=ax
        )

        st.pyplot(fig)

    else:
        st.warning("No Mood Data Available")