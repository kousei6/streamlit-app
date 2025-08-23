import streamlit as st
import requests
import json
from datetime import datetime

# --- Functions ---
def get_exchange_rate(api_key, base_currency, target_currency):
    """
    Fetches the real-time exchange rate from a currency conversion API.
    Uses the API from exchangerate-api.com.
    """
    if not api_key:
        st.error("APIキーが設定されていません。サイドバーから`exchangerate-api.com`のAPIキーを入力してください。")
        return None
        
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        
        if data.get("result") == "success":
            return data["conversion_rates"].get(target_currency)
        else:
            st.error(f"APIエラー: {data.get('error-type', '不明なエラー')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"APIへの接続中にエラーが発生しました: {e}")
        return None

# --- Streamlit UI ---

st.set_page_config(
    page_title="通貨換算ツール",
    page_icon="💵",
    layout="centered"
)

st.title("💵 通貨換算ツール")
st.markdown("リアルタイムの為替レートを使用して、通貨を換算します。")

# --- Sidebar for API key input ---
with st.sidebar:
    st.header("設定")
    api_key_help = "exchangerate-api.comから取得したAPIキーを入力してください。無料版で十分です。"
    api_key = st.text_input("APIキー", type="password", help=api_key_help)
    st.markdown("APIキーの取得: [exchangerate-api.com](https://www.exchangerate-api.com/)")

# --- Main App ---
currency_list = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "HKD", "KRW"]

col1, col2 = st.columns(2)

with col1:
    base_currency = st.selectbox("変換元通貨", currency_list, index=currency_list.index("JPY"))

with col2:
    target_currency = st.selectbox("変換先通貨", currency_list, index=currency_list.index("USD"))

try:
    amount = st.number_input(f"金額 ({base_currency})", min_value=0.01, value=100.0)
except Exception:
    amount = 0.0
    st.warning("有効な数値を入力してください。")

if st.button("換算"):
    if not api_key:
        st.warning("APIキーを入力してください。")
    else:
        with st.spinner("為替レートを取得中..."):
            rate = get_exchange_rate(api_key, base_currency, target_currency)
            
            st.markdown("---")
            
            if rate is not None:
                converted_amount = amount * rate
                st.subheader("換算結果")
                st.success(f"**{amount:,.2f} {base_currency}** は **{converted_amount:,.2f} {target_currency}** です。")
                st.info(f"1 {base_currency} = {rate:,.4f} {target_currency} （レート取得時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}）")
            else:
                st.error("換算に失敗しました。APIキーまたはネットワーク接続を確認してください。")
