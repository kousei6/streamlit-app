import streamlit as st
import json

def format_json(json_string):
    """
    JSON文字列を整形し、エラーがあればメッセージを返します。
    """
    try:
        # JSON文字列をPythonのオブジェクトにパース
        parsed_json = json.loads(json_string)
        # Pythonオブジェクトをインデント付きの整形済みJSON文字列に変換
        formatted_json = json.dumps(parsed_json, indent=4, ensure_ascii=False)
        return formatted_json, None
    except json.JSONDecodeError as e:
        # JSONデコードエラーをキャッチ
        return None, f"JSONデコードエラー: {e}"
    except Exception as e:
        # その他のエラーをキャッチ
        return None, f"予期せぬエラーが発生しました: {e}"

st.set_page_config(
    page_title="JSON Formatter",
    page_icon="📄",
    layout="wide"
)

st.title("📄 JSON Formatter")
st.write("JSONデータを入力すると、読みやすく整形して表示します。")

# ユーザー入力エリア
st.markdown("---")
st.subheader("入力")
input_json = st.text_area(
    "JSONデータをここに貼り付けてください。",
    height=300,
    placeholder="""{
  "name": "John Doe",
  "age": 30,
  "isStudent": false,
  "courses": [
    {
      "title": "History",
      "credits": 3
    },
    {
      "title": "Math",
      "credits": 4
    }
  ],
  "address": {
    "street": "123 Main St",
    "city": "Anytown"
  }
}"""
)

# 整形ボタン
if st.button("JSONを整形"):
    if input_json:
        formatted_data, error_message = format_json(input_json)
        
        st.markdown("---")
        st.subheader("出力")
        
        if error_message:
            st.error(error_message)
        else:
            # 整形済みJSONをコードブロックとして表示
            st.code(formatted_data, language="json")
            
            # 生データと整形済みデータのサイズを比較
            raw_size = len(input_json.encode('utf-8'))
            formatted_size = len(formatted_data.encode('utf-8'))
            
            st.markdown(
                f"""
                <div style="font-size: 0.9em; color: #666;">
                    <p>元のサイズ: {raw_size} バイト</p>
                    <p>整形後のサイズ: {formatted_size} バイト</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("JSONデータを入力してください。")
