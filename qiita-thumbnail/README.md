# 🖼️ 複数Qiita記事サムネイル抽出アプリ
このアプリケーションは、Streamlitを使って構築されたツールで、入力された複数のQiita記事のURLから、それぞれの記事のサムネイル画像（OGP画像またはTwitter Card画像）を抽出し、表示します。Qiita記事のサムネイルをまとめて確認したい場合に便利です。

# ✨ 機能
- URL入力: 改行区切りで複数のQiita記事のURLを入力できます。

- サムネイル抽出: 各URLからOGP画像（og:image）またはTwitter Card画像（twitter:image）のURLを抽出し、画像として表示します。

- エラーハンドリング: Qiita以外のURLや、画像が抽出できなかった場合に適切なメッセージを表示します。

- レスポンシブデザイン: Streamlitによって自動的にレスポンシブに対応し、様々な画面サイズで利用できます。

# 🛠️ 必要なライブラリ
このアプリケーションを実行するには、以下のPythonライブラリが必要です。

- streamlit

- requests

- BeautifulSoup4 (bs4)

以下のコマンドでインストールできます。
```
pip install streamlit requests beautifulsoup4
```
# 🚀 使い方
1. 上記の手順で必要なライブラリをインストールします。

2. 提供されたPythonコードをqiita_thumbnail_extractor.pyなどのファイル名で保存します。

3. ターミナルまたはコマンドプロンプトで、ファイルが保存されているディレクトリに移動し、以下のコマンドを実行します。
```
streamlit run qiita_thumbnail_extractor.py
```
4. Webブラウザが自動的に起動し、アプリケーションが表示されます。

# 💡 アプリケーションの操作
1. Qiita記事のURLを1行に1つずつ入力してください と表示されたテキストエリアに、サムネイルを抽出したいQiita記事のURLを貼り付けます。複数のURLを入力する場合は、各URLを改行して入力してください。

- 例:
```
https://qiita.com/yamamoto_kenta/items/8a34d7d0a2f4a5a5f6e8
https://qiita.com/kazukazu_pon/items/bb19782414704b2a30d5
https://qiita.com/taniokahikaru/items/7fb81837077a280c7d5c
```
2. 「サムネイルを抽出」 ボタンをクリックします。

3. 各URLに対して、抽出されたサムネイル画像と画像URLが表示されます。画像が見つからなかった場合やURLが無効な場合は、その旨が通知されます。

# 📝 コードの概要
- get_qiita_og_image_url(qiita_url): 指定されたQiitaのURLからHTMLコンテンツを取得し、og:imageまたはtwitter:imageメタタグを解析してサムネイル画像のURLを返します。

- Streamlit UI: テキストエリアでURLを受け取り、「サムネイルを抽出」ボタンで処理を開始します。結果はst.imageで表示されます。

- カスタムCSS: アプリケーションのテキストエリアやボタンのスタイルを調整するためのインラインCSSが含まれています。
