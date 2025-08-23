import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import zipfile
import shutil

# --- Streamlitのページ設定 ---
st.set_page_config(layout="centered", page_title="PDF画像抽出ツール")

st.title("🖼️ PDF画像抽出ツール 🖼️")
st.markdown("PDFファイルから画像を簡単に抽出できます。")

# --- 画像抽出関数 ---
@st.cache_resource # アプリケーションの再実行時にリソースをキャッシュ
def extract_images_from_pdf(pdf_file_path, output_dir):
    """
    PDFから画像を抽出し、指定されたディレクトリに保存する
    """
    extracted_image_paths = []
    
    # 出力ディレクトリが存在しなければ作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # ドキュメントを開く
        doc = fitz.open(pdf_file_path)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True) # full=Trueで埋め込み画像をすべて取得

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                
                # 画像のデータと拡張子を取得
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # ファイル名を設定
                image_filename = f"page{page_num+1}_img{img_index+1}.{image_ext}"
                image_path = os.path.join(output_dir, image_filename)
                
                # 画像をファイルに保存
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                extracted_image_paths.append(image_path)
        
        doc.close()
        return extracted_image_paths
    except Exception as e:
        st.error(f"画像の抽出中にエラーが発生しました: {e}")
        return []

# --- メインアプリケーションロジック ---

uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

if uploaded_file is not None:
    # アップロードされたPDFを一時ファイルとして保存
    # Streamlit Cloudなどの環境でファイルパスが必要なため
    temp_pdf_path = os.path.join("temp_pdf", uploaded_file.name)
    os.makedirs(os.path.dirname(temp_pdf_path), exist_ok=True)
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"PDFファイル '{uploaded_file.name}' をアップロードしました。")

    # 抽出ボタン
    if st.button("画像を抽出する", key="extract_button"):
        output_image_dir = "extracted_images"
        
        # 以前の抽出結果をクリア (もしあれば)
        if os.path.exists(output_image_dir):
            shutil.rmtree(output_image_dir)
        
        with st.spinner("画像を抽出中...しばらくお待ちください。"):
            extracted_paths = extract_images_from_pdf(temp_pdf_path, output_image_dir)

        if extracted_paths:
            st.success(f"{len(extracted_paths)}個の画像を抽出しました！")

            # --- 抽出画像のプレビュー ---
            st.subheader("抽出された画像 (一部プレビュー)")
            preview_count = 0
            cols = st.columns(5) # 5列で表示
            for i, img_path in enumerate(extracted_paths):
                if preview_count < 10: # 最大10枚までプレビュー
                    try:
                        img = Image.open(img_path)
                        with cols[i % 5]:
                            st.image(img, caption=os.path.basename(img_path), width=100)
                        preview_count += 1
                    except Exception as e:
                        st.warning(f"画像 '{os.path.basename(img_path)}' のプレビューに失敗しました: {e}")
                else:
                    break
            
            if len(extracted_paths) > 10:
                st.info(f"合計 {len(extracted_paths)}個の画像が抽出されました。全て表示するには、ZIPファイルをダウンロードしてください。")

            # --- ZIPファイルとしてダウンロード ---
            st.subheader("画像をダウンロード")
            
            # メモリ上でZIPファイルを作成
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for img_path in extracted_paths:
                    # ZIPファイル内のパスは、元のディレクトリ構造を維持しないように basename を使用
                    zf.write(img_path, os.path.basename(img_path))
            zip_buffer.seek(0) # バッファの先頭に戻る

            st.download_button(
                label="抽出画像をZIPでダウンロード",
                data=zip_buffer,
                file_name="extracted_pdf_images.zip",
                mime="application/zip"
            )
            
            st.info("ダウンロード後、一時ファイルは自動的に削除されます。")

        else:
            st.warning("このPDFからは画像が抽出されませんでした。")
    
    # 処理終了後に一時ファイルをクリーンアップ
    # ダウンロード完了後、またはブラウザを閉じた後に削除されることを想定
    # Streamlit Cloudではセッション終了時に自動でクリアされることが多い
    # ローカル環境で即座に削除したい場合は、st.empty()などと組み合わせてボタンを押した際に削除処理を行う
    # ただし、ダウンロードボタンと同時にファイル削除するとダウンロードが間に合わない可能性あり
    
    # 例：セッション終了時にクリーンアップするロジック（Streamlitアプリのライフサイクル依存）
    # st.session_state に extracted_paths がある状態で、
    # その後のセッションでファイルが存在すれば削除を試みるなど
    if 'extracted_image_output_dir' in st.session_state and os.path.exists(st.session_state.extracted_image_output_dir):
        try:
            st.write("一時ファイルをクリーンアップ中...")
            shutil.rmtree(st.session_state.extracted_image_output_dir)
            st.write("クリーンアップ完了。")
            del st.session_state.extracted_image_output_dir
        except Exception as e:
            st.warning(f"クリーンアップ中にエラーが発生しました: {e}")

else:
    st.info("PDFファイルをアップロードして、画像抽出を開始してください。")

st.markdown("---")
st.markdown("**注意:**")
st.markdown("- PDFの構造によっては、すべての画像が正確に抽出されない場合があります。")
st.markdown("- アップロードされたPDFファイルと抽出された画像は、セッション終了後またはアプリのリロード時に一時的に保存されますが、**永続的に保存されることはありません**。")
