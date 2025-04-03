import sqlite3

import pandas as pd
import streamlit as st

# SQLite データベースに接続
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Streamlit セッション状態を使用して選択された年を保持
if "selected_year" not in st.session_state:
    st.session_state.selected_year = None

if "selected_month" not in st.session_state:
    st.session_state.selected_month = None


# データを取得する関数
def get_entries_by_year_month(year, month):
    cursor.execute(
        "SELECT id, date, title, content FROM entries WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ? ORDER BY date DESC",
        (year, month),
    )
    rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=["ID", "Date", "Title", "Content"])


def get_all_years():
    cursor.execute(
        "SELECT DISTINCT strftime('%Y', date) as year FROM entries ORDER BY year DESC"
    )
    return [row[0] for row in cursor.fetchall()]


def get_months_in_year(year):
    cursor.execute(
        "SELECT DISTINCT strftime('%m', date) as month FROM entries WHERE strftime('%Y', date) = ? ORDER BY month",
        (year,),
    )
    return [row[0] for row in cursor.fetchall()]


# サイドバーの設定
st.sidebar.title("ナビゲーション")
years = get_all_years()

for year in years:
    if year is None:
        continue
    if st.sidebar.button(year):
        st.session_state.selected_year = year
        st.session_state.selected_month = None

if st.session_state.selected_year:
    st.sidebar.markdown(f"### {st.session_state.selected_year} 年の月一覧")
    months = get_months_in_year(st.session_state.selected_year)

    for month in months:
        if st.sidebar.button(f"{month} 月"):
            st.session_state.selected_month = month

# 選択された年と月に応じたフィルタリング結果を表示
if st.session_state.selected_year and st.session_state.selected_month:
    st.title(
        f"{st.session_state.selected_year} 年 {st.session_state.selected_month} 月の投稿一覧"
    )
    filtered_entries = get_entries_by_year_month(
        st.session_state.selected_year, st.session_state.selected_month
    )

    if len(filtered_entries) > 0:
        for index, row in filtered_entries.iterrows():
            st.subheader(row["Title"])
            st.write(f"投稿日: {row['Date']}")
            st.markdown(row["Content"])
            st.write("---")
    else:
        st.write("この月には投稿がありません。")

conn.close()
