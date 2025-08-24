import streamlit as st
import random

st.set_page_config(
    page_title="Random Number Generator",
    page_icon="🎲",
    layout="centered"
)

st.title("🎲 Random Number Generator")
st.write("指定した範囲内でランダムな整数を生成します。")

# 乱数の生成範囲を入力
st.markdown("---")
st.header("生成範囲の指定")
col1, col2 = st.columns(2)

with col1:
    min_val = st.number_input("最小値", min_value=0, value=0, step=1)

with col2:
    max_val = st.number_input("最大値", min_value=min_val, value=100, step=1)

# 入力値のバリデーション
if min_val > max_val:
    st.error("エラー: 最小値は最大値以下でなければなりません。")

# 乱数生成ボタン
st.markdown("---")
if st.button("乱数を生成", type="primary"):
    if min_val <= max_val:
        # 乱数を生成
        random_number = random.randint(min_val, max_val)
        
        # 乱数生成結果を表示
        st.success(f"生成された乱数: **{random_number}**")
        
        # セッションステートに履歴を保存
        if 'history' not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append(random_number)
    else:
        st.warning("範囲を正しく設定してください。")

# 履歴表示セクション
if 'history' in st.session_state and st.session_state.history:
    st.markdown("---")
    st.header("生成履歴")
    history_list = st.session_state.history[::-1] # 最新のものを先頭に
    for i, num in enumerate(history_list):
        st.write(f"{i+1}回前: {num}")
