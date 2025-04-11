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

# === 題目載入函式 ===
def load_question():
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    result = c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    st.session_state.current_question = result
    st.session_state.user_answer = None
    st.session_state.show_result = False

# 首次載入
if st.session_state.current_question is None:
    load_question()

# === 顯示題目 ===
q = st.session_state.current_question
st.title("📘 題庫練習系統")
st.markdown(f"#### 題目 {q[0]}：{q[2]}")
options = {"A": q[3], "B": q[4], "C": q[5], "D": q[6]}

# === 顯示選項與「提交答案」表單（只有未提交時顯示）===
if not st.session_state.show_result:
    with st.form("answer_form", clear_on_submit=False):
        selected = st.radio("請選擇答案：", list(options.keys()), format_func=lambda x: f"{x}. {options[x]}")
        submitted = st.form_submit_button("✅ 提交答案")
        if submitted:
            st.session_state.user_answer = selected
            st.session_state.show_result = True
            st.session_state.question_count += 1
            if selected == q[7]:
                st.success(f"答對了！答案是 {q[7]}：{options[q[7]]}")
                st.session_state.score += 1
            else:
                st.error(f"答錯了，正確答案是 {q[7]}：{options[q[7]]}")
else:
    # 已答題 → 顯示結果（前面已顯示），並給「下一題」
    if st.button("➡️ 下一題"):
        load_question()
        st.rerun()

# === 統計資訊 ===
if st.session_state.question_count > 0:
    st.markdown("---")
    st.info(f"已作答 {st.session_state.question_count} 題，答對 {st.session_state.score} 題，正確率：{(st.session_state.score / st.session_state.question_count) * 100:.1f}%")
