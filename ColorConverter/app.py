import streamlit as st
import colorsys

def hex_to_rgb(hex_code):
    """HEX色コードをRGB値のタプルに変換します。"""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_tuple):
    """RGB値のタプルをHEX色コードに変換します。"""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_tuple).upper()

def rgb_to_hsv(rgb_tuple):
    """RGB値をHSV値のタプルに変換します。"""
    r, g, b = [c / 255.0 for c in rgb_tuple]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (int(h * 360), int(s * 100), int(v * 100))

def hsv_to_rgb(hsv_tuple):
    """HSV値をRGB値のタプルに変換します。"""
    h, s, v = hsv_tuple
    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s / 100.0, v / 100.0)
    return (int(r * 255), int(g * 255), int(b * 255))

st.set_page_config(
    page_title="Color Converter",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 Color Converter")
st.write("RGB、HEX、HSVの色コードを相互に変換します。")

# RGB入力セクション
st.header("RGB to HEX/HSV")
with st.expander("RGBから変換", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        r = st.slider("R", 0, 255, 128)
    with col2:
        g = st.slider("G", 0, 255, 128)
    with col3:
        b = st.slider("B", 0, 255, 128)

    rgb_tuple_input = (r, g, b)
    hex_output = rgb_to_hex(rgb_tuple_input)
    hsv_output = rgb_to_hsv(rgb_tuple_input)
    
    st.markdown(f"**HEX:** `{hex_output}`")
    st.markdown(f"**HSV:** `{hsv_output[0]}°, {hsv_output[1]}%, {hsv_output[2]}%`")
    st.markdown(f"**プレビュー:** <span style='background-color:{hex_output}; padding:10px; border-radius:5px; border:1px solid #ccc; width:100px;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>", unsafe_allow_html=True)


st.divider()

# HEX入力セクション
st.header("HEX to RGB/HSV")
with st.expander("HEXから変換", expanded=False):
    hex_input = st.text_input("HEXコードを入力してください (例: #808080)", "#808080").strip()
    
    if len(hex_input) == 7 and hex_input.startswith('#'):
        try:
            rgb_output = hex_to_rgb(hex_input)
            hsv_output_from_hex = rgb_to_hsv(rgb_output)
            
            st.markdown(f"**RGB:** `{rgb_output}`")
            st.markdown(f"**HSV:** `{hsv_output_from_hex[0]}°, {hsv_output_from_hex[1]}%, {hsv_output_from_hex[2]}%`")
            st.markdown(f"**プレビュー:** <span style='background-color:{hex_input}; padding:10px; border-radius:5px; border:1px solid #ccc; width:100px;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>", unsafe_allow_html=True)
            
        except ValueError:
            st.error("無効なHEXコードです。正しい形式で入力してください。")
    else:
        st.warning("HEXコードは`#`から始まる6桁の16進数で入力してください。")


st.divider()

# HSV入力セクション
st.header("HSV to RGB/HEX")
with st.expander("HSVから変換", expanded=False):
    col1_hsv, col2_hsv, col3_hsv = st.columns(3)
    with col1_hsv:
        h = st.slider("H (Hue)", 0, 360, 180)
    with col2_hsv:
        s = st.slider("S (Saturation)", 0, 100, 50)
    with col3_hsv:
        v = st.slider("V (Value)", 0, 100, 50)

    hsv_tuple_input = (h, s, v)
    rgb_output_from_hsv = hsv_to_rgb(hsv_tuple_input)
    hex_output_from_hsv = rgb_to_hex(rgb_output_from_hsv)
    
    st.markdown(f"**RGB:** `{rgb_output_from_hsv}`")
    st.markdown(f"**HEX:** `{hex_output_from_hsv}`")
    st.markdown(f"**プレビュー:** <span style='background-color:{hex_output_from_hsv}; padding:10px; border-radius:5px; border:1px solid #ccc; width:100px;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>", unsafe_allow_html=True)
