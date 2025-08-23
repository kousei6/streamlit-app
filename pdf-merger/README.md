# pdf-merger

このアプリケーションは、複数のPDFファイルをアップロードして結合し、新しい一つのPDFファイルとしてダウンロードできるシンプルなWebツールです。PythonとStreamlitを利用して開発されています。

---

### 使用している主な技術

* **Python**: バックエンドのロジックとファイル処理に使用します。
* **Streamlit**: 直感的で使いやすいWebインターフェースを構築するために使用します。
* **PyPDF2**: PDFファイルの結合処理（読み込み、書き込み、ページの追加など）を行います。
* **PyCryptodome**: PyPDF2がPDFの暗号化や復号化を処理する際に必要となる、暗号化関連の依存ライブラリです。

---

### プロジェクトの概要

PDFファイルの結合は、様々な業務やプライベートで頻繁に必要となる作業です。本アプリケーションは、ユーザーがブラウザ上で簡単に複数のPDFファイルを選択し、ボタン一つでそれらを結合できるようなシンプルなUIを提供します。ローカル環境で手軽に利用できるため、外部サービスへのファイルアップロードに抵抗がある場合にも安心して使用できます。

---

### 必要な環境変数やコマンド一覧

特に環境変数の設定は不要です。

**必要なコマンド:**

1.  **ライブラリのインストール:**
    ```bash
    pip install streamlit PyPDF2 pycryptodome
    ```
2.  **アプリケーションの実行:**
    ```bash
    streamlit run pdf_merger_app.py
    ```

---

### ディレクトリ構成

```
.
├── pdf_merger_app.py  # アプリケーションのメインコード
└── README.md          # この説明ファイル
```

---

### 開発環境の構築方法

1.  **Pythonのインストール:**
    まず、お使いのシステムにPythonがインストールされていることを確認してください。もしインストールされていない場合は、[Python公式サイト](https://www.python.org/downloads/) からダウンロードしてインストールしてください。

2.  **仮想環境の作成（推奨）:**
    プロジェクトごとに仮想環境を作成することをお勧めします。これにより、プロジェクトの依存関係がシステム全体のPython環境に影響を与えることを防げます。
    ```bash
    python -m venv venv
    ```

3.  **仮想環境のアクティベート:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **必要なライブラリのインストール:**
    仮想環境をアクティベートした後、上記の「必要な環境変数やコマンド一覧」セクションに記載されているコマンドを実行して、必要なライブラリをインストールします。
    ```bash
    pip install streamlit PyPDF2 pycryptodome
    ```

5.  **アプリケーションコードの配置:**
    `pdf_merger_app.py` ファイルを任意のディレクトリに保存します。

6.  **アプリケーションの実行:**
    保存したディレクトリに移動し、以下のコマンドでアプリケーションを起動します。
    ```bash
    streamlit run pdf_merger_app.py
    ```
    コマンド実行後、Webブラウザが自動的に開き、アプリケーションが表示されます。

---

### トラブルシューティング

* **`ModuleNotFoundError: No module named 'PyPDF2'` または `ModuleNotFoundError: No module named 'streamlit'`:**
    * 原因: 必要なライブラリがインストールされていません。
    * 解決策: 仮想環境がアクティベートされていることを確認し、`pip install streamlit PyPDF2 pycryptodome` を実行してください。

* **`DependencyError: PyCryptodome is required for AES algorithm`:**
    * 原因: PDFファイルの結合に際して、PyPDF2が暗号化されたPDFを処理しようとしていますが、そのための依存ライブラリである`PyCryptodome`が不足しています。
    * 解決策: `pip install pycryptodome` を実行して、`PyCryptodome` をインストールしてください。

* **`streamlit run` コマンドが見つからない:**
    * 原因: Streamlitが正しくインストールされていないか、PATHが通っていない可能性があります。
    * 解決策: 仮想環境がアクティベートされているか確認し、`pip install streamlit` を再度実行してみてください。

---
