import os
import streamlit as st
import PyPDF2
from io import BytesIO

def extract_text_from_pdf(uploaded_file):
    """
    アップロードされたPDFファイルからテキストを抽出する

    Args:
        uploaded_file (streamlit.runtime.uploaded_file_manager.UploadedFile):
            Streamlitのファイルアップローダーで取得したファイルオブジェクト。

    Returns:
        str: 抽出されたテキスト。エラーが発生した場合はエラーメッセージ。
    """
    try:
        # BytesIOオブジェクトとしてPDFデータをPyPDF2に渡す
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() or "" # extract_textがNoneを返す場合があるため空文字列を結合
        return text
    except PyPDF2.errors.PdfReadError:
        return "エラー: PDFファイルが破損しているか、正しく読み込めませんでした。"
    except Exception as e:
        return f"予期せぬエラーが発生しました: {e}"

def main():
    st.set_page_config(page_title="PDFテキスト抽出アプリ", layout="centered")
    st.title("PDFテキスト抽出アプリ")
    st.markdown("PDFファイルからテキストを抽出し、表示・ダウンロードします。")

    uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

    if uploaded_file is not None:
        st.success(f"ファイル '{uploaded_file.name}' がアップロードされました。")

        # プログレスバーを表示
        with st.spinner("テキストを抽出中..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        if extracted_text.startswith("エラー:"):
            st.error(extracted_text)
        else:
            if not extracted_text.strip():
                st.warning("このPDFからはテキストがほとんど抽出できませんでした。画像ベースのPDFである可能性があります。")
            else:
                st.subheader("抽出されたテキスト:")
                # 抽出されたテキストを表示 (高さを調整可能なテキストエリア)
                st.text_area("テキスト内容", extracted_text, height=400)

                # テキストファイルをダウンロードするボタン
                st.download_button(
                    label="テキストをダウンロード",
                    data=extracted_text,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}_extracted.txt",
                    mime="text/plain"
                )

                st.info("抽出されたテキストは、PDF内の文字情報に基づいています。画像として埋め込まれたテキストは抽出されません。")
    
    st.markdown("---")
    st.markdown("このアプリは、PyPDF2ライブラリを使用してPDFからテキストを抽出します。")

if __name__ == "__main__":
    main()
