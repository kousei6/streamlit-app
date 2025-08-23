import streamlit as st
from PyPDF2 import PdfMerger
import os

st.set_page_config(layout="wide")

def merge_pdfs(pdf_files):
    """
    複数のPDFファイルを結合する関数
    """
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    output_path = "merged_output.pdf"
    merger.write(output_path)
    merger.close()
    return output_path

st.title("PDF結合アプリケーション")
st.write("複数のPDFファイルをアップロードして結合し、一つのPDFとしてダウンロードできます。")

# PDFファイルのアップロード
uploaded_files = st.file_uploader("PDFファイルをここにドラッグ＆ドロップ、またはクリックして選択してください (複数選択可)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.write("---")
    st.subheader("アップロードされたPDFファイル:")
    for file in uploaded_files:
        st.write(f"- {file.name}")

    if st.button("PDFを結合"):
        if len(uploaded_files) < 2:
            st.warning("PDFを結合するには2つ以上のファイルをアップロードしてください。")
        else:
            with st.spinner("PDFを結合中..."):
                merged_pdf_path = merge_pdfs(uploaded_files)
                st.success("PDFの結合が完了しました！")
                with open(merged_pdf_path, "rb") as f:
                    st.download_button(
                        label="結合されたPDFをダウンロード",
                        data=f.read(),
                        file_name="結合済みPDF.pdf",
                        mime="application/pdf"
                    )
                # 結合後の一時ファイルを削除
                os.remove(merged_pdf_path)

st.write("---")
st.info("このアプリケーションは、PyPDF2ライブラリを使用してPDFを処理しています。")
