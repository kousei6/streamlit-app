import streamlit as st
import random

# アプリケーションのタイトルとレイアウトを設定
st.set_page_config(page_title="DiceRoller", layout="centered")

def initialize_session_state():
    """
    セッションステートを初期化する関数
    """
    if "dice_history" not in st.session_state:
        st.session_state.dice_history = []
    if "total_score" not in st.session_state:
        st.session_state.total_score = 0

def roll_dice():
    """
    サイコロを振り、出目を記録する関数
    """
    # 1から6までのランダムな整数を生成
    roll_result = random.randint(1, 6)
    
    # 履歴と合計点に加算
    st.session_state.dice_history.append(roll_result)
    st.session_state.total_score += roll_result
    st.success(f"🎲 サイコロの出目: {roll_result}")

def reset_game():
    """
    ゲームの履歴とスコアをリセットする関数
    """
    st.session_state.dice_history = []
    st.session_state.total_score = 0
    st.success("ゲームがリセットされました。")

def main():
    """
    メインアプリケーションのロジック
    """
    initialize_session_state()

    st.title("🎲 DiceRoller")
    st.markdown("ボタンをクリックしてサイコロを振ろう！")

    # サイコロを振るボタン
    st.button("サイコロを振る", on_click=roll_dice, use_container_width=True)

    st.markdown("---")

    # 結果表示セクション
    st.header("結果")
    
    if st.session_state.dice_history:
        # 現在の合計点を表示
        st.metric(label="合計点", value=st.session_state.total_score)
        
        st.subheader("履歴")
        # 履歴を列挙
        for i, roll in enumerate(st.session_state.dice_history):
            st.write(f"{i + 1}回目: **{roll}**")
    else:
        st.info("まだサイコロが振られていません。")

    st.markdown("---")
    
    # リセットボタン
    st.button("ゲームをリセット", on_click=reset_game, use_container_width=True)

if __name__ == "__main__":
    main()
