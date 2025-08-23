# word-count

## 文字数カウントアプリ
このアプリケーションは、StreamlitとPythonを使用して構築されたシンプルな文字数カウントツールです。入力されたテキストの文字数（スペース・改行含む/除く）、単語数、および行数をカウントします。

**機能**

・文字数カウント: テキスト内のすべての文字（スペースや改行を含む）をカウントします。

・文字数カウント (スペース・改行除く): テキスト内のスペースや改行を除いた文字数をカウントします。

・単語数カウント: テキスト内の単語数をカウントします。

・行数カウント: テキスト内の行数をカウントします。

・ボタン操作: 「カウント」ボタンをクリックすることで、明示的にカウントを実行します。

**必要なもの**

・Python 3.7以上

・Streamlitライブラリ

**セットアップと実行方法**

1. リポジトリをクローンする (もしGitHubリポジトリがある場合) または、以下のコードを app.py という名前で保存します。
```
import streamlit as st

def main():
    # アプリケーションのタイトルを設定
    st.set_page_config(page_title="文字数カウント", layout="centered")
    st.title("文字数カウントアプリ")

    st.write("テキストを入力し、「カウント」ボタンを押してください。")

    # ユーザーがテキストを入力するためのテキストエリア
    # heightを調整して、より多くのテキストを表示できるようにします
    user_input = st.text_area("ここにテキストを入力...", height=250)

    # カウントを実行するためのボタン
    if st.button("カウント"):
        # 入力されたテキストが空でない場合にのみカウントを表示
        if user_input:
            # 文字数をカウント (スペースや改行も含む)
            char_count = len(user_input)

            # スペースを除いた文字数をカウント
            char_count_no_spaces = len(user_input.replace(" ", "").replace("\n", ""))

            # 単語数をカウント (空白文字で区切る)
            # 空白文字のみの入力に対応するため、strip()で前後の空白を削除してから分割
            word_count = len(user_input.split()) if user_input.strip() else 0

            # 行数をカウント (改行コードで区切る)
            # 最後の行が空の場合でもカウントされるように、splitlines()を使用
            line_count = len(user_input.splitlines())

            st.subheader("カウント結果:")
            st.metric(label="文字数 (スペース・改行含む)", value=char_count)
            st.metric(label="文字数 (スペース・改行除く)", value=char_count_no_spaces)
            st.metric(label="単語数", value=word_count)
            st.metric(label="行数", value=line_count)
        else:
            st.warning("カウントするテキストが入力されていません。")
    else:
        # ボタンが押されていない初期状態、またはテキストが入力されていない場合に表示
        st.info("テキストを入力し、「カウント」ボタンを押してください。")

if __name__ == "__main__":
    main()
```

2. Streamlitをインストールします。
まだインストールしていない場合は、以下のコマンドを実行してインストールします。
```
pip install streamlit
```
3. アプリケーションを実行します。
app.py を保存したディレクトリで、以下のコマンドを実行します。
```
streamlit run app.py
```
これにより、デフォルトのWebブラウザでアプリケーションが開きます。

**使い方**
1. ブラウザで開かれたアプリケーションの「ここにテキストを入力...」と表示されたテキストエリアに、カウントしたいテキストを入力します。

2. 「カウント」ボタンをクリックします。

3. 入力したテキストの文字数、単語数、行数が「カウント結果」セクションに表示されます。
