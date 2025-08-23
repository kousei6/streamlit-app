# app.py
import streamlit as st
import re
from yt_dlp import YoutubeDL
import requests
from bs4 import BeautifulSoup # bs4がインストールされていない場合は pip install beautifulsoup4 を実行してください

def get_youtube_id(url):
    """
    YouTube URLから動画IDを抽出する
    """
    # 短縮URL (youtu.be) に対応
    match = re.search(r'(?:youtube\.com/(?:watch\?v=|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)
    return None

def get_thumbnail_url(video_id, quality='maxresdefault'):
    """
    動画IDからサムネイルURLを生成する
    品質オプション: default, mqdefault, sddefault, hqdefault, maxresdefault
    """
    return f"http://img.youtube.com/vi/{video_id}/{quality}.jpg"

def get_video_title(url):
    """
    YouTube URLから動画タイトルを取得する (yt-dlpを使用)
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True, # 詳細な情報をダウンロードせず、メタデータのみ取得
        'force_generic_extractor': True, # 通常のURLとして処理
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'タイトル不明')
        except Exception as e:
            # st.warning(f"動画タイトルを取得できませんでした ({url}): {e}") # 警告が多すぎる場合はコメントアウト
            return "タイトル不明"

st.set_page_config(layout="wide", page_title="YouTubeサムネイル取得＆リスト化")
st.title("🖼️ YouTubeサムネイル一括取得＆リスト化アプリ")

st.markdown("""
YouTube動画のURLを入力して、サムネイル画像を一覧で表示します。
複数のURLを入力する場合は、改行して入力してください。
""")

# テキストエリアで複数行のURLを受け取る
youtube_urls_input = st.text_area(
    "YouTube動画のURLを入力してください（複数可、改行区切り）:",
    height=200,
    placeholder="例:\nhttps://www.youtube.com/watch?v=xxxxxxxxxxx"
)

# サムネイル品質の選択
thumbnail_quality = st.selectbox(
    "サムネイルの品質を選択してください:",
    options=['maxresdefault (最高画質)', 'hqdefault (高画質)', 'sddefault (標準画質)', 'mqdefault (中画質)', 'default (低画質)'],
    index=0 # デフォルトは最高画質
)

# 選択された品質の文字列を抽出
quality_map = {
    'maxresdefault (最高画質)': 'maxresdefault',
    'hqdefault (高画質)': 'hqdefault',
    'sddefault (標準画質)': 'sddefault',
    'mqdefault (中画質)': 'mqdefault',
    'default (低画質)': 'default'
}
selected_quality = quality_map[thumbnail_quality]

process_button = st.button("サムネイルを取得＆表示")

if process_button and youtube_urls_input:
    urls = [url.strip() for url in youtube_urls_input.split('\n') if url.strip()]

    if not urls:
        st.warning("URLが入力されていません。")
    else:
        st.subheader("取得結果")
        results_exist = False
        
        # Streamlitのカラム機能を使って2カラムで表示
        cols = st.columns(2)
        col_idx = 0

        for url in urls:
            video_id = get_youtube_id(url)
            if video_id:
                results_exist = True
                thumbnail_url = get_thumbnail_url(video_id, quality=selected_quality)
                title = get_video_title(url) # 動画タイトルを取得

                with cols[col_idx]:
                    st.markdown(f"**タイトル:** [{title}]({url})")
                    # ここを修正
                    st.image(thumbnail_url, caption=f"ID: {video_id}", use_container_width=True)
                    st.markdown(f"**サムネイルURL:** `{thumbnail_url}`")
                    st.markdown("---")
                col_idx = (col_idx + 1) % 2 # カラムを切り替える
            else:
                st.warning(f"以下のURLから有効なYouTube動画IDを抽出できませんでした: {url}")
        
        if not results_exist:
            st.info("有効なURLが見つかりませんでした。")
elif process_button and not youtube_urls_input:
    st.warning("URLを入力してください。")

st.markdown("---")
st.markdown("© 2025 YouTubeサムネイル一括取得＆リスト化アプリ")
