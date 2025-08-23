import streamlit as st

# --- Constants for Unit Conversions ---

# Length conversion factors (to meters)
LENGTH_UNITS = {
    "メートル (m)": 1.0,
    "キロメートル (km)": 1000.0,
    "センチメートル (cm)": 0.01,
    "ミリメートル (mm)": 0.001,
    "フィート (ft)": 0.3048,
    "インチ (in)": 0.0254,
    "マイル (mi)": 1609.34,
    "ヤード (yd)": 0.9144
}

# Weight conversion factors (to kilograms)
WEIGHT_UNITS = {
    "キログラム (kg)": 1.0,
    "グラム (g)": 0.001,
    "ポンド (lb)": 0.453592,
    "オンス (oz)": 0.0283495,
    "トン (t)": 1000.0
}

# --- Functions ---

def convert_unit(value, from_unit, to_unit, unit_dict):
    """
    Converts a value from one unit to another based on a dictionary of conversion factors.
    """
    if from_unit not in unit_dict or to_unit not in unit_dict:
        return None, "無効な単位です。"
    
    # Convert from the initial unit to the base unit (meters or kilograms)
    base_value = value * unit_dict[from_unit]
    
    # Convert from the base unit to the target unit
    converted_value = base_value / unit_dict[to_unit]
    
    return converted_value, None

# --- Streamlit UI ---

st.set_page_config(
    page_title="単位換算ツール",
    page_icon="⚖️",
    layout="centered"
)

st.title("⚖️ 単位換算ツール")
st.markdown("長さや重さなどの単位を簡単に換算します。")

# Select conversion mode
mode = st.radio("換算モードを選択してください", ("長さ", "重さ"))

st.markdown("---")

if mode == "長さ":
    st.header("📏 長さの換算")
    units = list(LENGTH_UNITS.keys())
    unit_dict = LENGTH_UNITS
    help_text = "変換元の長さを入力してください。"

elif mode == "重さ":
    st.header("🏋️ 重さの換算")
    units = list(WEIGHT_UNITS.keys())
    unit_dict = WEIGHT_UNITS
    help_text = "変換元の重さを入力してください。"

# User input
col1, col2, col3 = st.columns(3)

with col1:
    from_unit = st.selectbox("変換元", units, index=units.index("メートル (m)" if mode == "長さ" else "キログラム (kg)"))

with col2:
    try:
        value_input = st.number_input(f"数値を入力", min_value=0.0, help=help_text)
    except Exception:
        value_input = 0.0
        st.warning("有効な数値を入力してください。")

with col3:
    to_unit = st.selectbox("変換先", units, index=units.index("フィート (ft)" if mode == "長さ" else "ポンド (lb)"))

# Perform conversion
if value_input is not None:
    converted_value, error = convert_unit(value_input, from_unit, to_unit, unit_dict)

    st.markdown("---")

    if error:
        st.error(error)
    else:
        st.subheader("換算結果")
        st.success(f"**{value_input:,.4f} {from_unit.split(' ')[0]}** は **{converted_value:,.4f} {to_unit.split(' ')[0]}** です。")
