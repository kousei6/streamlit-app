import streamlit as st
from googletrans import Translator, LANGUAGES

# Translatorクラスのインスタンスを作成
translator = Translator()

st.set_page_config(
    page_title="Translator",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Translator")
st.write("テキストを別の言語に翻訳します。")

# 1. 翻訳元のテキスト入力
input_text = st.text_area(
    "翻訳したいテキストを入力してください。",
    height=200,
    placeholder="例: Hello, Streamlit!"
)

# 2. 翻訳元の言語と翻訳先の言語を選択
col1, col2 = st.columns(2)

with col1:
    # `googletrans.LANGUAGES`から言語リストを取得
    source_lang_name = st.selectbox(
        "翻訳元の言語",
        list(LANGUAGES.values()),
        index=list(LANGUAGES.keys()).index("en")
    )
    # 選択された言語名から言語コードを取得
    source_lang_code = [key for key, value in LANGUAGES.items() if value == source_lang_name][0]
    
with col2:
    target_lang_name = st.selectbox(
        "翻訳先の言語",
        list(LANGUAGES.values()),
        index=list(LANGUAGES.keys()).index("ja")
    )
    # 選択された言語名から言語コードを取得
    target_lang_code = [key for key, value in LANGUAGES.items() if value == target_lang_name][0]

# 3. 翻訳実行ボタン
if st.button("翻訳する"):
    if not input_text:
        st.warning("テキストを入力してください。")
    else:
        with st.spinner("翻訳中..."):
            try:
                # 翻訳を実行
                translation = translator.translate(
                    input_text,
                    src=source_lang_code,
                    dest=target_lang_code
                )
                
                st.markdown("---")
                st.subheader("翻訳結果")
                st.success(translation.text)

            except Exception as e:
                st.error(f"翻訳中にエラーが発生しました: {e}")
                st.warning("ネットワーク接続を確認するか、しばらくしてからもう一度お試しください。")
