import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

def generate_qr_code(data, box_size=10, border=4):
    """
    与えられたデータからQRコード画像を生成する。

    Args:
        data (str): QRコードにエンコードするテキストまたはURL。
        box_size (int): QRコードの各ボックス（ピクセル）のサイズ。
        border (int): QRコードの周囲のボーダーの太さ（ボックス単位）。

    Returns:
        PIL.Image.Image: 生成されたQRコードのPILイメージオブジェクト。
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L, # エラー訂正レベル
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

def main():
    st.set_page_config(page_title="QRコード生成アプリ", layout="centered")
    st.title("📸 QRコード生成アプリ")
    st.markdown("テキストやURLからQRコードを生成し、ダウンロードできます。")

    st.info("QRコードにしたいテキスト（URLなど）を入力してください。")

    user_input_data = st.text_area("QRコードにしたい内容:", height=150, placeholder="例: https://www.google.com または テストメッセージ")

    # セッションステートでQRコードのバイトデータを保持する
    if 'qr_byte_im' not in st.session_state:
        st.session_state.qr_byte_im = None
    if 'qr_caption' not in st.session_state:
        st.session_state.qr_caption = ""

    if st.button("QRコードを生成"):
        if user_input_data:
            with st.spinner("QRコードを生成中..."):
                qr_img_pil = generate_qr_code(user_input_data) # PIL.Image.Image オブジェクトを取得

                # ダウンロード用と表示用の両方で使えるように、PIL Imageをバイトデータに変換
                buf = BytesIO()
                qr_img_pil.save(buf, format="PNG")
                
                # セッションステートに保存
                st.session_state.qr_byte_im = buf.getvalue()
                st.session_state.qr_caption = "生成されたQRコード"
                
                st.rerun() # QRコードを表示するために再実行
        else:
            st.warning("QRコードにしたい内容を入力してください。")
            st.session_state.qr_byte_im = None # 入力がない場合はクリア
            st.session_state.qr_caption = ""
            st.rerun() # 警告表示のために再実行

    # セッションステートに画像データがあれば表示する
    if st.session_state.qr_byte_im:
        st.subheader("生成されたQRコード:")
        st.image(st.session_state.qr_byte_im, caption=st.session_state.qr_caption, use_container_width=True)

        st.download_button(
            label="QRコードをダウンロード (PNG)",
            data=st.session_state.qr_byte_im,
            file_name="qrcode.png",
            mime="image/png"
        )
            
    st.markdown("---")
    st.markdown("このアプリは、`qrcode`ライブラリを使用してQRコードを生成します。")

if __name__ == "__main__":
    main()
