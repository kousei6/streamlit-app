import streamlit as st
import random

# --- 絵文字データ ---
# Unicode Consortium の最新版から人気のあるものを抜粋
EMOJIS = [
    "😀", "😂", "🤣", "😊", "😇", "😉", "😌", "😍", "🥰", "😘",
    "😗", "😋", "😜", "🤪", "😝", "😛", "🤑", "🤗", "🤭", "🤫",
    "🤔", "😬", "😮", "🤥", "🤤", "😴", "🤧", "😷", "🤒", "🤕",
    "🤯", "🤠", "🥳", "😎", "🤓", "🧐", "😮‍💨", "😩", "😫", "😡",
    "😠", "🤬", "🤯", "🥶", "😱", "😨", "😰", "😥", "😢", "😭",
    "🤯", "🥳", "😎", "🤓", "🧐", "😮‍💨", "😩", "😫", "😡", "😠",
    "🤬", "🤯", "🥶", "😱", "😨", "😰", "😥", "😢", "😭", "🤯",
    "🥳", "😎", "🤓", "🧐", "😮‍💨", "😩", "😫", "😡", "😠", "🤬",
    "🥺", "😳", "🤯", "🥳", "😎", "🤓", "🧐", "😮‍💨", "😩", "😫",
    "😡", "😠", "🤬", "🥺", "😳", "🥳", "😎", "🤓", "🧐", "😮‍💨",
    "😩", "😫", "😡", "😠", "🤬", "🥺", "😳", "😱", "😨", "😰",
    "😥", "😢", "😭", "😮‍💨", "😩", "😫", "😡", "😠", "🤬", "🥺",
    "😳", "😱", "😨", "😰", "😥", "😢", "😭", "🤯", "🥳", "😎",
    "🤓", "🧐", "😮‍💨", "😩", "😫", "😡", "😠", "🤬", "🥺", "😳",
    "😱", "😨", "😰", "😥", "😢", "😭", "🤯", "🥳", "😎", "🤓",
    "🧐", "😮‍💨", "😩", "😫", "😡", "😠", "🤬", "🥺", "😳", "🤯",
    "🥳", "😎", "🤓", "🧐", "😮‍💨", "😩", "😫", "😡", "😠", "🤬",
]

def get_random_emoji():
    """
    EMOJISリストからランダムに1つの絵文字を返す関数
    """
    return random.choice(EMOJIS)

# --- Streamlitアプリのメイン関数 ---
def main():
    st.set_page_config(page_title="RandomEmoji", layout="centered")

    st.title("🎲 Random Emoji Generator")
    st.markdown("---")

    # セッションステートに現在の絵文字を保存
    if 'current_emoji' not in st.session_state:
        st.session_state.current_emoji = get_random_emoji()

    # 「新しい絵文字を生成」ボタン
    if st.button("新しい絵文字を生成"):
        st.session_state.current_emoji = get_random_emoji()
        st.rerun()

    # 中央に絵文字を大きく表示
    st.markdown(
        f"<h1 style='text-align: center; font-size: 200px;'>{st.session_state.current_emoji}</h1>",
        unsafe_allow_html=True
    )
    
    st.markdown(
        "<p style='text-align: center;'>ボタンを押すと、新しい絵文字がランダムに表示されます。</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
