from datetime import datetime
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

st.header("Student Mental health Tracker application")

# TO REMEMBER USER NAME
if "user" not in st.session_state:
    st.session_state.user = None

# Database Creation
class conn(sqlite3.Connection):
    """Connection implementation with transaction-aware context management."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        return False


conn = sqlite3.connect(
    "mentalhealth.db",
    check_same_thread=False,
    factory=conn
)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# Mood Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS moods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    mood TEXT,
    date TEXT
)
""")
# Journal Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS journal(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    entry TEXT,
    date TEXT
)
""")

conn.commit()

# Page Settings
st.set_page_config(page_title="Mindful")

# Sidebar Menu
page = st.sidebar.selectbox(
    "Menu",
    [
        "Login",
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
        
        if st.session_state.user is None:
            page = "Login"

# Login page

# Session state for user login error fix
if "user" not in st.session_state:
    st.session_state.user = None

if "email" not in st.session_state:
    st.session_state.email = None

if page == "Login":

    st.header("🔐 Please Login to use app")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Input Validation
        if not email or not password:
            st.error("❌ Please enter email and password!")
        else:
            try:
                cursor.execute(
                    "SELECT * FROM users WHERE email=? AND password=?",
                    (email, password)
                )

                user = cursor.fetchone()

                if user:
                    st.session_state.user = user[1]     # Name
                    st.session_state.email = user[2]    # Email

                    st.success("✅ Login Successful")
                    st.rerun()

                else:
                    st.error("❌ Invalid Email or Password")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

if st.session_state.user is None and page != "Login":
    st.warning("⚠️ Please Login to use app")
    st.stop()           

# HOME PAGE
if page == "Home":

    if st.session_state.user:

        st.header(f"Hello {st.session_state.user} 👋")

        st.info(
            "🌟 Daily Quote: Small progress is still progress."
        )

    else:
        st.warning("⚠️ Please Login First")

# MOOD TRACKER PAGE
if page == "Mood Tracker":

    st.header("Mood Tracker")

    mood_selection = st.radio(
        "How are you feeling today?",
        [
            "😊 Happy",
            "😐 Okay",
            "😔 Sad",
            "😣 Stressed"
        ]
    )
    if st.button("Save Mood:"):
        if not st.session_state.email:
            st.error("❌ Please login first!")
        else:
            try:
                today = datetime.now().strftime("%d-%m-%Y %H:%M")

                cursor.execute(
                    "INSERT INTO moods(email,mood,date) VALUES(?,?,?)",
                    (st.session_state.email, mood_selection, today)
                )
                conn.commit()
                st.success("✅ Mood Saved Successfully")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

    st.subheader("Mood History")

    if st.session_state.email:
        try:
            cursor.execute(
                "SELECT mood, date FROM moods WHERE email=?",
                (st.session_state.email,)
            )

            moods = cursor.fetchall()

            if moods:
                for mood_entry, date in moods:
                    st.write(f"{date}-{mood_entry}")
            else:
                st.info("No mood entries yet. Start tracking your mood!")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# JOURNAL PAGE

# Session state for journal count error fix
if "email" not in st.session_state:
    st.session_state.email = None

if page == "Journal":

    st.header("Journal")

    journal_entry = st.text_area(
        "How was your day?"
    )

    if st.button("Save Journal"):
        if not st.session_state.email:
            st.error("❌ Please login first!")
        elif not journal_entry.strip():
            st.error("❌ Please write something in your journal!")
        else:
            try:
                today = datetime.now().strftime("%d-%m-%Y %H:%M")
                
                cursor.execute(
                        "INSERT INTO journal(email,entry,date) VALUES(?,?,?)",
                        (st.session_state.email, journal_entry, today)
                )
                conn.commit()
                st.success("✅ Journal Saved Successfully")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

    st.subheader("Previous Entries")

    if st.session_state.email:
        try:
            cursor.execute(
                "SELECT entry, date FROM journal WHERE email=? ORDER BY id DESC",
                (st.session_state.email,)
            )

            entries = cursor.fetchall()
            if entries:
                for entry_text, date in entries:
                    st.write(f"{date}")
                    st.write(f"{entry_text}")
                    st.write("---")
            else:
                st.info("No journal entries yet. Start writing!")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# PROFILE PAGE

# Session state for profile count error fix
if "user" not in st.session_state:
    st.session_state.user = None
if "email" not in st.session_state:
    st.session_state.email = None

if page == "Profile":

    st.header("👤 My Profile")

    st.write("Name:", st.session_state.user)
    st.write("Email:", st.session_state.email)

    if st.session_state.email:
        try:
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
            st.subheader("Statistics")
            st.write("😊 Total Mood Entries:", mood_count)
            st.write("📖 Total Journal Entries:", journal_count)
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

    st.subheader("Account")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.email = None
        st.success("✅ Logged Out Successfully")
        st.rerun()

# Meditation Page
if page == "Meditation":

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
        st.success("🧘 Meditation Started - Take a deep breath and relax!")

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

    if st.session_state.email:
        try:
            cursor.execute(
                "SELECT mood FROM moods WHERE email=?",
                (st.session_state.email,)
            )

            moods = cursor.fetchall()

            if len(moods) > 0:

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
                ax.set_xlabel("Mood")
                ax.set_ylabel("Count")
                st.pyplot(fig)

            else:
                st.warning("⚠️ No Mood Data Available - Start tracking your mood!")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
