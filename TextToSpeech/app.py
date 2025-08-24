import streamlit as st
from gtts import gTTS
import io
import os

st.set_page_config(
    page_title="Text-to-Speech",
    page_icon="🔊",
    layout="centered"
)

st.title("🔊 Text-to-Speech")
st.write("入力されたテキストを音声に変換して再生します。")

st.info("このアプリには`gTTS`ライブラリが必要です。`pip install gTTS`でインストールしてください。")

# 1. テキスト入力エリア
text_input = st.text_area(
    "ここに読み上げたいテキストを入力してください。",
    height=200,
    placeholder="例: StreamlitはPythonで簡単にWebアプリを作成できるフレームワークです。"
)

# 2. 言語選択
lang = st.selectbox(
    "言語を選択してください。",
    options=["ja", "en", "es", "fr", "de", "zh-CN", "ko"],
    format_func=lambda x: {
        "ja": "日本語",
        "en": "英語",
        "es": "スペイン語",
        "fr": "フランス語",
        "de": "ドイツ語",
        "zh-CN": "中国語",
        "ko": "韓国語"
    }[x]
)

# 3. 実行ボタン
if st.button("音声生成"):
    if text_input:
        with st.spinner("音声を生成中..."):
            try:
                # gTTSで音声ファイルを生成
                tts = gTTS(text=text_input, lang=lang)
                
                # 音声データをメモリに保存
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                
                st.subheader("再生")
                # Streamlitのオーディオウィジェットで再生
                st.audio(audio_bytes, format="audio/mp3")

                # ダウンロードボタン
                st.download_button(
                    label="音声をダウンロード (MP3)",
                    data=audio_bytes,
                    file_name="speech.mp3",
                    mime="audio/mp3"
                )

            except Exception as e:
                st.error(f"音声生成中にエラーが発生しました: {e}")
                st.warning("入力されたテキストや選択された言語が正しくない可能性があります。")
    else:
        st.warning("テキストを入力してください。")
