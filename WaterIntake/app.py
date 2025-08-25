import streamlit as st
import pandas as pd
from datetime import date

# アプリケーションのタイトルとレイアウトを設定
st.set_page_config(page_title="WaterIntake", layout="centered")

def initialize_session_state():
    """
    セッションステートを初期化する関数
    """
    if "total_intake" not in st.session_state:
        st.session_state.total_intake = 0
    if "target_intake" not in st.session_state:
        st.session_state.target_intake = 2000 # デフォルト目標量（2000ml）

def add_intake(amount):
    """
    指定された量の水分を合計摂取量に加算する関数
    """
    st.session_state.total_intake += amount

def set_target():
    """
    目標量を設定する関数
    """
    new_target = st.session_state.target_input
    if new_target > 0:
        st.session_state.target_intake = new_target
    else:
        st.warning("目標量は0より大きい値を設定してください。")

def reset_intake():
    """
    水分摂取量をリセットする関数
    """
    st.session_state.total_intake = 0

def main():
    """
    メインアプリケーションのロジック
    """
    initialize_session_state()

    st.title("💧 WaterIntake Tracker")
    st.markdown("一日の水分摂取量を記録しましょう。")

    # 目標設定セクション
    st.sidebar.header("目標設定")
    with st.sidebar.form(key='target_form'):
        st.number_input(
            "目標摂取量 (ml)", 
            min_value=1, 
            step=100, 
            value=st.session_state.target_intake,
            key="target_input"
        )
        set_target_button = st.form_submit_button("目標を更新", on_click=set_target)

    # 進捗表示セクション
    st.header("今日の水分摂取量")
    current_progress = st.session_state.total_intake / st.session_state.target_intake if st.session_state.target_intake > 0 else 0
    current_progress_percentage = min(current_progress, 1.0) # 100%を超えないように制御

    st.subheader(f"{st.session_state.total_intake} ml / {st.session_state.target_intake} ml")
    st.progress(current_progress_percentage)
    
    if current_progress >= 1.0:
        st.success("🎉 おめでとうございます！目標達成です！")

    st.markdown("---")

    # 摂取量記録セクション
    st.header("水分を記録")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("コップ1杯 (200ml)", on_click=add_intake, args=(200,), use_container_width=True)
    with col2:
        st.button("ボトル1本 (500ml)", on_click=add_intake, args=(500,), use_container_width=True)
    with col3:
        st.button("その他", on_click=lambda: st.session_state.update(show_custom_input=True), use_container_width=True)
    
    # カスタム入力フォーム
    if st.session_state.get("show_custom_input"):
        with st.expander("カスタム量を記録"):
            custom_amount = st.number_input("追加する量 (ml)", min_value=1, step=1, key="custom_amount_input")
            if st.button("記録", key="custom_add_btn"):
                add_intake(custom_amount)
                st.session_state.show_custom_input = False
                st.rerun()

    st.markdown("---")

    # リセットボタン
    st.button("今日の記録をリセット", on_click=reset_intake, use_container_width=True)

if __name__ == "__main__":
    main()
