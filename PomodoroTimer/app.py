import streamlit as st
import time

# アプリケーションの状態を初期化
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 25 * 60  # デフォルトは25分
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "Work"
if 'work_count' not in st.session_state:
    st.session_state.work_count = 0
if 'is_finished' not in st.session_state:
    st.session_state.is_finished = False

def start_timer(duration_minutes):
    """タイマーを開始します。"""
    st.session_state.timer_running = True
    st.session_state.start_time = time.time()
    st.session_state.total_seconds = duration_minutes * 60
    st.session_state.is_finished = False

def stop_timer():
    """タイマーを停止します。"""
    st.session_state.timer_running = False

def reset_timer():
    """タイマーをリセットし、初期状態に戻します。"""
    stop_timer()
    st.session_state.total_seconds = 25 * 60
    st.session_state.current_mode = "Work"
    st.session_state.is_finished = False
    st.session_state.start_time = None
    st.session_state.work_count = 0

def toggle_mode():
    """モードを切り替えます（作業⇔休憩）。"""
    if st.session_state.current_mode == "Work":
        st.session_state.work_count += 1
        st.session_state.current_mode = "Break"
        duration = 5 if st.session_state.work_count % 4 != 0 else 15
        start_timer(duration)
        st.balloons()
    else:
        st.session_state.current_mode = "Work"
        start_timer(25)

# UI設定
st.set_page_config(
    page_title="Pomodoro Timer",
    page_icon="🍅",
    layout="centered"
)

st.title("🍅 Pomodoro Timer")
st.write("集中力と生産性を高めるためのポモドーロテクニックを実践しましょう。")

# 現在のモードと完了したポモドーロ数を表示
if st.session_state.current_mode == "Work":
    st.header(f"🧑‍💻 作業時間: {st.session_state.work_count + 1}回目")
else:
    st.header(f"☕ 休憩時間")

# タイマー表示
placeholder = st.empty()

# タイマーロジック
if st.session_state.timer_running and not st.session_state.is_finished:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_seconds = st.session_state.total_seconds - elapsed_time

    if remaining_seconds <= 0:
        st.session_state.is_finished = True
        remaining_seconds = 0
        st.toast(f"🎉 {st.session_state.current_mode} 時間が終了しました！")
        time.sleep(1) # toastが表示されるのを待つ
        toggle_mode()

    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)
    
    placeholder.markdown(f"# **{minutes:02d}:{seconds:02d}**")

    # プログレスバー
    progress_ratio = 1 - (remaining_seconds / st.session_state.total_seconds)
    st.progress(progress_ratio)

    time.sleep(1)  # 1秒待機
    st.rerun()
else:
    minutes = int(st.session_state.total_seconds // 60)
    seconds = int(st.session_state.total_seconds % 60)
    placeholder.markdown(f"# **{minutes:02d}:{seconds:02d}**")
    
# コントロールボタン
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ 開始", disabled=st.session_state.timer_running):
        if st.session_state.start_time is None:
            start_timer(25) # 初期状態では25分で開始
        st.rerun()
with col2:
    if st.button("⏸️ 一時停止", disabled=not st.session_state.timer_running):
        stop_timer()
        st.rerun()
with col3:
    if st.button("🔄 リセット"):
        reset_timer()
        st.rerun()
