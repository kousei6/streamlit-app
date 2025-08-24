import streamlit as st
from PIL import Image
import io

def resize_image(image, width=None, height=None, resize_type="幅・高さ指定"):
    """
    画像のサイズを変更します。
    """
    original_width, original_height = image.size

    try:
        if resize_type == "幅・高さ指定":
            if width and height:
                return image.resize((width, height), Image.LANCZOS)
            elif width:
                aspect_ratio = original_height / original_width
                new_height = int(width * aspect_ratio)
                return image.resize((width, new_height), Image.LANCZOS)
            elif height:
                aspect_ratio = original_width / original_height
                new_width = int(height * aspect_ratio)
                return image.resize((new_width, height), Image.LANCZOS)
            else:
                return image # 変更なし

        elif resize_type == "パーセンテージ指定":
            if width: # widthはパーセンテージとして使用
                new_width = int(original_width * (width / 100))
                new_height = int(original_height * (width / 100))
                return image.resize((new_width, new_height), Image.LANCZOS)
            else:
                return image # 変更なし
        
    except Exception as e:
        st.error(f"画像のリサイズ中にエラーが発生しました: {e}")
        return None

st.set_page_config(
    page_title="Image Resizer",
    page_icon="📏",
    layout="centered"
)

st.title("📏 Image Resizer")
st.write("画像をアップロードして、解像度やサイズを変更します。")

st.info("このアプリには`Pillow`ライブラリが必要です。`pip install Pillow`でインストールしてください。")

# 1. 画像アップロード
uploaded_file = st.file_uploader(
    "画像をアップロードしてください。",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    try:
        # 画像をPIL形式で読み込み
        original_image = Image.open(uploaded_file)
        original_width, original_height = original_image.size

        st.subheader("元の画像情報")
        st.write(f"**ファイル名:** {uploaded_file.name}")
        st.write(f"**元のサイズ:** {original_width} x {original_height} ピクセル")
        
        # 2. リサイズ方法の選択
        st.subheader("リサイズオプション")
        resize_type = st.radio(
            "リサイズ方法を選択してください。",
            ("幅・高さ指定", "パーセンテージ指定")
        )

        resized_image = None

        if resize_type == "幅・高さ指定":
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                new_width = st.number_input("新しい幅 (px)", min_value=1, value=original_width)
            with col2:
                new_height = st.number_input("新しい高さ (px)", min_value=1, value=original_height)
            
            if st.button("リサイズを実行", key="resize_dim"):
                resized_image = resize_image(original_image, new_width, new_height, resize_type)

        elif resize_type == "パーセンテージ指定":
            st.markdown("---")
            percentage = st.slider("サイズ (パーセンテージ)", 1, 200, 100)
            
            if st.button("リサイズを実行", key="resize_perc"):
                resized_image = resize_image(original_image, percentage, None, resize_type)

        # 3. リサイズ後の画像表示とダウンロード
        if resized_image:
            st.subheader("リサイズ後の画像")
            st.write(f"**新しいサイズ:** {resized_image.width} x {resized_image.height} ピクセル")
            st.image(resized_image, caption="リサイズされた画像", use_column_width=True)
            
            # ダウンロードボタン
            img_buffer = io.BytesIO()
            resized_image.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            
            st.download_button(
                label="画像をダウンロード (PNG)",
                data=img_buffer,
                file_name=f"resized_{uploaded_file.name}",
                mime="image/png"
            )

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
