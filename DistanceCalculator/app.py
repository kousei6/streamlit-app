import streamlit as st
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    """
    Haversine formula to calculate the great-circle distance between two points
    on a sphere (the Earth).
    
    Args:
        lat1 (float): Latitude of the first point in degrees.
        lon1 (float): Longitude of the first point in degrees.
        lat2 (float): Latitude of the second point in degrees.
        lon2 (float): Longitude of the second point in degrees.
        
    Returns:
        float: The distance in kilometers.
    """
    R = 6371.0  # Earth's radius in kilometers
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c
    
    return distance

# --- Streamlit UI ---

st.set_page_config(page_title="DistanceCalculator", layout="centered")

st.title("🌎2地点間距離計算アプリ")

st.markdown(
    """
    2つの地点の緯度と経度を入力して、その間の直線距離（大円距離）を計算します。
    """
)

# Use columns for a clean layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("地点1")
    lat1 = st.number_input(
        "緯度1 (度)",
        min_value=-90.0,
        max_value=90.0,
        value=35.6895,
        format="%.4f",
        help="例: 35.6895 (東京)"
    )
    lon1 = st.number_input(
        "経度1 (度)",
        min_value=-180.0,
        max_value=180.0,
        value=139.6917,
        format="%.4f",
        help="例: 139.6917 (東京)"
    )

with col2:
    st.subheader("地点2")
    lat2 = st.number_input(
        "緯度2 (度)",
        min_value=-90.0,
        max_value=90.0,
        value=34.0522,
        format="%.4f",
        help="例: 34.0522 (ロサンゼルス)"
    )
    lon2 = st.number_input(
        "経度2 (度)",
        min_value=-180.0,
        max_value=180.0,
        value=-118.2437,
        format="%.4f",
        help="例: -118.2437 (ロサンゼルス)"
    )

# A button to trigger the calculation
if st.button("距離を計算"):
    # Perform the calculation
    distance = haversine(lat1, lon1, lat2, lon2)
    
    # Display the result
    st.success(f"2地点間の直線距離は **{distance:.2f} km** です。")
    st.info("※ この計算は地球を完全な球体と仮定しています。")

st.markdown("---")
st.markdown("Created with [Streamlit](https://streamlit.io/)")
