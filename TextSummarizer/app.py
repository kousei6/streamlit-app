import streamlit as st
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
import nltk  # 必要なライブラリをimport

st.set_page_config(
    page_title="Text Summarizer",
    page_icon="✍️",
    layout="wide"
)

# NLTKのデータダウンロード（一度だけ実行）
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    st.warning("Downloading stopwords corpus...")
    nltk.download('stopwords')
    st.success("Stopwords corpus downloaded successfully.")

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    st.warning("Downloading punkt tokenizer...")
    nltk.download('punkt')
    st.success("Punkt tokenizer downloaded successfully.")

# 🔹 punkt_tab も追加（新しいNLTK仕様で必要）
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    st.warning("Downloading punkt_tab tokenizer...")
    nltk.download('punkt_tab')
    st.success("Punkt_tab tokenizer downloaded successfully.")

def summarize_text(text, n=3):
    """
    TF-IDFに基づいてテキストを要約します。
    
    Args:
        text (str): 要約する元のテキスト。
        n (int): 生成する要約文の数。
        
    Returns:
        str: 要約されたテキスト。
    """
    if not text.strip():
        return ""

    # 前処理：句読点、数字、小文字化
    cleaned_text = re.sub(r'[^a-zA-Z\s.]', '', text.lower())
    
    # 文章に分割
    sentences = sent_tokenize(cleaned_text)
    if len(sentences) <= n:
        # 元の文章数が指定された要約文数より少ない場合はそのまま返す
        return text

    # ストップワードの取得（英語）
    stop_words = set(stopwords.words('english'))
    
    # TF-IDFベクタライザの初期化
    vectorizer = TfidfVectorizer(stop_words=list(stop_words))
    
    # TF-IDF行列を計算
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # 各文章のスコアを計算（各文章のTF-IDF値の合計）
    sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
    
    # スコアの高い文章のインデックスを取得
    top_sentence_indices = sentence_scores.argsort()[-n:][::-1]
    
    # 元の文章の順番でソート
    sorted_indices = sorted(top_sentence_indices)
    
    # 要約文を生成
    summary_sentences = [sentences[i] for i in sorted_indices]
    
    return " ".join(summary_sentences)

st.title("✍️ Text Summarizer")
st.write("長い文章を自動的に要約します。")

st.info("""
このアプリは、**TF-IDF** (Term Frequency-Inverse Document Frequency) という技術を使用して、文章の重要度を計算し、最も重要な文章を抽出して要約を作成します。
""")

# 必要な外部ライブラリの表示
st.info("このアプリには`nltk`と`scikit-learn`が必要です。`pip install nltk scikit-learn`でインストールしてください。")

# ユーザー入力
input_text = st.text_area(
    "ここに要約したい文章を貼り付けてください。",
    height=400,
    placeholder="""
(ここに長い文章を入力してください。例：)
Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.
As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be "AI," having become a routine technology.
"""
)

# 要約文の数を指定
summary_length = st.slider(
    "要約する文章の数",
    min_value=1,
    max_value=10,
    value=3
)

if st.button("要約を実行"):
    if input_text:
        with st.spinner("要約中..."):
            summary = summarize_text(input_text, summary_length)
            st.markdown("---")
            st.subheader("要約結果")
            if summary:
                st.success(summary)
            else:
                st.warning("要約できませんでした。入力されたテキストを確認してください。")
    else:
        st.warning("文章を入力してください。")
