import streamlit as st

# アプリケーションのタイトルを設定
st.set_page_config(page_title="GroceryList", layout="centered")

def initialize_session_state():
    """
    セッションステートを初期化する関数
    """
    if "grocery_list" not in st.session_state:
        st.session_state.grocery_list = []

def add_item():
    """
    買い物リストにアイテムを追加する関数
    """
    # テキスト入力ボックスの値を取得
    new_item = st.session_state.new_item_input.strip()
    if new_item:
        st.session_state.grocery_list.append(new_item)
        # 入力ボックスをクリア
        st.session_state.new_item_input = ""

def delete_item(item_to_delete):
    """
    指定されたアイテムをリストから削除する関数
    """
    st.session_state.grocery_list.remove(item_to_delete)

def clear_list():
    """
    買い物リストをすべてクリアする関数
    """
    st.session_state.grocery_list = []

def main():
    """
    メインアプリケーションのロジック
    """
    # セッションステートの初期化
    initialize_session_state()

    # タイトルと説明
    st.title("🛒 GroceryList")
    st.markdown("買い物リストを作成・管理できるシンプルなアプリです。")

    # アイテム追加セクション
    st.header("アイテムを追加")
    # 入力と追加ボタンを横に並べる
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input("ここにアイテム名を入力", key="new_item_input", on_change=add_item, help="Enterキーを押すと追加されます")
    with col2:
        st.button("追加", on_click=add_item, use_container_width=True)

    st.markdown("---")

    # 買い物リスト表示セクション
    st.header("買い物リスト")
    if st.session_state.grocery_list:
        # リストアイテムを列挙
        for i, item in enumerate(st.session_state.grocery_list):
            item_col, button_col = st.columns([5, 1])
            with item_col:
                st.write(f"- {item}")
            with button_col:
                # 削除ボタン。`key`をユニークにするためにインデックスを使用
                st.button("削除", key=f"delete_btn_{i}", on_click=delete_item, args=(item,), use_container_width=True)

        st.markdown("---")

        # 全件削除ボタン
        if st.button("リストをすべてクリア", use_container_width=True):
            clear_list()
    else:
        st.info("買い物リストにアイテムがありません。")

if __name__ == "__main__":
    main()
