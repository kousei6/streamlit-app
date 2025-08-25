import streamlit as st
import pandas as pd

# 周期表のデータ
# 実際にはもっと多くのデータを含めることができますが、ここではデモンストレーション用に簡略化します。
PERIODIC_TABLE_DATA = {
    'AtomicNumber': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Symbol': ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne'],
    'Name': ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine', 'Neon'],
    'AtomicMass': [1.008, 4.0026, 6.94, 9.0122, 10.81, 12.011, 14.007, 15.999, 18.998, 20.180]
}

# DataFrameを作成
df_periodic_table = pd.DataFrame(PERIODIC_TABLE_DATA)

def app():
    """
    周期表の検索アプリケーション
    """
    st.title("簡易周期表アプリ :atom_symbol:")
    st.markdown("元素記号、原子番号、元素名で周期表の情報を検索できます。")

    # セレクターボックス
    search_type = st.selectbox(
        "検索方法を選択してください:",
        ["元素記号", "原子番号", "元素名"]
    )

    st.markdown("---")

    # 検索ウィジェットの表示
    if search_type == "元素記号":
        symbol = st.text_input("元素記号を入力してください (例: H, He)")
        if symbol:
            result = df_periodic_table[df_periodic_table['Symbol'].str.lower() == symbol.lower()]
            display_result(result)

    elif search_type == "原子番号":
        try:
            atomic_number = st.number_input("原子番号を入力してください (例: 1, 2)", min_value=1, format="%d")
            if atomic_number:
                result = df_periodic_table[df_periodic_table['AtomicNumber'] == atomic_number]
                display_result(result)
        except ValueError:
            st.error("有効な原子番号を入力してください。")

    elif search_type == "元素名":
        name = st.text_input("元素名を入力してください (例: Hydrogen, Helium)")
        if name:
            result = df_periodic_table[df_periodic_table['Name'].str.lower() == name.lower()]
            display_result(result)

    st.markdown("---")
    st.subheader("周期表のデータ一覧")
    st.dataframe(df_periodic_table)
    st.info("このデータはデモンストレーション用です。完全なデータではありません。")

def display_result(result_df):
    """
    検索結果をユーザーに表示するヘルパー関数
    """
    if not result_df.empty:
        st.success("検索結果が見つかりました！")
        for index, row in result_df.iterrows():
            st.write(f"**元素名:** {row['Name']}")
            st.write(f"**元素記号:** {row['Symbol']}")
            st.write(f"**原子番号:** {row['AtomicNumber']}")
            st.write(f"**原子量:** {row['AtomicMass']}")
    else:
        st.warning("お探しの元素は見つかりませんでした。入力内容を確認してください。")

if __name__ == "__main__":
    app()
