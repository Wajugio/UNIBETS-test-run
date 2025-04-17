import streamlit as st
import sqlite3
import random
import datetime
from PIL import Image

# ---------- DB SETUP ----------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bets (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        match TEXT,
        amount REAL,
        outcome TEXT,
        result TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

# ---------- LOGIN ----------
def login(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

# ---------- REGISTER ----------
def register(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# ---------- BET ----------
def place_bet(user_id, match, outcome, amount):
    result = random.choice(["Win", "Lose"])
    timestamp = datetime.datetime.now().isoformat()
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO bets (user_id, match, amount, outcome, result, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, match, amount, outcome, result, timestamp))
    conn.commit()
    conn.close()
    return result

# ---------- GET USER BET COUNT FOR WEEK ----------
def get_weekly_bet_count(user_id):
    one_week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM bets WHERE user_id = ? AND timestamp >= ?", (user_id, one_week_ago))
    count = c.fetchone()[0]
    conn.close()
    return count

# ---------- GET BET HISTORY ----------
def get_bets(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT match, amount, outcome, result, timestamp FROM bets WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    bets = c.fetchall()
    conn.close()
    return bets

# ---------- STREAMLIT UI ----------
init_db()
st.title("🎲 UNIBETS")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if st.session_state.user_id is None:
    st.subheader("Login or Register")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user_id = login(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            register(new_user, new_pass)
            st.success("Account created. Please log in.")

else:
    st.success("Logged in ✅")
    st.subheader("🏠 Dashboard")
    st.write("Welcome to UNIBETS! Choose what you'd like to do next.")

    action = st.radio("What would you like to do?", ["🎯 Place a Bet", "📜 Bet History", "🚪 Logout"])

    if action == "🎯 Place a Bet":
        st.header("🎯 Place Your Bet")
        bet_limit = 10
        current_bets = get_weekly_bet_count(st.session_state.user_id)

        if current_bets >= bet_limit:
            st.warning(f"You have reached the weekly bet limit of {bet_limit}.")
        else:
            match = st.text_input("Match (e.g., FIU vs UF)")
            outcome = st.text_input("Your Prediction")
            amount = st.number_input("Bet Amount", min_value=1.0)
            if st.button("Place Bet"):
                result = place_bet(st.session_state.user_id, match, outcome, amount)
                st.info(f"Bet Result: {result}")

    elif action == "📜 Bet History":
        st.header("📜 Your Bet History")
        bets = get_bets(st.session_state.user_id)
        if bets:
            st.dataframe(bets, use_container_width=True)
        else:
            st.write("You haven't placed any bets yet.")

    elif action == "🚪 Logout":
        st.session_state.user_id = None
        st.rerun()
