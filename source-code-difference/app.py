import streamlit as st
import difflib

def highlight_diff(text1, text2):
    """
    2つのテキストの差分をハイライトしてHTML形式で返します。
    """
    d = difflib.Differ()
    diff = d.compare(text1.splitlines(keepends=True), text2.splitlines(keepends=True))
    
    html_output = "<pre style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>"
    for line in diff:
        if line.startswith('+ '):
            html_output += f"<span style='background-color: #d4edda; display: block;'>{line}</span>"  # 追加された行 (緑)
        elif line.startswith('- '):
            html_output += f"<span style='background-color: #f8d7da; display: block;'>{line}</span>"  # 削除された行 (赤)
        elif line.startswith('? '):
            # 変更された行の内部差分（今回はシンプルなハイライトのため無視）
            # 必要であれば、difflib.SequenceMatcherなどで詳細な差分を取得し、より複雑なハイライトを実装
            pass 
        else:
            html_output += f"<span>{line}</span>"
    html_output += "</pre>"
    return html_output

st.set_page_config(layout="wide")

st.title("ソースコード差分チェッカー")

st.markdown("""
    このアプリケーションは、2つの入力されたテキスト（ソースコードなど）の差分を表示します。
    変更された行はハイライトされます。
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("元のコード")
    code1 = st.text_area("最初のコードをここに入力してください", height=300, key="code1")

with col2:
    st.subheader("新しいコード")
    code2 = st.text_area("比較するコードをここに入力してください", height=300, key="code2")

if st.button("差分を表示"):
    if code1 and code2:
        st.subheader("差分結果")
        diff_html = highlight_diff(code1, code2)
        st.components.v1.html(diff_html, height=600, scrolling=True)
    else:
        st.warning("両方のテキストエリアにコードを入力してください。")

st.markdown("---")
st.markdown("Powered by Streamlit")
