import streamlit as st
import calendar
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import io
import holidays

# --- PDF生成のための設定 ---
# 日本語フォントの登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

# --- 祝日データのキャッシュ ---
# holidaysライブラリのインスタンスをセッションステートにキャッシュ
@st.cache_data
def get_holidays(year):
    return holidays.JP(years=year)

def create_calendar_pdf(year, month):
    """
    指定された年月のカレンダーをPDFとして生成する。
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ページタイトル
    c.setFont('HeiseiKakuGo-W5', 24)
    c.drawCentredString(width / 2.0, height - 50, f"{year}年 {month}月")

    # カレンダーのヘッダー（曜日）
    c.setFont('HeiseiKakuGo-W5', 12)
    days_of_week = ["月", "火", "水", "木", "金", "土", "日"]
    x_start = 50
    y_start = height - 100
    cell_width = (width - 100) / 7
    cell_height = 40

    for i, day in enumerate(days_of_week):
        color = "black"
        if day == "土":
            c.setFillColorRGB(0.0, 0.0, 1.0) # 青
        elif day == "日":
            c.setFillColorRGB(1.0, 0.0, 0.0) # 赤
        else:
            c.setFillColorRGB(0.0, 0.0, 0.0) # 黒
        c.drawCentredString(x_start + i * cell_width + cell_width / 2.0, y_start - 10, day)

    # カレンダーの日付
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    
    jp_holidays = get_holidays(year)

    c.setFont('HeiseiKakuGo-W5', 14)
    for row, week in enumerate(month_days):
        for col, day in enumerate(week):
            if day == 0:
                continue

            day_obj = date(year, month, day)
            
            # 曜日と祝日で色分け
            if day_obj in jp_holidays:
                c.setFillColorRGB(1.0, 0.0, 0.0) # 赤（祝日）
            elif day_obj.weekday() == 5: # 土曜日
                c.setFillColorRGB(0.0, 0.0, 1.0) # 青
            elif day_obj.weekday() == 6: # 日曜日
                c.setFillColorRGB(1.0, 0.0, 0.0) # 赤
            else:
                c.setFillColorRGB(0.0, 0.0, 0.0) # 黒

            x_pos = x_start + col * cell_width + 10
            y_pos = y_start - 30 - row * cell_height

            # 日付の描画
            c.drawString(x_pos, y_pos, str(day))

            # 祝日の名前を描画
            if day_obj in jp_holidays:
                holiday_name = jp_holidays[day_obj]
                c.setFont('HeiseiMin-W3', 8)
                c.drawString(x_pos, y_pos - 10, holiday_name)
                c.setFont('HeiseiKakuGo-W5', 14)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- Streamlitアプリのメイン関数 ---
def main():
    st.title("月間カレンダープリンター")
    st.subheader("指定した年月のカレンダーをPDFで作成・ダウンロードできます。")

    st.markdown("---")

    # 現在の日付を取得
    today = date.today()
    
    # ユーザー入力
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("年", min_value=1900, max_value=2100, value=today.year)
    with col2:
        month = st.number_input("月", min_value=1, max_value=12, value=today.month)

    st.markdown("---")

    if st.button("カレンダーPDFを生成"):
        try:
            with st.spinner("PDFを生成中..."):
                pdf_buffer = create_calendar_pdf(year, month)
                st.download_button(
                    label="PDFをダウンロード",
                    data=pdf_buffer,
                    file_name=f"calendar_{year}_{month}.pdf",
                    mime="application/pdf"
                )
            st.success("PDFが生成されました！ダウンロードボタンをクリックしてください。")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

    # アプリケーションの説明
    st.markdown("""
        ### アプリケーションについて
        このアプリは、入力された年と月のカレンダーをPDF形式で作成します。
        - **日本の祝日**を自動的に取得し、赤字で表示します。
        - **土曜日と日曜日**も色分けして表示されます。
        - 印刷に適したA4サイズでレイアウトされます。
        
        #### 注意
        - 祝日データは`holidays`ライブラリに依存します。
        - PDF出力には`reportlab`ライブラリを使用しています。
    """)

if __name__ == "__main__":
    main()
