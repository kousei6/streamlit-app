import streamlit as st
from PIL import Image, ImageFilter
import io

def apply_filter(image, filter_name):
    """
    画像に指定されたフィルターを適用します。
    """
    if filter_name == "オリジナル":
        return image
    elif filter_name == "グレースケール":
        return image.convert("L")
    elif filter_name == "ぼかし":
        return image.filter(ImageFilter.BLUR)
    elif filter_name == "シャープ化":
        return image.filter(ImageFilter.SHARPEN)
    else:
        return image

st.set_page_config(
    page_title="Image Filter",
    page_icon="🖼️",
    layout="centered"
)

st.title("🖼️ Image Filter")
st.write("画像をアップロードして、様々なフィルターを適用してみましょう。")

st.info("このアプリには`Pillow`ライブラリが必要です。`pip install Pillow`でインストールしてください。")

# 画像アップロード
uploaded_file = st.file_uploader(
    "画像をアップロードしてください。",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    try:
        # 画像をPIL形式で読み込み
        original_image = Image.open(uploaded_file)
        
        # フィルター選択
        filter_option = st.selectbox(
            "適用するフィルターを選択してください。",
            ("オリジナル", "グレースケール", "ぼかし", "シャープ化")
        )
        
        # フィルター適用
        filtered_image = apply_filter(original_image, filter_option)

        # プレビュー表示
        st.subheader("プレビュー")
        st.image(filtered_image, caption=f"{filter_option} フィルター", use_column_width=True)

        # ダウンロードボタン
        img_buffer = io.BytesIO()
        filtered_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        st.download_button(
            label="画像をダウンロード (PNG)",
            data=img_buffer,
            file_name=f"filtered_image_{filter_option.replace(' ', '_')}.png",
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
