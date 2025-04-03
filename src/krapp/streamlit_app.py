import streamlit as st

from krapp.content_formatter import ContentFormatter
from krapp.date_extractor import DateExtractor
from krapp.text_db_manager import TextDBManager

# Streamlit セッション状態を使用して選択された年を保持
if "selected_year" not in st.session_state:
    st.session_state.selected_year = None

if "selected_month" not in st.session_state:
    st.session_state.selected_month = None

if "db" not in st.session_state:
    with st.spinner("Wait for it...", show_time=True):
        st.session_state.db = TextDBManager(
            folder_path="/Users/ishida/Documents/Texts",
            date_extractor=DateExtractor(),
        )
        st.session_state.db.process_folder()

db = st.session_state.db

# データを取得する関数

# サイドバーの設定
st.sidebar.title("ナビゲーション")
years = db.get_all_years()

for year in years:
    if year is None:
        continue
    if st.sidebar.button(year):
        st.session_state.selected_year = year
        st.session_state.selected_month = None

if st.session_state.selected_year:
    st.sidebar.markdown(f"### {st.session_state.selected_year} 年の月一覧")
    months = db.get_months_in_year(st.session_state.selected_year)

    for month in months:
        if st.sidebar.button(f"{month} 月"):
            st.session_state.selected_month = month

# 選択された年と月に応じたフィルタリング結果を表示
if st.session_state.selected_year and st.session_state.selected_month:
    st.title(
        f"{st.session_state.selected_year} 年 {st.session_state.selected_month} 月の投稿一覧"
    )
    filtered_entries = db.get_entries_by_year_month(
        st.session_state.selected_year, st.session_state.selected_month
    )

    if len(filtered_entries) > 0:
        formatter = ContentFormatter()
        for index, row in filtered_entries.iterrows():
            st.subheader(row["Title"])
            st.write(f"投稿日: {row['Date']}")
            st.markdown(formatter.format_content(row["Content"]))
            st.write("---")
    else:
        st.write("この月には投稿がありません。")
