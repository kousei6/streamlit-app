import streamlit as st
from datetime import date

def calculate_age(birth_date):
    """
    Calculates age in years from a given birth date.
    
    Args:
        birth_date (datetime.date): The user's birth date.
        
    Returns:
        int: The calculated age in years.
    """
    today = date.today()
    
    # Calculate age
    age = today.year - birth_date.year
    
    # Adjust if the birthday has not yet occurred this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
        
    return age

# --- Streamlit UI ---

st.set_page_config(page_title="AgeCalculator", layout="centered")

st.title("🎂年齢計算アプリ")

st.markdown(
    """
    あなたの生年月日を入力して、現在の年齢を計算します。
    """
)

# Use st.date_input for user to select their birth date
# Use a key to ensure the widget is unique and to easily access its value
birth_date = st.date_input(
    "あなたの生年月日を選んでください",
    min_value=date(1900, 1, 1),
    max_value=date.today(),
    value=date(2000, 1, 1) # Default value
)

# A button to trigger the calculation
if st.button("年齢を計算"):
    if birth_date:
        # Pass the selected date to the calculation function
        age = calculate_age(birth_date)
        
        # Display the result
        st.success(f"あなたの現在の年齢は **{age}** 歳です！")
        
    else:
        st.warning("生年月日を選択してください。")

st.markdown("---")
st.markdown("Created with [Streamlit](https://streamlit.io/)")
