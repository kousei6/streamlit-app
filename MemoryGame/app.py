import streamlit as st
import random
import time

# セッションステートの初期化
if 'cards' not in st.session_state:
    st.session_state.cards = []
if 'flipped_cards' not in st.session_state:
    st.session_state.flipped_cards = []
if 'matched_cards' not in st.session_state:
    st.session_state.matched_cards = []
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'message' not in st.session_state:
    st.session_state.message = "「ゲーム開始」ボタンを押してスタート！"

def create_card_deck(num_pairs):
    """
    指定されたペア数のカードデッキを作成しシャッフルする
    """
    emojis = ["🍎", "�", "🍋", "🍉", "🍇", "🍓", "🍒", "🍑", "🍍", "🥥", "🥝", "🥑"]
    selected_emojis = random.sample(emojis, num_pairs)
    card_values = selected_emojis * 2
    random.shuffle(card_values)
    
    # カードの状態を保持するリスト
    st.session_state.cards = [
        {'value': val, 'is_flipped': False, 'is_matched': False}
        for val in card_values
    ]
    st.session_state.game_started = True
    st.session_state.message = "カードをめくってください。"
    st.session_state.flipped_cards = []
    st.session_state.matched_cards = []

def flip_card(index):
    """
    カードをめくる処理
    """
    card = st.session_state.cards[index]
    if not st.session_state.game_started: # ゲームが始まっていない場合は何もしない
        return 

    # すでにめくられている、またはマッチ済みのカードは再度めくれない
    if card['is_flipped'] or card['is_matched']:
        return

    if len(st.session_state.flipped_cards) < 2:
        card['is_flipped'] = True
        st.session_state.flipped_cards.append(index)
        
        # 2枚めくった後の判定
        if len(st.session_state.flipped_cards) == 2:
            st.session_state.message = "判定中..."
            st.rerun() # UIを更新して、めくられたカードを表示

def check_match():
    """
    めくられた2枚のカードが一致するか判定する
    """
    idx1, idx2 = st.session_state.flipped_cards
    card1 = st.session_state.cards[idx1]
    card2 = st.session_state.cards[idx2]

    if card1['value'] == card2['value']:
        st.session_state.matched_cards.extend([idx1, idx2])
        card1['is_matched'] = True
        card2['is_matched'] = True
        st.session_state.message = "ペアが揃いました！:sparkles:"
    else:
        st.session_state.message = "残念、ペアではありません。"
        time.sleep(1) # ユーザーが結果を確認できるよう1秒待つ
        card1['is_flipped'] = False
        card2['is_flipped'] = False
    
    st.session_state.flipped_cards = []

def check_win():
    """
    全カードが揃ったか判定する
    """
    if len(st.session_state.matched_cards) == len(st.session_state.cards):
        st.balloons()
        st.session_state.message = "ゲームクリア！おめでとうございます！🎉"
        st.session_state.game_started = False
        return True
    return False

# メインアプリケーションのロジック
st.title("記憶力ゲーム (Memory Game)")
st.write("同じ絵文字のペアを全て見つけてください。")

# ゲーム開始ボタン
if st.session_state.game_started:
    if st.button("リセットしてもう一度"):
        st.session_state.game_started = False
        st.rerun() # st.experimental_rerun() を st.rerun() に変更
else:
    num_pairs_choice = st.selectbox("ゲームの難易度を選択してください:", [4, 6, 8, 10], index=1, format_func=lambda x: f"{x}ペア")
    if st.button("ゲーム開始"):
        create_card_deck(num_pairs_choice)
        st.rerun() # st.experimental_rerun() を st.rerun() に変更

st.info(st.session_state.message)

# カードの表示
if st.session_state.game_started:
    # カードの数に応じて列数を調整
    num_cards = len(st.session_state.cards)
    cols_per_row = 4
    if num_cards <= 6: # 例えば、6枚以下の場合は3列に
        cols_per_row = 3
    elif num_cards <= 8: # 8枚以下の場合は4列に
        cols_per_row = 4
    else: # それ以上の場合は5列など
        cols_per_row = 5 # 必要に応じて調整

    cols = st.columns(cols_per_row) # 1行に表示するカードの列数

    for i, card in enumerate(st.session_state.cards):
        col = cols[i % cols_per_row]
        
        if card['is_matched']:
            display_text = card['value']
            button_disabled = True
        elif card['is_flipped']:
            display_text = card['value']
            button_disabled = True
        else:
            display_text = "❓"
            button_disabled = False
        
        with col:
            st.button(
                display_text,
                key=f"card_{i}",
                on_click=flip_card,
                args=(i,),
                # 2枚めくられている間は他のカードをめくれないようにする
                disabled=button_disabled or len(st.session_state.flipped_cards) == 2
            )
            
    # めくられたカードが2枚になったら判定を実行
    if len(st.session_state.flipped_cards) == 2:
        check_match()
        # 勝利判定後、ゲームが続行する場合は再描画
        if not check_win():
            st.rerun() # st.experimental_rerun() を st.rerun() に変更
