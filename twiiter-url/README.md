# twiiter-url

以下は、あなたのコードに対応したREADMEの例です。Streamlitアプリ「Twitter(X)動画ダウンローダー」用です。


# Twitter(X) 動画ダウンローダー

このアプリは、**Twitter（現X）に投稿された動画を簡単にダウンロード**できるStreamlitアプリです。動画付きのツイートURLを入力し、ボタンをクリックするだけでローカルに保存されます。

## 使用技術

* [Python](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)（YouTube-DLのフォーク。Twitter動画のダウンロードにも対応）


## インストール方法

以下のコマンドで必要なパッケージをインストールしてください：

```bash
pip install streamlit yt-dlp
```



## 使い方

1. このPythonスクリプトを `twitter_downloader.py` などの名前で保存。
2. 以下のコマンドでアプリを起動：

```bash
streamlit run twitter_downloader.py
```

3. ブラウザが開きます。Twitter(X)の動画付きツイートURLを入力し、「ダウンロード」ボタンをクリック。
4. 同じディレクトリに `.mp4` ファイルが保存されます。



##  注意点

* 対象URLは `x.com`（旧twitter.com）のみ対応しています。
* yt-dlpライブラリの仕様変更やTwitterの仕様変更により、動作しない場合があります。
* ダウンロードした動画の利用は、著作権・利用規約を遵守してください。



## 開発者向けメモ

動画の保存形式などを変更したい場合は、以下の設定を変更してください：

```python
ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',  # 出力ファイル名の形式
    'format': 'best[ext=mp4]',       # 最高画質のMP4形式を選択
}
```



## ライセンス

このプロジェクトはMITライセンスです。自由にご利用ください。

