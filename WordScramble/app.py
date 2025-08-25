import streamlit as st
import random
import time

# --- ゲームの状態管理 ---
def initialize_game_state():
    """ゲームの初期状態をセッションステートに設定する"""
    # 初回ロード時、またはセッションクリア後のリロード時（ゲームオーバー後の「もう一度プレイする」を含む）
    if "word_list" not in st.session_state:
        st.session_state.word_list = ["PYTHON", "STREAMLIT", "DEVELOPER", "PROGRAMMING", "CHALLENGE", "PUZZLE", "JUPYTER"]
        st.session_state.score = 0
        st.session_state.current_word_index = 0
        st.session_state.game_over = False
        st.session_state.message = ""
        st.session_state.answer_correct = False
        st.session_state.current_input_value = "" # text_input の表示値を制御する変数
        select_new_word()
    else:
        # ゲーム続行中の通常の reruns、または「次の問題へ」が押された後の処理
        # 新しい問題に進む準備ができた場合のみ、入力フィールドとメッセージをリセット
        if st.session_state.get("prepare_next_question", False):
            st.session_state.current_input_value = "" # 入力欄をクリア
            st.session_state.message = "" # メッセージをクリア
            st.session_state.answer_correct = False # 正解フラグをリセット
            st.session_state.prepare_next_question = False # フラグをリセット
            select_new_word() # 新しい単語を選択

def select_new_word():
    """新しい単語を選択し、シャッフルしてセッションステートに保存する"""
    if st.session_state.current_word_index >= len(st.session_state.word_list):
        st.session_state.game_over = True
        return

    st.session_state.current_word = st.session_state.word_list[st.session_state.current_word_index]
    scrambled_list = list(st.session_state.current_word)
    random.shuffle(scrambled_list)
    st.session_state.scrambled_word = "".join(scrambled_list)

def check_answer_callback():
    """ユーザーの回答をチェックするコールバック関数"""
    # st.text_input の key="answer_input" の値は st.session_state.answer_input に格納される
    user_answer = st.session_state.answer_input.upper().strip()

    if user_answer == st.session_state.current_word:
        st.session_state.score += 1
        st.session_state.message = "✅ **正解！** お見事です！"
        st.session_state.answer_correct = True
    else:
        st.session_state.message = f"❌ **不正解...** もう一度考えてみましょう。"
        st.session_state.answer_correct = False
        # 不正解の場合は入力内容を保持し、再描画後も入力欄に表示されるようにする
        st.session_state.current_input_value = user_answer


def next_question_button_callback():
    """次の問題へ進むボタンが押されたときのコールバック"""
    st.session_state.current_word_index += 1
    # 次のStreamlit実行サイクルで新しい問題の準備をするためのフラグを立てる
    st.session_state.prepare_next_question = True
    st.rerun()

# --- Streamlitアプリのメイン関数 ---
def main():
    st.title("Word Scramble - 単語並び替えパズル")
    st.subheader("シャッフルされた文字を並び替えて、正しい単語を当てよう！")

    initialize_game_state()

    st.markdown("---")

    if st.session_state.game_over:
        st.success(f"🎉 **ゲームクリア！** 全問正解です！あなたのスコアは **{st.session_state.score} / {len(st.session_state.word_list)}** です。")
        if st.button("もう一度プレイする"):
            st.session_state.clear() # 全てのセッションステートをクリアしてゲームをリセット
            st.rerun()
        return

    st.markdown(f"### 問題 {st.session_state.current_word_index + 1}")
    st.markdown(f"シャッフルされた単語: **`{st.session_state.scrambled_word}`**")

    # text_input の value を st.session_state.current_input_value で制御する
    # key="answer_input" はユーザーが入力した値が格納される場所。
    # on_change で check_answer_callback を呼ぶ。
    st.text_input(
        "ここに答えを入力してください",
        key="answer_input", # ユーザーの入力値を格納するキー
        value=st.session_state.current_input_value, # この値が入力欄の初期値/現在の値を決める
        on_change=check_answer_callback,
        help="入力後、Enterキーを押してください。"
    )

    st.markdown(f"現在のスコア: {st.session_state.score}")
    st.info(st.session_state.message)

    if st.session_state.get("answer_correct"):
        # 次の問題へボタンが押されたら next_question_button_callback を呼ぶ
        st.button("次の問題へ", on_click=next_question_button_callback)

if __name__ == "__main__":
    main()
