import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time # For exponential backoff

def fetch_yahoo_news():
    """
    Fetches news headlines and their associated thumbnail images from Yahoo! Japan News.
    Returns a pandas DataFrame with titles, URLs, and image URLs.
    Implements exponential backoff for robust fetching.
    """
    url = "https://news.yahoo.co.jp/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    news_list = []
    default_image_url = "https://placehold.co/120x80/cccccc/333333?text=No+Image" # Placeholder image

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- より汎用的なセレクタ戦略 ---
            # Yahoo!ニュースの記事リンクのパターンに基づいてaタグを直接検索します。
            # これらのURLパターンは比較的安定している傾向があります。
            all_links = soup.find_all('a', href=True)
            
            processed_links = set() # 重複を避けるためのセット
            
            for a_tag in all_links:
                link = a_tag.get('href')
                title = a_tag.get_text(strip=True)
                image_url = default_image_url

                # Yahoo!ニュースの記事リンクの条件をチェック
                # リンクが有効で、タイトルがあり、かつ記事のパスパターンに一致する場合
                if link and title and \
                   ("news.yahoo.co.jp/articles/" in link or \
                    "news.yahoo.co.jp/pickup/" in link or \
                    "news.yahoo.co.jp/topics/" in link) and \
                   link not in processed_links:
                    
                    # 画像の検索:
                    # 1. リンクタグの子要素として<img>を探す
                    img_tag = a_tag.find('img')
                    
                    # 2. リンクタグの親要素や兄弟要素の近くから<img>を探す
                    if not img_tag:
                        # リンクタグの親要素をたどり、その中で<img>を探す
                        parent = a_tag.find_parent()
                        if parent:
                            img_tag = parent.find('img')
                        
                    # 3. リンクタグの兄弟要素の近くから<img>を探す (例: div.thumbnail > img)
                    if not img_tag:
                        sibling_img_wrapper = a_tag.find_previous_sibling(lambda tag: tag.name in ['div', 'span'] and tag.find('img'))
                        if sibling_img_wrapper:
                            img_tag = sibling_img_wrapper.find('img')
                        
                    if img_tag:
                        image_url = img_tag.get('data-src') or img_tag.get('src')
                        # 小さすぎる画像やbase64形式の画像を除外 (アイコンやトラッカーの可能性)
                        if image_url and (image_url.startswith('data:image') or ('width="1"' in str(img_tag))):
                             image_url = default_image_url
                        
                        # 絶対URLに変換
                        if image_url and not image_url.startswith('http'):
                            image_url = f"https://news.yahoo.co.jp{image_url}"
                        elif not image_url: # img_tagは見つかったがsrc/data-srcがない場合
                            image_url = default_image_url
                    
                    news_list.append({"title": title, "link": link, "image": image_url})
                    processed_links.add(link)
            
            if news_list:
                return pd.DataFrame(news_list)
            
            st.warning(f"試行 {attempt + 1}/{max_retries}: サイト構造が変わったか、記事が見つかりませんでした。再試行します...")
            time.sleep(2 ** attempt) # 指数バックオフ
        
        except requests.exceptions.RequestException as e:
            st.error(f"試行 {attempt + 1}/{max_retries}: ニュースの取得中にネットワークエラーが発生しました: {e}")
            time.sleep(2 ** attempt) # 指数バックオフ
        except Exception as e:
            st.error(f"試行 {attempt + 1}/{max_retries}: ニュースの処理中に予期せぬエラーが発生しました: {e}")
            time.sleep(2 ** attempt) # 指数バックオフ
        
    st.error("ニュースの取得に失敗しました。サイト構造が大幅に変更されたか、ネットワークの問題が解決しません。")
    return pd.DataFrame()

# --- Streamlit UI ---

st.set_page_config(page_title="NewsFetcher", layout="wide")

st.title("NewsFetcher: 最新ニュース見出し")

st.markdown(
    """
    このアプリは、Yahoo!ニュースから最新の見出しとサムネイル画像をリアルタイムで取得して表示します。
    「更新」ボタンをクリックして最新の情報を取得してください。
    """
)

# 手動でニュースを更新するボタン
if st.button("更新"):
    st.session_state.news_data = fetch_yahoo_news()
    st.rerun()

# セッションステートにデータがない場合、初回取得を行う
if "news_data" not in st.session_state:
    with st.spinner("ニュースを初回取得中..."):
        st.session_state.news_data = fetch_yahoo_news()

# ニュースデータを表示
if st.session_state.news_data.empty:
    st.warning("現在、見出しを取得できません。時間を置いてから再度お試しください。")
else:
    st.subheader("最新の見出し")
    for index, row in st.session_state.news_data.iterrows():
        col1, col2 = st.columns([1, 4]) # カラムの幅を調整
        
        with col1:
            st.image(row['image'], width=120, caption="") # キャプションなしで画像を表示
        
        with col2:
            st.markdown(f"**[{row['title']}]({row['link']})**")
            
        st.markdown("---") # ニュースアイテム間の区切り線
