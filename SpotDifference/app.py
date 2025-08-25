import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import random
import os

# セッションステートの初期化
if 'correct_spots' not in st.session_state:
    st.session_state.correct_spots = set()
if 'total_differences' not in st.session_state:
    st.session_state.total_differences = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'image_loaded' not in st.session_state:
    st.session_state.image_loaded = False
if 'clicked_spots' not in st.session_state:
    st.session_state.clicked_spots = []
if 'images' not in st.session_state:
    st.session_state.images = {}
if 'image_paths' not in st.session_state:
    st.session_state.image_paths = {'A': "image_A.png", 'B': "image_B.png"}

def create_difference_images():
    """
    デモ用の間違い探し画像を生成する関数
    (実際のアプリではユーザーがアップロードすることも可能)
    """
    st.session_state.game_over = False
    st.session_state.correct_spots = set()
    st.session_state.clicked_spots = []
    
    # 既存のデモ画像を削除（再生成のため）
    for path in st.session_state.image_paths.values():
        if os.path.exists(path):
            os.remove(path)

    # サンプル画像を作成
    width, height = 600, 400
    img_A = Image.new('RGB', (width, height), 'white')
    draw_A = ImageDraw.Draw(img_A)
    # 基準となる図形を描画
    draw_A.rectangle((100, 100, 200, 200), fill='red') # 違い1の元
    draw_A.rectangle((300, 150, 400, 250), fill='blue') # 違い2の元
    draw_A.rectangle((500, 200, 550, 300), fill='green') # 違い3の元
    
    # img_Bはimg_Aからコピーし、違いを作成
    img_B = img_A.copy()
    draw_B = ImageDraw.Draw(img_B)
    
    # 違いを作成
    # 1. 四角形の色を変える
    draw_B.rectangle((100, 100, 200, 200), fill='orange')
    # 2. 四角形を消す (背景色で上書き)
    draw_B.rectangle((300, 150, 400, 250), fill='white')
    # 3. 四角形の位置を変える
    draw_B.rectangle((525, 200, 575, 300), fill='green') # 元の位置から右に移動

    img_A.save(st.session_state.image_paths['A'])
    img_B.save(st.session_state.image_paths['B'])

    # 正解座標の定義 (中心座標と許容範囲)
    st.session_state.total_differences = 3
    st.session_state.images = {
        'A': st.session_state.image_paths['A'],
        'B': st.session_state.image_paths['B']
    }
    st.session_state.difference_locs = {
        'red_to_orange': {'x': 150, 'y': 150, 'tolerance': 50}, # 違い1 (色変更)
        'blue_to_white': {'x': 350, 'y': 200, 'tolerance': 50}, # 違い2 (削除)
        'green_shift': {'x': 550, 'y': 250, 'tolerance': 50},   # 違い3 (位置変更後の中心)
    }
    st.session_state.image_loaded = True

def check_click(x, y):
    """
    クリックされた座標が正解エリア内にあるかチェックする
    """
    if st.session_state.game_over:
        return

    found_correct = False
    for key, loc in st.session_state.difference_locs.items():
        if key not in st.session_state.correct_spots:
            dist = np.sqrt((x - loc['x'])**2 + (y - loc['y'])**2)
            if dist <= loc['tolerance']:
                st.session_state.correct_spots.add(key)
                st.session_state.clicked_spots.append({'x': x, 'y': y, 'color': 'green'})
                found_correct = True
                if len(st.session_state.correct_spots) == st.session_state.total_differences:
                    st.session_state.game_over = True
                    st.balloons()
                st.rerun() # UIを更新
                return
    
    # 正解でなかった場合
    if not found_correct:
        st.session_state.clicked_spots.append({'x': x, 'y': y, 'color': 'red'})
        st.rerun() # UIを更新

# ----- Streamlit UI -----
st.title("間違い探しゲーム 🔎")
st.write("2枚の画像を見比べて、異なる箇所を全てクリックしてください！")

# ゲームの開始・リセットボタン
if st.button("新しいゲームを始める"):
    create_difference_images()
    st.rerun()

if st.session_state.image_loaded:
    if st.session_state.game_over:
        st.success("おめでとうございます！全ての誤りを見つけました！🎉")
    else:
        st.info(f"見つけた間違い: {len(st.session_state.correct_spots)} / {st.session_state.total_differences}")

    # 2枚の画像を並べて表示
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(st.session_state.images['A'], use_column_width=True, caption="画像A")
    
    with col2:
        image_B = Image.open(st.session_state.images['B'])
        draw = ImageDraw.Draw(image_B)

        # クリックされた箇所に印をつける
        for spot in st.session_state.clicked_spots:
            color = spot['color']
            x, y = spot['x'], spot['y']
            radius = 10
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=color, width=3)
        
        st.image(image_B, use_column_width=True, caption="画像B (クリックして間違い探し)")

    # 画像クリックイベントのハンドリング
    # Streamlitのネイティブ機能だけではクリック座標を取得できないため、JavaScriptと連携させる必要があります。
    # ここでは、簡略化のため、座標入力を模擬したテキスト入力フィールドを使用します。
    # 実際には、st.buttonを画像の上に重ねるなどのより複雑な実装が必要になります。
    st.markdown("---")
    st.subheader("⚠️ ここをクリックして間違いを探す代わりに、座標を入力してください (開発者向け)")
    st.info("この機能はStreamlitの制約のため、簡易的なデモです。")
    x_input = st.number_input("X座標を入力", min_value=0, max_value=600, value=0)
    y_input = st.number_input("Y座標を入力", min_value=0, max_value=400, value=0)
    
    if st.button("座標を送信"):
        check_click(x_input, y_input)

else:
    st.warning("「新しいゲームを始める」ボタンを押してゲームを開始してください。")
