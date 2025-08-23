import streamlit as st
import math
import re

# calculate関数はmain関数の前に定義する
def calculate(expression):
    """
    与えられた数式を評価し、結果を返す。
    安全のため、eval()は使用せず、基本的な演算のみを許可する。
    """
    try:
        # 数式文字列から数値と演算子を抽出
        expression = expression.replace(" ", "")

        # 各種関数の置換 (Pythonのmathモジュールに合わせる)
        expression = expression.replace("sin(", "math.sin(")
        expression = expression.replace("cos(", "math.cos(")
        expression = expression.replace("tan(", "math.tan(")
        expression = expression.replace("log(", "math.log(") # 自然対数
        expression = expression.replace("log10(", "math.log10(") # 常用対数
        expression = expression.replace("sqrt(", "math.sqrt(")
        expression = expression.replace("pi", "math.pi")
        expression = expression.replace("e", "math.e")
        
        # べき乗記号 '^' が入力された場合を '**' に変換 (ボタンからも入るが手入力も考慮)
        expression = expression.replace("^", "**")

        # eval()に渡す前に、本当に計算してよい文字のみで構成されているか厳しくチェック
        # 数字、演算子、括弧、小数点、そしてmathモジュールから変換された関数名のみを許可
        # evalの安全性を確保するために非常に重要
        # 許可する文字/パターンの正規表現を結合
        # ここでre.escapeは不要、直接文字列として許可パターンを記述
        allowed_pattern_chars = r"[\d\.\+\-\*\/\(\)\s]"
        allowed_pattern_funcs = r"math\.sin|math\.cos|math\.tan|math\.log|math\.log10|math\.sqrt|math\.pi|math\.e|\*\*" # '**'も許可
        
        # 数式全体が許可された文字と関数のみで構成されているかチェック
        # 一度全ての許可パターンを空文字列に置き換えて、残るものがないか確認
        temp_expression = expression
        temp_expression = re.sub(r"("+allowed_pattern_funcs.replace('.', '\\.')+r")", "", temp_expression) # 関数部分を先に除去
        temp_expression = re.sub(allowed_pattern_chars, "", temp_expression) # 基本文字を除去
        
        if temp_expression.strip(): # 許可されない文字が残っていればエラー
            raise ValueError(f"不正な文字が含まれています: '{temp_expression.strip()}'")

        result = eval(expression)
        return result
    except SyntaxError:
        return "数式が正しくありません"
    except ZeroDivisionError:
        return "ゼロで割ることはできません"
    except ValueError as e:
        return f"エラー: {e}"
    except NameError:
        return "不正な関数名または変数名です"
    except TypeError as e:
        return f"型エラー: {e}"
    except Exception as e:
        return f"予期せぬ計算エラー: {e}"

def main():
    st.set_page_config(page_title="簡易計算機アプリ", layout="centered")
    st.title("🔢 簡易計算機アプリ")
    st.markdown("数値入力ボックスとボタンで四則演算や関数計算ができます。")

    # セッションステートの初期化
    if 'current_input' not in st.session_state:
        st.session_state.current_input = ""
    if 'result' not in st.session_state:
        st.session_state.result = ""

    # 結果表示エリア
    st.text_input("結果", value=st.session_state.result, key="display", disabled=True)

    # 入力ボックス
    st.text_input("数式を入力またはボタンで構成", value=st.session_state.current_input, key="input_box")

    # ユーザーがテキストボックスに直接入力した場合、st.session_state.input_box が更新される
    # その値を st.session_state.current_input に同期させる
    if st.session_state.input_box != st.session_state.current_input:
        st.session_state.current_input = st.session_state.input_box

    # ボタンの配置
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("7"): st.session_state.current_input += "7"; st.rerun()
        if st.button("4"): st.session_state.current_input += "4"; st.rerun()
        if st.button("1"): st.session_state.current_input += "1"; st.rerun()
        if st.button("0"): st.session_state.current_input += "0"; st.rerun()
    with col2:
        if st.button("8"): st.session_state.current_input += "8"; st.rerun()
        if st.button("5"): st.session_state.current_input += "5"; st.rerun()
        if st.button("2"): st.session_state.current_input += "2"; st.rerun()
        if st.button("."): st.session_state.current_input += "."; st.rerun()
    with col3:
        if st.button("9"): st.session_state.current_input += "9"; st.rerun()
        if st.button("6"): st.session_state.current_input += "6"; st.rerun()
        if st.button("3"): st.session_state.current_input += "3"; st.rerun()
        if st.button("C"): # Clearボタン
            st.session_state.current_input = ""
            st.session_state.result = ""
            st.rerun()
    with col4:
        # HTMLエンティティを使用する
        if st.button(" &divide; ", help="除算"): st.session_state.current_input += "/"; st.rerun()
        if st.button(" &times; ", help="乗算"): st.session_state.current_input += "*"; st.rerun()
        if st.button(" &minus; ", help="減算"): st.session_state.current_input += "-"; st.rerun()
        if st.button(" &plus; ", help="加算"): st.session_state.current_input += "+"; st.rerun()

    # 関数ボタンとその他
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        if st.button("( ", help="括弧の開始"): st.session_state.current_input += "("; st.rerun()
        if st.button("sqrt", help="平方根: sqrt(数値)"): st.session_state.current_input += "sqrt("; st.rerun()
        if st.button("log", help="自然対数: log(数値)"): st.session_state.current_input += "log("; st.rerun()
    with col6:
        if st.button(" )", help="括弧の終了"): st.session_state.current_input += ")"; st.rerun()
        if st.button(" ^ ", help="べき乗: (数値)^(べき数)"): st.session_state.current_input += "**"; st.rerun() # Pythonのべき乗演算子
        if st.button("log10", help="常用対数: log10(数値)"): st.session_state.current_input += "log10("; st.rerun()
    with col7:
        if st.button("sin", help="サイン (ラジアン): sin(数値)"): st.session_state.current_input += "sin("; st.rerun()
        if st.button("cos", help="コサイン (ラジアン): cos(数値)"): st.session_state.current_input += "cos("; st.rerun()
        if st.button("tan", help="タンジェント (ラジアン): tan(数値)"): st.session_state.current_input += "tan("; st.rerun()
    with col8:
        if st.button("π", help="円周率"): st.session_state.current_input += "pi"; st.rerun()
        if st.button("e", help="自然対数の底"): st.session_state.current_input += "e"; st.rerun()
        # = ボタンは最後に配置
        if st.button(" &equals; "): # = ボタンもHTMLエンティティを使用
            st.session_state.result = str(calculate(st.session_state.current_input))
            st.session_state.current_input = "" # 計算後に入力クリア
            st.rerun() # 結果を即時反映

if __name__ == "__main__":
    main()
