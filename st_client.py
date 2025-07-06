from html import escape

import pandas as pd
import streamlit as st

import ntnuviz

st.set_page_config(
    page_title="臺師大課表視覺化",
    page_icon="📅",
    menu_items={"report a bug": "mailto:jahsehjaeger@proton.me"},
)

"""
# 臺師大課表視覺化

1. 課程查詢系統 > 開課和課程大綱查詢
2. 輸入學系、班級等相關篩選資料
3. 點選`開課資料匯出`
4. 上傳`.xls`檔案
5. 選擇年級
6. 取得課表 🎉

[程式源碼](https://github.com/JahsehJ/ntnuviz)
"""

c = st.container(border=True)

file = c.file_uploader(
    "上傳 `.xls` 檔案",
    type="xls",
)

year = c.selectbox("選擇年級", ("1", "2", "3", "4", "碩", "博"))

"""
:orange-badge[請務必核對資料正確性]

:blue-badge[無標註年級之課程資料一律顯示]

:violet-badge[回報問題: jahsehjaeger@proton.me]
"""


@st.fragment
def download_csv(csv: bytes) -> None:
    st.download_button(
        "匯出 `.csv` 檔", data=csv, file_name="課表.csv", mime="text/csv"
    )


if file:
    df = pd.read_excel(file, ntnuviz.SHEET_NAME)
    timetable = ntnuviz.timetable_from_df(df, year)

    def html_escape_and_replace_linebreak(x) -> str:
        return escape(str(x)).replace("\n", "<br>")

    timetable_df = ntnuviz.timetable_to_df(timetable)
    html = timetable_df.to_html(
        na_rep="",
        formatters=[html_escape_and_replace_linebreak for _ in range(5)],
        escape=False,
        border=0,
    )

    st.markdown(html, unsafe_allow_html=True)
    download_csv(timetable_df.to_csv().encode("utf-8"))
