import streamlit as st

def calculate_bmi(height_cm, weight_kg):
    """
    身長（cm）と体重（kg）からBMIを計算する

    Args:
        height_cm (float or int): 身長（センチメートル）
        weight_kg (float or int): 体重（キログラム）

    Returns:
        float or None: 計算されたBMI値。無効な入力の場合はNone。
    """
    if height_cm <= 0 or weight_kg <= 0:
        return None
    
    height_m = height_cm / 100 # cmをmに変換
    bmi = weight_kg / (height_m ** 2)
    return bmi

def get_bmi_category(bmi):
    """
    BMI値に基づいて肥満度を分類する（日本肥満学会の基準）

    Args:
        bmi (float): BMI値

    Returns:
        str: 肥満度カテゴリの文字列
    """
    if bmi < 18.5:
        return "低体重 (やせ型)"
    elif 18.5 <= bmi < 25:
        return "普通体重"
    elif 25 <= bmi < 30:
        return "肥満 (1度)"
    elif 30 <= bmi < 35:
        return "肥満 (2度)"
    elif 35 <= bmi < 40:
        return "肥満 (3度)"
    else:
        return "肥満 (4度)"

def main():
    st.set_page_config(page_title="BMI計算ツール", layout="centered")
    st.title("BMI計算ツール")
    st.markdown("あなたの身長と体重からBMI（Body Mass Index）を計算します。")

    st.info("※BMI（Body Mass Index）は、体重と身長の関係から算定される、肥満度を示す指数です。")
    st.markdown("---")

    # 入力フィールド
    height = st.number_input("身長 (cm)", min_value=1.0, max_value=300.0, value=170.0, step=0.1, help="例: 170.5")
    weight = st.number_input("体重 (kg)", min_value=1.0, max_value=500.0, value=60.0, step=0.1, help="例: 60.0")

    if st.button("BMIを計算"):
        if height > 0 and weight > 0:
            bmi_value = calculate_bmi(height, weight)
            if bmi_value is not None:
                st.subheader("計算結果:")
                st.write(f"あなたのBMIは **{bmi_value:.2f}** です。")

                bmi_category = get_bmi_category(bmi_value)
                st.write(f"判定: **{bmi_category}**")

                # 肥満度に応じた色分け表示
                if bmi_category == "普通体重":
                    st.success("おめでとうございます！健康的な範囲のBMIです。")
                elif "低体重" in bmi_category:
                    st.warning("低体重です。健康のために適切な体重を目指しましょう。")
                else: # 肥満のカテゴリ
                    st.error("肥満の傾向があります。生活習慣の見直しを検討しましょう。")
            else:
                st.error("身長と体重は正の値を入力してください。")
        else:
            st.warning("身長と体重を入力してください。")

    st.markdown("---")
    st.subheader("BMIの分類（日本肥満学会の基準）")
    st.markdown("""
    * 18.5未満: 低体重 (やせ型)
    * 18.5以上 25未満: 普通体重
    * 25以上 30未満: 肥満 (1度)
    * 30以上 35未満: 肥満 (2度)
    * 35以上 40未満: 肥満 (3度)
    * 40以上: 肥満 (4度)
    """)

if __name__ == "__main__":
    main()
