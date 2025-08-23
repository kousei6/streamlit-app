# uobei-gacha

このコードは、魚べいという回転寿司チェーンのメニューから、指定された予算内でランダムに商品を選ぶ「N円ガチャ」をシミュレーションするものです。streamlitを使ってUIを作成し、メニュー選択や予算設定を可能にしています。以下にコード全体を詳しく説明します。

---

## **コード全体の概要**

1. **メニューデータの定義**:
   - `menu_city`: 都心型店舗のメニューデータ（商品名と価格）。
   - `menu_super_city`: 超都心型店舗のメニューデータ（商品名と価格）。

2. **`n_yen_gacha` 関数**:
   - 指定された予算内でランダムに商品を選ぶロジックを実装。

3. **Streamlit UI**:
   - streamlitライブラリを使用して、ユーザーが店舗タイプと予算を選択できるUIを作成。
   - 「ガチャを回す！」ボタンを押すと、`n_yen_gacha`関数を実行し、結果を表示。

---

## **詳細なコード説明**

### **1. メニューデータの定義**
```python
menu_city = [
    {"name": "大切りまぐろ", "price": 130},
    {"name": "まぐろステーキ", "price": 150},
    ...
]
menu_super_city = [
    {"name": "大切りまぐろ", "price": 170},
    {"name": "まぐろステーキ", "price": 190},
    ...
]
```
- `menu_city` と `menu_super_city` は、それぞれ都心型店舗と超都心型店舗のメニューを表すリストです。
- 各メニュー項目は辞書形式で、`"name"`（商品名）と `"price"`（価格）のキーを持ちます。

### **2. `n_yen_gacha` 関数**
```python
def n_yen_gacha(menu, target_price):
    result = []
    total = 0
    tries = 0

    while total < target_price and tries < 1000:
        item = random.choice(menu)
        if total + item["price"] <= target_price:
            result.append(item)
            total += item["price"]
        tries += 1
    return result, total
```
- **引数**:
  - `menu`: メニューのリスト（`menu_city` または `menu_super_city`）。
  - `target_price`: 予算（ガチャの上限金額）。

- **処理**:
  1. **初期化**:
     - `result = []`: 選ばれた商品を格納するリスト。
     - `total = 0`: 現在の合計金額。
     - `tries = 0`: 試行回数。

  2. **ループ**:
     - `while total < target_price and tries < 1000:`:
       - 合計金額が予算未満かつ試行回数が1000回未満の間、ループを続けます。
     - `item = random.choice(menu)`:
       - メニューからランダムに商品を選びます。
     - `if total + item["price"] <= target_price:`:
       - 現在の合計金額に選んだ商品の価格を足しても予算を超えない場合、商品を追加します。
       - `result.append(item)`: 選ばれた商品をリストに追加。
       - `total += item["price"]`: 合計金額を更新。
     - `tries += 1`: 試行回数を1増やします。

  3. **返却**:
     - `return result, total`: 選ばれた商品のリストとその合計金額を返します。

### **3. Streamlit UI**
```python
import streamlit as st
import random

st.title("🍣 魚べいN円ガチャ")

menu_type = st.selectbox("店舗を選んでください", ["都心型店舗", "超都心型店舗"])
budget = st.selectbox("予算を選んでください", [500, 1000, 1500])

if menu_type == "都心型店舗":
    selected_menu = menu_city
else:
    selected_menu = menu_super_city

if st.button("ガチャを回す！"):
    items, total = n_yen_gacha(selected_menu, budget)
    st.subheader("🎯 結果")
    for item in items:
        st.write(f"・{item['name']}（{item['price']}円）")
    st.write(f"**合計：{total}円**")
```
- **インポート**:
  - `import streamlit as st`: streamlitライブラリをインポートし、`st`という名前で使えるようにします。
  - `import random`: randomライブラリをインポート。
- **タイトル**:
  - `st.title("🍣 魚べいN円ガチャ")`: アプリのタイトルを表示。
- **店舗タイプの選択**:
  - `menu_type = st.selectbox("店舗を選んでください", ["都心型店舗", "超都心型店舗"])`:
    - ドロップダウンリストを作成し、店舗タイプを選択できるようにします。
    - 選択肢は "都心型店舗" と "超都心型店舗"。
- **予算の選択**:
  - `budget = st.selectbox("予算を選んでください",[500][1000][1500])`:
    - ドロップダウンリストを作成し、予算を選択できるようにします。
    - 選択肢は 500円、1000円、1500円。
- **メニューの選択**:
  - `if menu_type == "都心型店舗": selected_menu = menu_city else: selected_menu = menu_super_city`:
    - 選択された店舗タイプに応じて、使用するメニューデータを決定します。
- **ガチャ実行ボタン**:
  - `if st.button("ガチャを回す！"):`:
    - 「ガチャを回す！」ボタンを作成し、押されたときに以下の処理を実行します。
    - `items, total = n_yen_gacha(selected_menu, budget)`:
      - `n_yen_gacha` 関数を呼び出し、選ばれた商品のリストとその合計金額を取得します。
    - **結果表示**:
      - `st.subheader("🎯 結果")`: 結果のセクションタイトルを表示。
      - `for item in items: st.write(f"・{item['name']}（{item['price']}円）")`:
        - 選ばれた各商品について、商品名と価格を箇条書きで表示します。
      - `st.write(f"**合計：{total}円**")`: 合計金額を表示。

---

## **実行方法**

1. **必要なライブラリのインストール**:
   ```bash
   pip install streamlit
   ```

2. **コードの実行**:
   ```bash
   streamlit run スクリプト名.py
   ```

---
