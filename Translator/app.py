import streamlit as st
from deep_translator import GoogleTranslator

# Streamlit ページ設定
st.set_page_config(
    page_title="Translator",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Translator")
st.write("テキストを別の言語に翻訳します。")

# deep-translatorで対応している言語一覧を取得
translator = GoogleTranslator()
supported_langs = translator.get_supported_languages(as_dict=True)
# 辞書の形: {"english": "en", "japanese": "ja", ...}

# 1. 翻訳元のテキスト入力
input_text = st.text_area(
    "翻訳したいテキストを入力してください。",
    height=200,
    placeholder="例: Hello, Streamlit!"
)

# 2. 翻訳元の言語と翻訳先の言語を選択
col1, col2 = st.columns(2)

with col1:
    source_lang_name = st.selectbox(
        "翻訳元の言語",
        list(supported_langs.keys()),
        index=list(supported_langs.values()).index("en")  # 初期値は英語
    )
    source_lang_code = supported_langs[source_lang_name]

with col2:
    target_lang_name = st.selectbox(
        "翻訳先の言語",
        list(supported_langs.keys()),
        index=list(supported_langs.values()).index("ja")  # 初期値は日本語
    )
    target_lang_code = supported_langs[target_lang_name]

# 3. 翻訳実行ボタン
if st.button("翻訳する"):
    if not input_text:
        st.warning("テキストを入力してください。")
    else:
        with st.spinner("翻訳中..."):
            try:
                translation = GoogleTranslator(
                    source=source_lang_code,
                    target=target_lang_code
                ).translate(input_text)

                st.markdown("---")
                st.subheader("翻訳結果")
                st.success(translation)

            except Exception as e:
                st.error(f"翻訳中にエラーが発生しました: {e}")
                st.warning("ネットワーク接続を確認するか、しばらくしてからもう一度お試しください。")
