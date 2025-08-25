import streamlit as st
from datetime import date, timedelta

# アプリケーションのタイトルとレイアウトを設定
st.set_page_config(page_title="HabitTracker", layout="centered")

def initialize_session_state():
    """
    セッションステートを初期化する関数
    """
    if "habits" not in st.session_state:
        # habits: {習慣名: [達成日付, ...]}
        st.session_state.habits = {}

def add_habit():
    """
    新しい習慣をセッションステートに追加する関数
    """
    new_habit = st.session_state.new_habit_input.strip()
    if new_habit and new_habit not in st.session_state.habits:
        st.session_state.habits[new_habit] = []
        st.session_state.new_habit_input = "" # 入力ボックスをクリア

def clear_all_habits():
    """
    全ての習慣と記録をリセットする関数
    """
    st.session_state.habits = {}

def log_completion(habit_name):
    """
    指定された習慣の達成を記録する関数
    """
    today_str = date.today().isoformat()
    if today_str not in st.session_state.habits[habit_name]:
        st.session_state.habits[habit_name].append(today_str)
        st.session_state.habits[habit_name].sort() # 日付をソート

def delete_habit(habit_name):
    """
    指定された習慣をリストから削除する関数
    """
    del st.session_state.habits[habit_name]

def main():
    """
    メインアプリケーションのロジック
    """
    initialize_session_state()

    st.title("🎯 HabitTracker")
    st.markdown("日々の習慣や目標を記録しましょう。")

    # 習慣追加セクション
    with st.expander("新しい習慣を追加"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input("習慣名を入力", key="new_habit_input", on_change=add_habit, help="Enterキーを押すと追加されます")
        with col2:
            st.button("追加", on_click=add_habit, use_container_width=True)

    st.markdown("---")

    # 習慣リスト表示セクション
    if st.session_state.habits:
        for habit_name, completion_dates in st.session_state.habits.items():
            # 各習慣をコンテナで囲む
            with st.container(border=True):
                col_name, col_log, col_delete = st.columns([4, 1, 1])
                with col_name:
                    st.subheader(habit_name)
                with col_log:
                    # 達成ボタン
                    st.button("達成！", key=f"log_{habit_name}", on_click=log_completion, args=(habit_name,), use_container_width=True)
                with col_delete:
                    # 削除ボタン
                    st.button("削除", key=f"delete_{habit_name}", on_click=delete_habit, args=(habit_name,), use_container_width=True)

                if completion_dates:
                    st.markdown("---")
                    st.write("📅 **達成日:**")
                    # 達成日を文字列として表示
                    display_dates = ", ".join(completion_dates)
                    st.markdown(f"**{display_dates}**")
                else:
                    st.info("まだ達成記録がありません。")

        st.markdown("---")
        # 全件クリアボタン
        st.button("すべての習慣をリセット", on_click=clear_all_habits, use_container_width=True)
    else:
        st.info("まだ習慣がありません。新しい習慣を追加しましょう！")

if __name__ == "__main__":
    main()
