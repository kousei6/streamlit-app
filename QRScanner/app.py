import streamlit as st
from PIL import Image
import io
import pyzbar.pyzbar as pyzbar

st.set_page_config(
    page_title="QR Code Scanner",
    page_icon="📷",
    layout="centered"
)

st.title("📷 QR Code Scanner")
st.write("画像ファイル（PNG, JPEGなど）をアップロードして、QRコードを読み取ります。")

st.info("このアプリには`Pillow`と`pyzbar`ライブラリが必要です。`pip install Pillow pyzbar`でインストールしてください。")

uploaded_file = st.file_uploader("ここに画像ファイルをドラッグ＆ドロップ、またはクリックしてアップロードしてください。", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # ファイルを画像として読み込み
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="アップロードされた画像", use_column_width=True)
        st.write("")
        st.write("### 読み取り結果")

        # QRコードをデコード
        decoded_objects = pyzbar.decode(image)
        
        if decoded_objects:
            for obj in decoded_objects:
                st.success(f"**タイプ:** {obj.type}")
                st.success(f"**データ:** `{obj.data.decode('utf-8')}`")
        else:
            st.warning("画像からQRコードを検出できませんでした。")
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
