import streamlit as st
import random
import string
import pyperclip

# --- Functions ---
def generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols):
    """
    Generate a random password based on the specified criteria.
    """
    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        st.warning("パスワードを生成するには、少なくとも1つの文字種を選択してください。")
        return ""

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def copy_to_clipboard(text):
    """
    Copy text to the clipboard.
    Note: This function will work only in a browser with the necessary permissions.
    It's more reliable to use JavaScript for this, but this is a simple example.
    """
    try:
        pyperclip.copy(text)
        st.success("パスワードがクリップボードにコピーされました！")
    except pyperclip.PyperclipException:
        st.error("クリップボードへのコピーに失敗しました。お使いの環境では対応していない可能性があります。")

# --- Streamlit UI ---
st.set_page_config(
    page_title="安全なパスワードジェネレーター",
    page_icon="🔑",
    layout="centered"
)

st.title("🔑 パスワードジェネレーター")
st.markdown("安全なパスワードを簡単に作成します。")

# Sidebar for options
st.sidebar.header("パスワード設定")

# Password length slider
length = st.sidebar.slider("パスワードの長さ", min_value=8, max_value=64, value=16)

# Character type checkboxes
use_uppercase = st.sidebar.checkbox("大文字 (A-Z)", value=True)
use_lowercase = st.sidebar.checkbox("小文字 (a-z)", value=True)
use_digits = st.sidebar.checkbox("数字 (0-9)", value=True)
use_symbols = st.sidebar.checkbox("記号 (!@#$)", value=True)

st.sidebar.markdown("---")
if st.sidebar.button("パスワードを生成"):
    # Generate password when button is clicked
    password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols)
    if password:
        st.subheader("生成されたパスワード")
        st.code(password, language="text")
        
        # Add a button to copy the password to the clipboard
        if st.button("パスワードをコピー"):
            copy_to_clipboard(password)

st.info("💡 ヒント: パスワードの長さを長くし、文字種を増やすほど、安全性が高まります。")
