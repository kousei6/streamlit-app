
# qr-code-generation

## 使用している主な技術

* **Python**: プログラミング言語
* **Streamlit**: Webアプリケーションフレームワーク
* **qrcode**: QRコード生成ライブラリ
* **Pillow (PIL)**: 画像処理ライブラリ

## プロジェクトの概要

このプロジェクトは、Webブラウザ上で動作するシンプルなQRコード生成アプリケーションです。ユーザーが入力フィールドにテキストやURLを入力すると、瞬時に対応するQRコード画像が生成され、画面に表示されます。生成されたQRコード画像はPNG形式でダウンロードすることも可能です。Webサイトへのリンク共有や、オフラインでの情報提供などに活用できます。

## 必要な環境変数やコマンド一覧

特に環境変数の設定は不要です。

アプリケーションを起動するには、プロジェクトのルートディレクトリで以下のコマンドを実行します。

```bash
streamlit run app.py
```

## ディレクトリ構成

```
.
├── app.py          # Streamlitアプリケーションのメインファイル
├── README.md       # このREADMEファイル
└── requirements.txt  # プロジェクトの依存関係を記述したファイル
```

## 開発環境の構築方法

1.  **Pythonのインストール**:
    Python 3.7以上のバージョンがインストールされていることを確認してください。
    公式Webサイト: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **仮想環境の作成とアクティベート (推奨)**:
    プロジェクトの依存関係を隔離するために仮想環境を使用することをお勧めします。

    ```bash
    python -m venv venv
    # Windowsの場合
    .\venv\Scripts\activate
    # macOS/Linuxの場合
    source venv/bin/activate
    ```

3.  **必要なライブラリのインストール**:
    仮想環境をアクティベートした後、`requirements.txt` に記述されている必要なライブラリをインストールします。

    ```bash
    pip install -r requirements.txt
    ```

これで開発環境の構築は完了です。

## トラブルシューティング

* **`streamlit` コマンドが見つからない**:
    `pip install streamlit` が正しく実行されているか確認してください。仮想環境を使用している場合は、仮想環境がアクティベートされていることを確認してください。

* **アプリケーションが起動しない、またはエラーが発生する**:
    ターミナルに表示されるエラーメッセージを確認してください。
    * Pythonのバージョンが要件（3.7以上）を満たしているか確認してください。
    * すべての依存関係が `pip install -r requirements.txt` で正しくインストールされているか確認してください。
    * `app.py` ファイルの構文エラーがないか確認してください。

* **QRコードが表示されない、またはダウンロードボタンが表示されない**:
    「QRコードにしたい内容」のテキストエリアに何も入力されていない状態で「QRコードを生成」ボタンを押していませんか？何かテキストを入力してから再試行してください。

* **`ModuleNotFoundError: No module named 'qrcode'` または `No module named 'PIL'`**:
    `requirements.txt` に記載されている `qrcode` および `Pillow` ライブラリが正しくインストールされているか確認してください。`pip install -r requirements.txt` を再度実行してみてください。

* **`TypeError: a bytes-like object is required, not 'PilImage'` が表示される**:
    このエラーは、`st.image()` 関数にPIL (Pillow) の画像オブジェクトを直接渡している場合に発生します。Streamlitは通常、画像データをバイト形式で期待します。提供されたコードでは、`PIL.Image.Image` オブジェクトをPNG形式のバイトデータに変換してから`st.image()`に渡すように修正されています。この修正が正しく適用されているか確認してください。

* **`UnboundLocalError: local variable 'byte_im' referenced before assignment` が表示される**:
    このエラーは、QRコードのバイトデータ (`byte_im` など) が生成される前に、`st.image()` や `st.download_button()` がその変数を参照しようとした場合に発生します。最新のコードでは、QRコード生成処理と画像表示・ダウンロードボタンの表示ロジックをセッションステート (`st.session_state.qr_byte_im`) を介して制御することで、この問題が解決されています。コードが最新版に更新されているか確認してください。
