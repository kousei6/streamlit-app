import streamlit as st
import random

# アプリケーションのタイトルとレイアウトを設定
st.set_page_config(page_title="MealPlanner", layout="centered")

# ダミーの食事メニューデータ
MEALS = {
    "朝食": ["トーストと目玉焼き", "パンケーキ", "シリアルとフルーツ", "和朝食（ご飯、味噌汁、焼き魚）", "スムージーとヨーグルト"],
    "昼食": ["サンドイッチ", "パスタ", "チャーハン", "カレーライス", "うどん", "サラダボウル"],
    "夕食": ["ハンバーグ定食", "カレーライス", "鶏の唐揚げ", "豚の生姜焼き", "麻婆豆腐", "お寿司"],
}

DAYS_OF_WEEK = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

def initialize_session_state():
    """
    セッションステートを初期化する関数
    """
    if "meal_plan" not in st.session_state:
        st.session_state.meal_plan = {}
        generate_all_meals()

def generate_meal(day, meal_type):
    """
    特定の曜日と食事タイプのメニューをランダムに生成する関数
    """
    if day not in st.session_state.meal_plan:
        st.session_state.meal_plan[day] = {}
    st.session_state.meal_plan[day][meal_type] = random.choice(MEALS[meal_type])

def generate_all_meals():
    """
    すべての曜日と食事タイプのメニューを生成する関数
    """
    st.session_state.meal_plan = {}
    for day in DAYS_OF_WEEK:
        for meal_type in MEALS.keys():
            generate_meal(day, meal_type)

def main():
    """
    メインアプリケーションのロジック
    """
    initialize_session_state()

    st.title("🍽️ MealPlanner")
    st.markdown("一週間の食事メニューをランダムに提案します。")

    # 全件再提案ボタン
    st.button("すべてのメニューを再提案", on_click=generate_all_meals, use_container_width=True)

    st.markdown("---")

    # 曜日ごとのメニュー表示
    for day in DAYS_OF_WEEK:
        st.subheader(f"✨ {day}")
        
        # 曜日ごとのコンテナ
        with st.container(border=True):
            for meal_type in MEALS.keys():
                col1, col2 = st.columns([4, 1])
                with col1:
                    # 提案されたメニューを表示
                    st.write(f"**{meal_type}:** {st.session_state.meal_plan[day].get(meal_type, '')}")
                with col2:
                    # 個別の再提案ボタン
                    st.button(
                        "再提案",
                        key=f"{day}_{meal_type}_regenerate_btn",
                        on_click=generate_meal,
                        args=(day, meal_type),
                        use_container_width=True
                    )
        st.markdown("") # スペース用

if __name__ == "__main__":
    main()
