import streamlit as st
import sqlite3
import random

# === 連線到 SQLite 資料庫 ===
conn = sqlite3.connect("questions.db")
c = conn.cursor()

# === 初始化 SessionState 儲存答題進度 ===
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None

# === 標題 ===
st.title("📝 題庫練習系統")

# === 選擇年份 ===
year_options = [row[0] for row in c.execute("SELECT DISTINCT year FROM questions").fetchall()]
year = st.selectbox("請選擇年份：", year_options)

# === 載入題目 ===
def load_random_question():
    rows = c.execute("SELECT * FROM questions WHERE year=?", (year,)).fetchall()
    if rows:
        st.session_state.current_question = random.choice(rows)
    else:
        st.warning("查無題目")

# === 初始載入題目 ===
if st.session_state.current_question is None:
    load_random_question()

# === 顯示題目 ===
q = st.session_state.current_question

if q:
    st.markdown(f"### 題目 {q[0]}")
    st.markdown(q[2])  # 題幹
    options = {
        "A": q[3],
        "B": q[4],
        "C": q[5],
        "D": q[6],
    }
    user_answer = st.radio("請選擇答案：", list(options.keys()), format_func=lambda k: f"{k}. {options[k]}")

    if st.button("提交答案"):
        st.session_state.question_count += 1
        if user_answer == q[7]:
            st.success("✅ 答對了！")
            st.session_state.score += 1
        else:
            st.error(f"❌ 答錯了，正確答案是 {q[7]}：{options[q[7]]}")

        # 下一題按鈕
        if st.button("下一題"):
            load_random_question()
            st.rerun()

# === 顯示統計 ===
if st.session_state.question_count > 0:
    st.info(f"你已作答 {st.session_state.question_count} 題，答對 {st.session_state.score} 題，正確率 {(st.session_state.score / st.session_state.question_count) * 100:.1f}%")
