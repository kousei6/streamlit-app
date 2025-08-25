import streamlit as st
import random
import time

# --- ゲームの状態管理 ---
def initialize_game_state():
    """ゲームの初期状態をセッションステートに設定する"""
    if "word" not in st.session_state or st.session_state.game_over:
        st.session_state.game_over = False
        st.session_state.word_list = ["PYTHON", "STREAMLIT", "DEVELOPER", "HANGMAN", "CODING", "ENGINEER", "PROGRAMMING"]
        st.session_state.word = random.choice(st.session_state.word_list).upper()
        st.session_state.guessed_letters = set()
        st.session_state.incorrect_guesses = 0
        st.session_state.max_incorrect = 6  # 描画するパーツの数
        st.session_state.game_status = ""

# --- UIコンポーネント ---
def display_hangman(incorrect_count):
    """間違った回数に応じてハングマンの絵を表示する"""
    stages = [
        # 0: 初期状態
        """
           -----
           |   |
               |
               |
               |
               |
        """,
        # 1: 頭
        """
           -----
           |   |
           O   |
               |
               |
               |
        """,
        # 2: 体
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        """,
        # 3: 片腕
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        """,
        # 4: 両腕
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        """,
        # 5: 片足
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        """,
        # 6: 両足 (ゲームオーバー)
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        """
    ]
    # incorrect_count が stages リストの範囲を超えないように調整
    # これが今回のエラー修正の核心です。
    if incorrect_count >= len(stages):
        incorrect_count = len(stages) - 1
        
    st.text(stages[incorrect_count])

def display_word():
    """単語の現在の状態（_ と文字）を表示する"""
    display = ""
    for letter in st.session_state.word:
        if letter in st.session_state.guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    st.markdown(f"## {display}")

# --- ゲームロジック ---
def handle_guess():
    """ユーザーの推測を処理する"""
    guess = st.session_state.guess_input.strip().upper()
    if not guess.isalpha() or len(guess) != 1:
        st.session_state.game_status = "❌ 無効な入力です。アルファベット一文字を入力してください。"
        return

    if guess in st.session_state.guessed_letters:
        st.session_state.game_status = f"🤔 '{guess}'は既に推測済みです。別の文字をどうぞ。"
        return

    st.session_state.guessed_letters.add(guess)
    st.session_state.game_status = ""

    if guess not in st.session_state.word:
        st.session_state.incorrect_guesses += 1
        st.session_state.game_status = f"❌ 残念！'{guess}'は単語に含まれていません。"
    else:
        st.session_state.game_status = f"✅ 正解！'{guess}'は単語に含まれていました。"

    # 入力フィールドをクリア
    st.session_state.guess_input = ""

def check_game_status():
    """ゲームの勝利または敗北を判定する"""
    word_set = set(st.session_state.word)
    if word_set.issubset(st.session_state.guessed_letters):
        st.balloons()
        st.success(f"🎉 **おめでとうございます！勝利です！** 単語は '{st.session_state.word}' でした。")
        st.session_state.game_over = True
    elif st.session_state.incorrect_guesses >= st.session_state.max_incorrect:
        st.error(f"💀 **ゲームオーバー...** 正解は '{st.session_state.word}' でした。")
        st.session_state.game_over = True

# --- Streamlitアプリのメイン関数 ---
def main():
    st.title("ハングマンゲーム")
    st.subheader("単語を当てて、ハングマンを救おう！")

    # ゲームの初期化
    initialize_game_state()

    st.markdown("---")

    # ゲームの進行状況を表示
    display_hangman(st.session_state.incorrect_guesses)
    display_word()

    st.write(f"間違えた回数: {st.session_state.incorrect_guesses} / {st.session_state.max_incorrect}")
    st.write(f"推測済みの文字: {', '.join(sorted(list(st.session_state.guessed_letters)))}")

    # ゲームが進行中の場合のみ、入力ウィジェットを表示
    if not st.session_state.game_over:
        st.markdown("---")
        st.text_input(
            "アルファベットを推測してください",
            max_chars=1,
            key="guess_input",
            on_change=handle_guess,
            help="入力後、Enterキーを押してください。"
        )
        st.info(st.session_state.game_status)
    
    # ゲーム終了後の再開ボタン
    check_game_status()
    if st.session_state.game_over:
        if st.button("もう一度プレイする"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
