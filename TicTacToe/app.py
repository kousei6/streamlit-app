import streamlit as st

# セッションステートの初期化
# ユーザーがページを更新してもゲームの状態を保持するために必須です
if 'board' not in st.session_state:
    st.session_state.board = [''] * 9
if 'player' not in st.session_state:
    st.session_state.player = 'X'
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

def check_winner():
    """
    勝利条件をチェックする関数
    """
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 横
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 縦
        (0, 4, 8), (2, 4, 6)              # 斜め
    ]
    for combo in winning_combinations:
        if (st.session_state.board[combo[0]] == st.session_state.board[combo[1]] == st.session_state.board[combo[2]] != ''):
            st.session_state.winner = st.session_state.player
            st.session_state.game_over = True
            return True

    # 引き分けのチェック
    if all(cell != '' for cell in st.session_state.board):
        st.session_state.winner = '引き分け'
        st.session_state.game_over = True
        return True
    
    return False

def handle_click(index):
    """
    セルがクリックされたときの処理
    """
    if not st.session_state.game_over and st.session_state.board[index] == '':
        st.session_state.board[index] = st.session_state.player
        check_winner()
        if not st.session_state.game_over:
            st.session_state.player = 'O' if st.session_state.player == 'X' else 'X'

def reset_game():
    """
    ゲームをリセットする関数
    """
    st.session_state.board = [''] * 9
    st.session_state.player = 'X'
    st.session_state.winner = None
    st.session_state.game_over = False

# アプリケーションのメインレイアウト
st.title("〇×ゲーム")
st.write("2人のプレイヤーで遊ぶことができます。")

# 状態表示
if st.session_state.winner:
    if st.session_state.winner == '引き分け':
        st.info("ゲーム終了！引き分けです。")
    else:
        st.success(f"プレイヤー '{st.session_state.winner}' の勝利です！:tada:")
else:
    st.info(f"現在のプレイヤー: '{st.session_state.player}'")

# ゲームボードの描画
st.markdown("""
<style>
.stButton>button {
    height: 100px;
    width: 100px;
    font-size: 4em;
}
.board-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# 3x3のグリッドを作成
with st.container():
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3, col1, col2, col3, col1, col2, col3] # 9つのボタンを3つのカラムに配置するためのトリック
    
    for i in range(9):
        with cols[i]:
            st.button(
                st.session_state.board[i] if st.session_state.board[i] else ' ',
                key=i,
                on_click=handle_click,
                args=(i,),
                disabled=st.session_state.game_over or st.session_state.board[i] != ''
            )

# ゲームリセットボタン
st.markdown("---")
if st.button("ゲームをリセット", help="現在のゲームを最初からやり直します。"):
    reset_game()
    st.experimental_rerun()
