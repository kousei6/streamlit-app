import streamlit as st
import random
import time

# --- 定数とデータ ---
QUOTES = [
    "A journey of a thousand miles begins with a single step.",
    "The early bird catches the worm.",
    "All that glitters is not gold.",
    "Practice makes perfect.",
    "Where there's a will, there's a way.",
    "Look before you leap.",
    "Two heads are better than one.",
    "Actions speak louder than words."
]

# --- Streamlitアプリのロジック ---
def initialize_state():
    """セッションステートを初期化する"""
    st.session_state.start_time = None
    st.session_state.typing_text = random.choice(QUOTES)
    st.session_state.is_typing = False
    st.session_state.user_input = ""
    st.session_state.completed = False

def start_typing():
    """タイピングを開始する"""
    st.session_state.is_typing = True
    st.session_state.start_time = time.time()
    st.session_state.user_input = ""
    st.session_state.completed = False

def calculate_wpm(start_time, end_time, user_input):
    """WPMを計算する"""
    typing_time_seconds = end_time - start_time
    # WPM = (文字数 / 5) / (経過時間(分))
    words = len(user_input.split())
    if typing_time_seconds > 0:
        return (words / typing_time_seconds) * 60
    return 0

def calculate_accuracy(original_text, user_input):
    """正確性を計算する"""
    correct_chars = 0
    min_len = min(len(original_text), len(user_input))
    for i in range(min_len):
        if original_text[i] == user_input[i]:
            correct_chars += 1
    # 正確性(%) = (正しい文字数 / ユーザーが入力した文字数) * 100
    if len(user_input) > 0:
        return (correct_chars / len(user_input)) * 100
    return 0

def main():
    st.set_page_config(page_title="TypingTutor", layout="wide")

    st.title("👨‍💻 TypingTutor")
    st.markdown("---")

    # セッションステートの初期化
    if 'typing_text' not in st.session_state:
        initialize_state()

    # サイドバーにステータスを表示
    with st.sidebar:
        st.header("ステータス")
        if st.session_state.is_typing and not st.session_state.completed:
            elapsed_time = time.time() - st.session_state.start_time
            wpm = calculate_wpm(st.session_state.start_time, time.time(), st.session_state.user_input)
            st.metric("経過時間", f"{elapsed_time:.2f} 秒")
            st.metric("リアルタイムWPM", f"{wpm:.2f}")

        if st.button("再挑戦"):
            initialize_state()
            st.rerun()

    # メインコンテンツ
    st.subheader("表示されたテキストをタイピングしてください")
    st.text_area(
        label="お題",
        value=st.session_state.typing_text,
        height=100,
        disabled=True
    )

    # ユーザー入力
    user_input = st.text_input(
        label="ここにタイピング",
        value=st.session_state.user_input,
        on_change=lambda: st.session_state.update(user_input=st.session_state.user_input_key),
        key="user_input_key"
    )

    # タイピング開始のトリガー
    if not st.session_state.is_typing and user_input and not st.session_state.completed:
        start_typing()

    # 完了判定
    if st.session_state.is_typing and user_input == st.session_state.typing_text:
        st.session_state.is_typing = False
        st.session_state.completed = True
        end_time = time.time()
        
        final_wpm = calculate_wpm(st.session_state.start_time, end_time, user_input)
        accuracy = calculate_accuracy(st.session_state.typing_text, user_input)

        st.success("タイピング完了！お疲れ様でした！🎉")
        st.metric("最終WPM", f"{final_wpm:.2f}")
        st.metric("正確性", f"{accuracy:.2f} %")

    # アプリ実行
if __name__ == "__main__":
    main()
