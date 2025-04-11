import streamlit as st
import sqlite3
import random

# === 初始化狀態 ===
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "user_answer" not in st.session_state:
    st.session_state.user_answer = None
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# === 題目載入函式 ===
def load_question():
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    result = c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    st.session_state.current_question = result
    st.session_state.user_answer = None
    st.session_state.show_result = False
    st.session_state.feedback = ""

# 初次載入
if st.session_state.current_question is None:
    load_question()

# === 顯示題目 ===
q = st.session_state.current_question
st.title("📘 題庫練習系統")
st.markdown(f"#### 題目 {q[0]}：{q[2]}")
options = {"A": q[3], "B": q[4], "C": q[5], "D": q[6]}

# === 顯示選項 ===
if not st.session_state.show_result:
    st.session_state.user_answer = st.radio(
        "請選擇答案：", list(options.keys()),
        format_func=lambda x: f"{x}. {options[x]}"
    )
    if st.button("✅ 提交答案"):
        st.session_state.show_result = True
        st.session_state.question_count += 1
        correct = q[7]
        if st.session_state.user_answer == correct:
            st.session_state.score += 1
            st.session_state.feedback = f"✅ 答對了！答案是 {correct}：{options[correct]}"
        else:
            st.session_state.feedback = f"❌ 答錯了，正確答案是 {correct}：{options[correct]}"

# === 顯示結果（和題目同頁）===
if st.session_state.show_result:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

    if st.button("➡️ 下一題"):
        load_question()

# === 統計資訊 ===
if st.session_state.question_count > 0:
    st.markdown("---")
    st.info(
        f"已作答 {st.session_state.question_count} 題，"
        f"答對 {st.session_state.score} 題，"
        f"正確率：{(st.session_state.score / st.session_state.question_count) * 100:.1f}%"
    )
