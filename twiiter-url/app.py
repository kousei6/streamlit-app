import streamlit as st
import yt_dlp

st.title("Twitter(X) 動画ダウンローダー")

url = st.text_input("動画付きツイートのURLを入力してください")

if st.button("ダウンロード"):
    if "x.com" not in url:
        st.error("有効なTwitter(X)のURLを入力してください")
    else:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'best[ext=mp4]',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            st.success("ダウンロード成功！同じディレクトリに保存されました。")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
