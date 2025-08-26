import streamlit as st
import re

def evaluate_password_strength(password):
    """
    Evaluates the strength of a password based on several criteria.
    Returns a score and a list of feedback messages.
    """
    score = 0
    feedback = []

    # Rule 1: Length
    if len(password) >= 12:
        score += 2
        feedback.append("✅ 長さは12文字以上です。")
    elif len(password) >= 8:
        score += 1
        feedback.append("✔️ 長さは8文字以上です。")
    else:
        feedback.append("❌ 長さが8文字未満です。")
        
    # Rule 2: Contains uppercase letters
    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append("✅ 大文字が含まれています。")
    else:
        feedback.append("❌ 大文字を含めてください。")
        
    # Rule 3: Contains lowercase letters
    if re.search(r'[a-z]', password):
        score += 1
        feedback.append("✅ 小文字が含まれています。")
    else:
        feedback.append("❌ 小文字を含めてください。")
    
    # Rule 4: Contains numbers
    if re.search(r'[0-9]', password):
        score += 1
        feedback.append("✅ 数字が含まれています。")
    else:
        feedback.append("❌ 数字を含めてください。")
        
    # Rule 5: Contains symbols
    if re.search(r'[!@#$%^&*()_+.,<>/?;:\'\"\\|`~\[\]{}()]', password):
        score += 1
        feedback.append("✅ 記号が含まれています。")
    else:
        feedback.append("❌ 記号を含めてください。")

    return score, feedback

def get_strength_level(score):
    """
    Maps a score to a strength level.
    """
    if score >= 5:
        return "非常に強力", "green"
    elif score >= 3:
        return "強力", "blue"
    elif score >= 1:
        return "中程度", "orange"
    else:
        return "弱い", "red"

# --- Streamlit UI ---

st.set_page_config(page_title="PasswordStrength", layout="centered")

st.title("🔒パスワード強度チェッカー")

st.markdown(
    """
    パスワードを入力して、そのセキュリティ強度を評価します。
    """
)

# Use st.text_input with type="password" to hide the input characters
password_input = st.text_input("パスワードを入力", type="password")

if password_input:
    score, feedback = evaluate_password_strength(password_input)
    strength, color = get_strength_level(score)
    
    st.subheader("評価結果")
    st.markdown(f"**強度:** <span style='color:{color}; font-size: 24px;'>{strength}</span>", unsafe_allow_html=True)

    st.subheader("改善のためのフィードバック")
    for item in feedback:
        st.markdown(f"- {item}")
        
st.markdown("---")
st.markdown("Created with [Streamlit](https://streamlit.io/)")
