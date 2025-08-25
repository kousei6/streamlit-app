import streamlit as st
import datetime
import time

# --- ゲームの状態管理 ---
def initialize_alarm_state():
    """アラームの状態をセッションステートに設定する"""
    if "alarm_on" not in st.session_state:
        st.session_state.alarm_on = False
    if "alarm_time" not in st.session_state:
        st.session_state.alarm_time = datetime.time(8, 0) # 初期設定時刻
    if "alarm_triggered" not in st.session_state:
        st.session_state.alarm_triggered = False

def set_alarm():
    """アラームをセットし、有効にする"""
    st.session_state.alarm_on = True
    st.session_state.alarm_triggered = False
    st.success(f"⏰ アラームを {st.session_state.alarm_time.strftime('%H:%M')} に設定しました。")

def stop_alarm():
    """アラームを停止する"""
    st.session_state.alarm_on = False
    st.session_state.alarm_triggered = False
    st.info("アラームを停止しました。")

def play_sound():
    """
    アラーム音を再生する（Streamlitで直接音を鳴らすのは困難なため、ヒントを提供）
    
    ローカルで実行する場合は、winsound (Windows) や playsound ライブラリを使用できます。
    例: pip install playsound
    
    import playsound
    playsound.playsound('path/to/your/alarm_sound.mp3')
    
    Webアプリの場合、HTML/JavaScriptを`st.components.v1.html`で埋め込むのが一般的です。
    例:
    st.components.v1.html('''
    <audio autoplay loop>
        <source src="your_alarm_sound.mp3" type="audio/mpeg">
    </audio>
    ''', height=0)
    """
    st.warning("🎵 アラームが鳴っています！")

# --- Streamlitアプリのメイン関数 ---
def main():
    st.title("目覚まし時計アプリ")
    st.subheader("時刻を設定して、アラームを鳴らそう")

    initialize_alarm_state()

    st.markdown("---")

    # 現在時刻をリアルタイムで表示
    current_time_placeholder = st.empty()
    
    # ユーザー入力
    st.sidebar.header("設定")
    selected_time = st.sidebar.time_input(
        "アラーム時刻を設定してください",
        value=st.session_state.alarm_time,
        key="alarm_time_input"
    )
    st.session_state.alarm_time = selected_time

    # アラームセットボタン
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("アラームをセット", on_click=set_alarm, use_container_width=True):
            pass
    with col2:
        if st.button("アラームを停止", on_click=stop_alarm, use_container_width=True):
            pass

    # メイン表示エリア
    st.metric("設定時刻", st.session_state.alarm_time.strftime("%H:%M"))

    st.markdown("---")

    # アラームのロジック
    while True:
        current_time = datetime.datetime.now().time()
        current_time_placeholder.markdown(f"### 現在時刻: **{current_time.strftime('%H:%M:%S')}**")

        if st.session_state.alarm_on and not st.session_state.alarm_triggered:
            # 時と分が一致するかチェック
            if current_time.hour == st.session_state.alarm_time.hour and \
               current_time.minute == st.session_state.alarm_time.minute:
                
                # アラーム作動
                st.session_state.alarm_triggered = True
                st.balloons()
                play_sound()
                
        # 1秒ごとに更新
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
