import streamlit as st
import random

# アプリケーションのタイトルとレイアウトを設定
st.set_page_config(page_title="RockPaperScissors", layout="centered")

def initialize_session_state():
    """
    セッションステートを初期化する関数
    """
    if "player_score" not in st.session_state:
        st.session_state.player_score = 0
    if "computer_score" not in st.session_state:
        st.session_state.computer_score = 0
    if "result" not in st.session_state:
        st.session_state.result = "下のボタンを押して勝負しよう！"
    if "player_choice" not in st.session_state:
        st.session_state.player_choice = None
    if "computer_choice" not in st.session_state:
        st.session_state.computer_choice = None

def play_game(player_choice):
    """
    ジャンケンゲームのロジックを実行する関数
    """
    choices = ["グー", "チョキ", "パー"]
    computer_choice = random.choice(choices)

    st.session_state.player_choice = player_choice
    st.session_state.computer_choice = computer_choice

    # 勝敗判定ロジック
    if player_choice == computer_choice:
        st.session_state.result = "引き分け！"
    elif (player_choice == "グー" and computer_choice == "チョキ") or \
         (player_choice == "チョキ" and computer_choice == "パー") or \
         (player_choice == "パー" and computer_choice == "グー"):
        st.session_state.result = "あなたの勝ち！🎉"
        st.session_state.player_score += 1
    else:
        st.session_state.result = "コンピュータの勝ち...😭"
        st.session_state.computer_score += 1

def reset_scores():
    """
    スコアと結果をリセットする関数
    """
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.result = "下のボタンを押して勝負しよう！"
    st.session_state.player_choice = None
    st.session_state.computer_choice = None

def main():
    """
    メインアプリケーションのロジック
    """
    initialize_session_state()

    st.title("✊✋✌️ ジャンケンゲーム")
    st.markdown("コンピュータとジャンケンで勝負しよう！")

    # スコアボード
    st.header("現在のスコア")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("あなた", st.session_state.player_score)
    with col2:
        st.metric("コンピュータ", st.session_state.computer_score)
    
    st.markdown("---")

    # プレイヤーの選択ボタン
    st.header("あなたの手を選んでください")
    col_g, col_c, col_p = st.columns(3)
    with col_g:
        st.button("✊ グー", on_click=play_game, args=("グー",), use_container_width=True)
    with col_c:
        st.button("✌️ チョキ", on_click=play_game, args=("チョキ",), use_container_width=True)
    with col_p:
        st.button("✋ パー", on_click=play_game, args=("パー",), use_container_width=True)

    st.markdown("---")
    
    # 結果表示
    st.header("結果")
    if st.session_state.player_choice:
        st.write(f"あなたが選んだ手: **{st.session_state.player_choice}**")
        st.write(f"コンピュータが選んだ手: **{st.session_state.computer_choice}**")
        st.subheader(st.session_state.result)
    else:
        st.info("まだ勝負が始まっていません。手を選んでください。")

    st.markdown("---")

    # スコアリセットボタン
    st.button("スコアをリセット", on_click=reset_scores, use_container_width=True)

if __name__ == "__main__":
    main()
