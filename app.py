import streamlit as st
import sqlite3

# Database Connection
conn = sqlite3.connect("mentalhealth.db")
cursor = conn.cursor()

# Mood Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS moods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT
)
""")

# Journal Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS journal(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry TEXT
)
""")

conn.commit()

# Page Settings
st.set_page_config(page_title="Mindful")

# App Title
st.title("🧠 Mindful")
st.subheader("Student Mental Health App")

# Sidebar Menu
page = st.sidebar.selectbox(
    "Menu",
    ["Home", "Mood Tracker", "Journal", "Profile"]
)

# HOME PAGE
if page == "Home":

    st.header("Hello Manasi 👋")

    st.info(
        "🌟 Daily Quote: Small progress is still progress."
    )

    st.write(
        "Welcome to your Mental Wellness Companion."
    )

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
            "INSERT INTO moods(mood) VALUES(?)",
            (mood,)
        )

        conn.commit()

        st.success("Mood Saved Successfully")

    st.subheader("Mood History")

    cursor.execute(
        "SELECT mood FROM moods"
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

    for item in entries:
        st.write("•", item[0])

# PROFILE PAGE
elif page == "Profile":

    st.header("Profile")

    st.write("Name: Manasi")
    st.write("Course: BSc Computer Science")

    cursor.execute(
        "SELECT COUNT(*) FROM moods"
    )

    mood_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM journal"
    )

    journal_count = cursor.fetchone()[0]

    st.write("Total Mood Entries:", mood_count)
    st.write("Total Journal Entries:", journal_count)