import streamlit as st
from langdetect import detect, LangDetectException

# セッションステートの初期化
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""
if 'detected_language' not in st.session_state:
    st.session_state.detected_language = None

def detect_language(text):
    """
    入力されたテキストの言語を判定する
    """
    if not text.strip():
        return None
    try:
        lang_code = detect(text)
        return lang_code
    except LangDetectException:
        return "判定不能"
    
def get_language_name(lang_code):
    """
    言語コードに対応する言語名を返す（簡易版）
    より多くの言語に対応するには、外部ライブラリや辞書が必要
    """
    lang_names = {
        'en': '英語 (English)',
        'ja': '日本語 (Japanese)',
        'zh-cn': '中国語 (簡体字)',
        'es': 'スペイン語 (Spanish)',
        'fr': 'フランス語 (French)',
        'de': 'ドイツ語 (German)',
        'ko': '韓国語 (Korean)',
        'ru': 'ロシア語 (Russian)',
        'it': 'イタリア語 (Italian)',
        'pt': 'ポルトガル語 (Portuguese)',
        'ar': 'アラビア語 (Arabic)',
        'hi': 'ヒンディー語 (Hindi)',
        'th': 'タイ語 (Thai)',
        'vi': 'ベトナム語 (Vietnamese)',
        'id': 'インドネシア語 (Indonesian)',
        'tr': 'トルコ語 (Turkish)',
        'nl': 'オランダ語 (Dutch)'
    }
    return lang_names.get(lang_code, f"不明な言語コード ({lang_code})")


# アプリケーションのメインレイアウト
st.title("言語判別アプリ 🌐")
st.write("テキストボックスに文章を入力してください。入力された言語を自動で判別します。")
st.markdown("---")

# テキスト入力エリア
user_text = st.text_area(
    "ここにテキストを入力してください:",
    height=200,
    placeholder="例：こんにちは、元気ですか？"
)

# 言語判定ボタン
if st.button("言語を判別"):
    if user_text:
        st.session_state.detected_language = detect_language(user_text)
    else:
        st.session_state.detected_language = None
    
# 判定結果の表示
if st.session_state.detected_language:
    st.markdown("---")
    st.subheader("判定結果")
    if st.session_state.detected_language == "判定不能":
        st.error("入力されたテキストからは言語を判別できませんでした。より長い文章を入力してみてください。")
    else:
        lang_name = get_language_name(st.session_state.detected_language)
        st.success(f"このテキストは **{lang_name}** です。")
        st.markdown(f"**言語コード:** `{st.session_state.detected_language}`")
