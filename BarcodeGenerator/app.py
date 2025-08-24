import streamlit as st
import barcode
from barcode.writer import ImageWriter
from barcode.errors import BarcodeNotFoundError
from PIL import Image
import io

def generate_barcode(code_type, data):
    """
    指定された種類とデータでバーコード画像を生成します。
    サポートされる種類: JAN (EAN-13), Code128
    """
    try:
        if code_type == 'JAN':
            # EAN-13は13桁の数字である必要があります
            if not (data.isdigit() and len(data) == 13):
                st.error("JANコードは13桁の数字でなければなりません。")
                return None
            EAN = barcode.get_barcode_class('ean13')
            ean = EAN(data, writer=ImageWriter())
            
        elif code_type == 'Code 128':
            # Code 128は任意の文字列に対応
            if not data:
                st.error("Code 128のデータは空にできません。")
                return None
            Code128 = barcode.get_barcode_class('code128')
            ean = Code128(data, writer=ImageWriter())
        
        else:
            st.error("サポートされていないバーコードタイプです。")
            return None

        # バーコードをメモリ上のPNG画像として生成
        buffer = io.BytesIO()
        ean.write(buffer)
        buffer.seek(0)
        
        return Image.open(buffer)
    
    except barcode.errors.BarcodeNotFoundError:
        st.error(f"'{code_type}'のバーコードタイプが見つかりません。")
        return None
    except Exception as e:
        st.error(f"バーコード生成中にエラーが発生しました: {e}")
        return None

st.set_page_config(
    page_title="Barcode Generator",
    page_icon=" barcodes",
    layout="centered"
)

st.title(" Barcode Generator")
st.write("JANコード（EAN-13）やCode 128などのバーコードを生成します。")

# 必要な外部ライブラリの表示
st.info("このアプリには`python-barcode`ライブラリが必要です。`pip install python-barcode`でインストールしてください。")

# バーコードタイプ選択
barcode_type = st.radio("生成するバーコードの種類を選択してください。", ('JAN', 'Code 128'))

# データ入力
if barcode_type == 'JAN':
    user_input = st.text_input("13桁のJANコード（EAN-13）を入力してください。", value="4901234567891")
else:
    user_input = st.text_input("生成したい文字列を入力してください。", value="Streamlit-App")

# ボタンで生成をトリガー
if st.button("バーコードを生成"):
    if user_input:
        with st.spinner("バーコードを生成中..."):
            barcode_image = generate_barcode(barcode_type, user_input)
            if barcode_image:
                st.image(barcode_image, caption=f"{barcode_type} バーコード", use_column_width=True)
                
                # ダウンロードボタン
                img_buffer = io.BytesIO()
                barcode_image.save(img_buffer, format="PNG")
                img_buffer.seek(0)
                
                st.download_button(
                    label="画像をダウンロード (PNG)",
                    data=img_buffer,
                    file_name=f"{barcode_type}_{user_input}.png",
                    mime="image/png"
                )
    else:
        st.warning("バーコードを生成するにはデータを入力してください。")
