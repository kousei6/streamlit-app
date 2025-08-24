import streamlit as st
import autopep8
import difflib

st.set_page_config(
    page_title="Auto Code Formatter",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Auto Code Formatter")
st.write("完全に崩れたPythonコードでも、自動でインデントとスタイルを整形します。")
st.info("このアプリは `autopep8` を使用しています。`pip install autopep8` でインストールしてください。")

# 1. コード入力エリア
code_input = st.text_area(
    "ここにPythonコードを貼り付けてください。",
    height=400,
    placeholder="""
def fibonacci(n):
 if n<=0:
  return []
 elif n==1:
  return [0]
    elif n==2:
   return [0,1]
  else:
     seq=[0,1]
   for i in range(2,n):
       seq.append(seq[i-1]+seq[i-2])
        return seq

 def main():
    num=10
 print("Fibonacci sequence:")
    print(fibonacci(num))

main( )
"""
)

# 2. フォーマット実行ボタン
if st.button("コードを整形"):
    if code_input.strip():
        with st.spinner("整形中..."):
            try:
                # autopep8で整形
                formatted_code = autopep8.fix_code(code_input)

                # 整形結果の表示
                st.markdown("---")
                st.subheader("整形結果")
                st.code(formatted_code, language="python")

                # 整形前後の比較
                st.markdown("---")
                st.subheader("整形前後の差分")
                diff = difflib.unified_diff(
                    code_input.splitlines(keepends=True),
                    formatted_code.splitlines(keepends=True),
                    fromfile="original.py",
                    tofile="formatted.py"
                )
                diff_text = "".join(diff)

                if diff_text:
                    st.code(diff_text, language="diff")
                else:
                    st.info("コードは既に整形済みです。変更はありません。")

            except Exception as e:
                st.error(f"予期せぬエラーが発生しました: {e}")
    else:
        st.warning("Pythonコードを入力してください。")
