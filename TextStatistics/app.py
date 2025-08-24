import streamlit as st
import re
from collections import Counter
import pandas as pd

st.set_page_config(
    page_title="Text Statistics",
    page_icon="📊",
    layout="wide"
)

def get_word_count(text):
    """
    テキストの単語数を取得します。
    """
    words = re.findall(r'\b\w+\b', text.lower())
    return len(words)

def get_character_count(text, include_spaces=True):
    """
    テキストの文字数を取得します。
    """
    if include_spaces:
        return len(text)
    else:
        return len(text.replace(" ", "").replace("\n", ""))

def get_line_count(text):
    """
    テキストの行数を取得します。
    """
    return text.count('\n') + 1 if text else 0

def get_word_frequency(text):
    """
    テキスト内の単語の出現頻度を計算します。
    """
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words).most_common(10)

st.title("📊 Text Statistics")
st.write("テキストを貼り付けて、文字数や単語数などの統計情報を確認しましょう。")

# 1. テキスト入力エリア
text_input = st.text_area(
    "ここに分析したいテキストを入力してください。",
    height=300,
    placeholder="""
テキスト統計は、自然言語処理（NLP）において基礎的なタスクです。
このツールは、文章の基本的な特性を素早く理解するのに役立ちます。
"""
)

# 2. 統計情報の計算と表示
if text_input:
    st.markdown("---")
    st.subheader("統計情報")

    char_count = get_character_count(text_input, include_spaces=True)
    word_count = get_word_count(text_input)
    line_count = get_line_count(text_input)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="文字数", value=char_count)
    with col2:
        st.metric(label="単語数", value=word_count)
    with col3:
        st.metric(label="行数", value=line_count)

    st.markdown("---")
    
    # 単語の出現頻度
    st.subheader("単語の出現頻度（トップ10）")
    word_freq = get_word_frequency(text_input)
    if word_freq:
        freq_df = pd.DataFrame(word_freq, columns=["単語", "出現回数"])
        st.table(freq_df)
    else:
        st.info("単語が検出されませんでした。")
else:
    st.info("テキストを入力すると、ここに統計情報が表示されます。")
