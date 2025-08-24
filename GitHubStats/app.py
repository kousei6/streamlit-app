import streamlit as st
import requests

# GitHub APIのベースURL
GITHUB_API_URL = "https://api.github.com/users/"

st.set_page_config(
    page_title="GitHub Stats",
    page_icon="🐙",
    layout="centered"
)

st.title("🐙 GitHub Stats")
st.write("GitHubユーザー名から公開リポジトリの情報を取得します。")

st.info("このアプリは、GitHubの公開APIを使用しています。非公開リポジトリの取得には対応していません。")

# ユーザー名入力
github_username = st.text_input("GitHubユーザー名を入力してください。", placeholder="例: streamlit")

# 実行ボタン
if st.button("リポジトリ情報を取得", type="primary"):
    if not github_username:
        st.warning("GitHubユーザー名を入力してください。")
    else:
        # APIリクエストURLの構築
        repos_url = f"{GITHUB_API_URL}{github_username}/repos"

        with st.spinner("リポジトリ情報を取得中..."):
            try:
                # GitHub APIへのGETリクエスト
                response = requests.get(repos_url)
                
                # HTTPステータスコードのチェック
                if response.status_code == 200:
                    repos_data = response.json()
                    
                    if not repos_data:
                        st.warning(f"ユーザー '{github_username}' には公開リポジトリがありません。")
                    else:
                        st.success(f"ユーザー '{github_username}' のリポジトリ一覧")
                        
                        # リポジトリ情報をループで表示
                        for repo in repos_data:
                            st.markdown(f"**[{repo['name']}]({repo['html_url']})**")
                            st.write(f"💬 説明: {repo['description'] if repo['description'] else 'なし'}")
                            st.write(f"⭐ スター: {repo['stargazers_count']} | 🍴 フォーク: {repo['forks_count']}")
                            st.write("---")
                elif response.status_code == 404:
                    st.error(f"エラー: ユーザー '{github_username}' が見つかりませんでした。")
                else:
                    st.error(f"GitHub APIへのリクエスト中にエラーが発生しました。ステータスコード: {response.status_code}")
                    st.json(response.json()) # エラーレスポンスを表示
            except requests.exceptions.RequestException as e:
                st.error(f"ネットワークエラーが発生しました: {e}")
