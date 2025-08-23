# pdf-text

### 使用している主な技術

* **Python**: プログラミング言語
* **Streamlit**: Webアプリケーションフレームワーク
* **PyPDF2**: PDFファイルの読み書きライブラリ
* **PyCryptodome**: PDFの暗号化/復号化処理に使用されるライブラリ

### プロジェクトの概要

このアプリは、PDFファイルから文字情報を簡単に取り出せるツールです。アップロードされたPDFからテキストを抽出し、ブラウザで確認したり、テキストファイルとしてダウンロードしたりできます。PDFの内容を手早く確認したい時や、テキストデータとして再利用したい場合に便利です。

### 必要な環境変数やコマンド一覧

特に環境変数の設定は必要ありません。

アプリを起動するには、プロジェクトのルートディレクトリで以下のコマンドを実行します。

```bash
streamlit run app.py
```

### ディレクトリ構成

```
.
├── app.py          # Streamlitアプリケーションのメインファイル
├── README.md       # このREADMEファイル
└── requirements.txt  # プロジェクトの依存関係を記述したファイル
```

### 開発環境の構築方法

1.  **Pythonのインストール**:
    Python 3.7以上のバージョンがインストールされていることを確認してください。
    公式Webサイト: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **仮想環境の作成とアクティベート (推奨)**:
    プロジェクトの依存関係を整理するために、仮想環境の使用をおすすめします。

    ```bash
    python -m venv venv
    # Windowsの場合
    .\venv\Scripts\activate
    # macOS/Linuxの場合
    source venv/bin/activate
    ```

3.  **必要なライブラリのインストール**:
    仮想環境をアクティベートしたら、`requirements.txt` にリストされている必要なライブラリをインストールします。

    ```bash
    pip install -r requirements.txt
    ```

これで開発環境の準備は完了です。

### トラブルシューティング

* **`streamlit` コマンドが見つからない**:
    `pip install streamlit` が正しく実行されているか確認してください。もし仮想環境を使っている場合は、仮想環境がアクティブになっているかどうかも確認しましょう。

* **アプリが起動しない、またはエラーが出る**:
    ターミナルに表示されるエラーメッセージを確認してください。
    * Pythonのバージョンが要件（3.7以上）を満たしていますか？
    * すべての依存関係が `pip install -r requirements.txt` できちんとインストールされていますか？
    * `app.py` ファイルに文法エラーはありませんか？

* **PDFからテキストがうまく抽出されない、または内容が空になる**:
    アップロードしたPDFが、文字情報ではなく、画像としてスキャンされたものである可能性があります。PyPDF2はPDF内に埋め込まれたテキストを抽出しますが、画像内の文字は認識できません。もし画像ベースのPDFからテキストを抽出したい場合は、Tesseract-OCRのようなOCR（光学文字認識）ツールと、それに対応するPythonライブラリ（例: `pytesseract`）が必要になりますが、このアプリの現在の機能には含まれていません。

* **`PyPDF2.errors.PdfReadError` エラーが出る**:
    これは、アップロードしたPDFファイルが破損しているか、PyPDF2がサポートしていない形式である可能性が高いです。別のPDFファイルで試すか、PDFビューアでファイルが正常に開けるかを確認してみてください。

* **予期せぬエラーが発生しました: PyCryptodome is required for AES algorithm エラーが出る**:
このエラーは、PDFファイルが暗号化されており、その復号化に必要なPyCryptodomeライブラリがインストールされていない場合に発生します。
pip install pycryptodome を実行して、ライブラリをインストールしてください。requirements.txtにpycryptodomeを追加し、pip install -r requirements.txtを再実行することをお勧めします。
