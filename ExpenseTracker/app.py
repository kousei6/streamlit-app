import streamlit as st
import pandas as pd
from datetime import date
import io

# アプリケーションのタイトルとレイアウトを設定
st.set_page_config(page_title="ExpenseTracker", layout="centered")

def initialize_session_state():
    """
    セッションステートを初期化する関数
    """
    if "expenses_df" not in st.session_state:
        # DataFrameの初期化: 日付, 項目, 金額, メモ
        st.session_state.expenses_df = pd.DataFrame(
            columns=["日付", "項目", "金額", "メモ"]
        )

def add_expense():
    """
    フォームからの入力に基づいて支出を記録する関数
    """
    # フォームからの値を取得
    item = st.session_state.item_input.strip()
    amount = st.session_state.amount_input
    memo = st.session_state.memo_input.strip()
    
    # 必須項目チェック
    if item and amount > 0:
        new_entry = pd.DataFrame(
            [{
                "日付": st.session_state.date_input,
                "項目": item,
                "金額": amount,
                "メモ": memo
            }]
        )
        # 既存のDataFrameに新しい行を追加
        st.session_state.expenses_df = pd.concat(
            [st.session_state.expenses_df, new_entry],
            ignore_index=True
        )
        # 入力ボックスをクリア
        st.session_state.item_input = ""
        st.session_state.amount_input = 0.0
        st.session_state.memo_input = ""
    else:
        st.warning("項目名と金額は必須です。")

def clear_data():
    """
    すべての支出データをリセットする関数
    """
    st.session_state.expenses_df = pd.DataFrame(
        columns=["日付", "項目", "金額", "メモ"]
    )

def main():
    """
    メインアプリケーションのロジック
    """
    initialize_session_state()

    st.title("💰 ExpenseTracker")
    st.markdown("毎日の支出を記録し、お金の流れを把握しましょう。")

    # 支出記録フォーム
    st.header("新しい支出を記録")
    with st.form(key='expense_form', clear_on_submit=False):
        # 日付入力
        col1, col2 = st.columns(2)
        with col1:
            record_date = st.date_input("日付", value=date.today(), key="date_input")
        
        # 項目と金額
        col3, col4 = st.columns(2)
        with col3:
            item = st.text_input("項目", key="item_input", help="例: 食費, 交通費")
        with col4:
            amount = st.number_input("金額 (円)", min_value=0.0, step=1.0, key="amount_input")

        # メモ
        memo = st.text_area("メモ (任意)", key="memo_input")
        
        # フォームの送信ボタン
        submit_button = st.form_submit_button(label="記録する", on_click=add_expense)
    
    st.markdown("---")

    # 支出の概要と一覧
    st.header("支出の概要")

    if not st.session_state.expenses_df.empty:
        total_expense = st.session_state.expenses_df["金額"].sum()
        st.metric(label="合計支出金額", value=f"¥ {total_expense:,.0f}")
        
        st.markdown("---")
        st.subheader("支出一覧")
        # 支出データを表示
        st.dataframe(st.session_state.expenses_df, use_container_width=True, hide_index=True)

        # データのエクスポートとクリアボタン
        st.markdown("---")
        col_download, col_clear = st.columns([3, 1])
        with col_download:
            csv_data = st.session_state.expenses_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="データをCSVでダウンロード",
                data=csv_data,
                file_name="expenses.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_clear:
            st.button("全データクリア", on_click=clear_data, use_container_width=True)
            
    else:
        st.info("まだ支出の記録がありません。上のフォームから支出を記録してください。")

if __name__ == "__main__":
    main()
