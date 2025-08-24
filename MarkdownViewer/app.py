import streamlit as st
import markdown

st.set_page_config(
    page_title="Markdown Viewer",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Markdown Viewer")
st.write("左側のテキストボックスにMarkdownを記述すると、右側にリアルタイムでプレビューが表示されます。")

st.info("このアプリには`markdown`ライブラリが必要です。`pip install markdown`でインストールしてください。")

# 2つのカラムを作成
col1, col2 = st.columns(2)

with col1:
    st.header("入力 (Markdown)")
    markdown_text = st.text_area(
        "Markdownを入力してください。",
        height=500,
        placeholder="""# これは見出しです

## これはサブ見出しです

これは普通の段落です。

**太字**や*斜体*、そして`コード`を記述できます。

- リストの項目1
- リストの項目2

[Streamlitの公式サイト](https://streamlit.io)

```python
import streamlit as st
st.write("Hello, world!")
"""
)

with col2:
    st.header("プレビュー (HTML)")
    if markdown_text:
        # MarkdownをHTMLに変換
        html_output = markdown.markdown(markdown_text)
        # HTMLとして表示
        st.markdown(html_output, unsafe_allow_html=True)
    else:
        st.info("ここにプレビューが表示されます。")
