import streamlit as st
import random
import numpy as np

def generate_bingo_card():
    """
    ビンゴカードの数字を生成する関数。
    B: 1-15, I: 16-30, N: 31-45, G: 46-60, O: 61-75
    """
    card = []
    # B列 (1-15)
    card.extend(random.sample(range(1, 16), 5))
    # I列 (16-30)
    card.extend(random.sample(range(16, 31), 5))
    # N列 (31-45) - 中央はFREE
    n_col = random.sample(range(31, 45), 4)
    n_col.insert(2, "FREE")
    card.extend(n_col)
    # G列 (46-60)
    card.extend(random.sample(range(46, 61), 5))
    # O列 (61-75)
    card.extend(random.sample(range(61, 76), 5))
    
    # 5x5のNumPy配列に変換して整形
    bingo_matrix = np.array(card).reshape(5, 5)
    return bingo_matrix

def main():
    """
    Streamlitアプリのメイン関数
    """
    st.set_page_config(page_title="BingoGenerator", layout="wide")
    
    st.title("🔢 Bingo Card Generator")
    st.markdown("---")
    
    # セッションステートにビンゴカードを保存
    if 'bingo_card' not in st.session_state:
        st.session_state.bingo_card = generate_bingo_card()
    
    # 「新しいカードを生成」ボタン
    if st.button("新しいビンゴカードを生成"):
        st.session_state.bingo_card = generate_bingo_card()
        st.rerun()

    # ビンゴカードの表示
    st.subheader("あなたのビンゴカード")
    
    # Streamlitのcolumn機能を使ってグリッドを整形
    columns = st.columns(5)
    headers = ["B", "I", "N", "G", "O"]
    
    # ヘッダー列
    for col, header in zip(columns, headers):
        with col:
            st.markdown(f"<h3 style='text-align: center;'>{header}</h3>", unsafe_allow_html=True)
            
    # ビンゴカードの表示
    for i in range(5):
        cols = st.columns(5)
        for j in range(5):
            with cols[j]:
                number = st.session_state.bingo_card[i, j]
                # FREEセルを強調表示
                if number == "FREE":
                    st.markdown(
                        f"<div style='text-align: center; border: 2px solid #4CAF50; border-radius: 5px; padding: 10px; font-size: 24px; font-weight: bold; background-color: #e8f5e9;'>{number}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div style='text-align: center; border: 1px solid #ddd; border-radius: 5px; padding: 10px; font-size: 24px;'>{number}</div>",
                        unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main()
