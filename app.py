import streamlit as st
import sqlite3
import random

# === 初始化狀態 ===
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "history" not in st.session_state:
    st.session_state.history = []  # 儲存所有作答紀錄
if "current_index" not in st.session_state:
    st.session_state.current_index = -1  # -1 表示目前是最新題目

# === 題目載入函式 ===
def load_new_question():
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    result = c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    return result

# === 初始化新一題 ===
def push_new_question():
    q = load_new_question()
    st.session_state.history.append({
        "question": q,
        "user_answer": None,
        "result": None,
    })
    st.session_state.current_index += 1

# === 首次載入 ===
if len(st.session_state.history) == 0:
    push_new_question()

# === 目前題目 ===
qdata = st.session_state.history[st.session_state.current_index]
q = qdata["question"]
st.title("📘 題庫練習系統")
st.markdown(f"#### 題目 {q[0]}：{q[2]}")

options = {"A": q[3], "B": q[4], "C": q[5], "D": q[6]}

# === 顯示選項 ===
if qdata["user_answer"] is None:
    user_choice = st.radio("請選擇答案：", list(options.keys()), format_func=lambda x: f"{x}. {options[x]}")
    if st.button("✅ 提交答案"):
        qdata["user_answer"] = user_choice
        qdata["result"] = (user_choice == q[7])
        st.session_state.question_count += 1
        if qdata["result"]:
            st.session_state.score += 1
        st.rerun()
else:
    # === 顯示所有選項 + emoji ===
    for k, v in options.items():
        if k == qdata["user_answer"] == q[7]:
            st.markdown(f"👉✅ **{k}. {v}**")
        elif k == qdata["user_answer"] and k != q[7]:
            st.markdown(f"👉❌ **{k}. {v}**")
        elif k == q[7]:
            st.markdown(f"✅ {k}. {v}")
        else:
            st.markdown(f"⬜ {k}. {v}")

    if qdata["result"]:
        st.success(f"答對了！答案是 {q[7]}：{options[q[7]]}")
    else:
        st.error(f"答錯了，正確答案是 {q[7]}：{options[q[7]]}")

# === 上一題 / 下一題 按鈕 ===
col1, col2 = st.columns(2)
with col1:
    if st.session_state.current_index > 0:
        if st.button("⬅️ 上一題"):
            st.session_state.current_index -= 1
            st.rerun()
with col2:
    if st.session_state.current_index < len(st.session_state.history) - 1:
        if st.button("➡️ 下一題"):
            st.session_state.current_index += 1
            st.rerun()
    elif qdata["user_answer"] is not None:
        if st.button("🆕 新題目"):
            push_new_question()
            st.rerun()

# === 統計資訊 ===
if st.session_state.question_count > 0:
    st.markdown("---")
    st.info(f"已作答 {st.session_state.question_count} 題，答對 {st.session_state.score} 題，正確率：{(st.session_state.score / st.session_state.question_count) * 100:.1f}%")
