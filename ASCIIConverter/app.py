import streamlit as st

def string_to_ascii(text):
    """
    文字列をASCIIコードのリストに変換します。
    """
    return [ord(char) for char in text]

def ascii_to_string(ascii_codes):
    """
    ASCIIコードのリストを文字列に変換します。
    """
    return "".join([chr(code) for code in ascii_codes])

st.set_page_config(
    page_title="ASCII Converter",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 ASCII Converter")
st.write("文字列とASCIIコードを相互に変換します。")

# タブUIで機能を切り替え
tab1, tab2 = st.tabs(["文字列からASCII", "ASCIIから文字列"])

with tab1:
    st.header("文字列からASCIIコードへ")
    string_input = st.text_area(
        "ここに文字列を入力してください。",
        height=150,
        placeholder="例: Hello, World!"
    )
    
    if st.button("変換", key="string_to_ascii_btn"):
        if string_input:
            ascii_list = string_to_ascii(string_input)
            st.success("変換結果:")
            st.code(" ".join(map(str, ascii_list)), language="text")
            st.info("各数字はスペースで区切られた文字のASCIIコードを表します。")
        else:
            st.warning("文字列を入力してください。")
            
    with st.expander("ASCIIコードとは？"):
        st.markdown("""
        **ASCII** (American Standard Code for Information Interchange) は、コンピュータが文字を表現するために使用する文字コードです。
        各文字（例: 'A', 'a', '!'）には、0から127までのユニークな整数値が割り当てられています。
        """)
        st.markdown("")


with tab2:
    st.header("ASCIIコードから文字列へ")
    ascii_input = st.text_area(
        "ここにASCIIコードをスペースで区切って入力してください。",
        height=150,
        placeholder="例: 72 101 108 108 111 44 32 87 111 114 108 100 33"
    )
    
    if st.button("変換", key="ascii_to_string_btn"):
        if ascii_input:
            try:
                # 入力された文字列をスペースで分割し、整数リストに変換
                ascii_codes = [int(code) for code in ascii_input.split()]
                
                # ASCIIコードが有効な範囲かチェック (0-127)
                for code in ascii_codes:
                    if not (0 <= code <= 127):
                        st.error(f"無効なASCIIコードです: {code}。0から127の範囲で入力してください。")
                        break
                        
                result_string = ascii_to_string(ascii_codes)
                st.success("変換結果:")
                st.code(result_string, language="text")
            except ValueError:
                st.error("入力が無効です。スペースで区切られた半角数字のみを入力してください。")
        else:
            st.warning("ASCIIコードを入力してください。")
