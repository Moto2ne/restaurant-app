import streamlit as st
import pandas as pd
from collections import Counter  # 集計用

# データを読み込む関数
def load_data():
    try:
        return pd.read_csv("restaurants.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["店名", "料理", "場所"])

# データを保存する関数
def save_data(data):
    data.to_csv("restaurants.csv", index=False)

# アプリのタイトル
st.title("📌 みんなのおすすめレストラン")

# データ読み込み
data = load_data()

# おすすめ一覧を表示
st.subheader("📋 現在のおすすめレストラン一覧")
if data.empty:
    st.write("まだ登録されたレストランがありません。")
else:
    st.dataframe(data)

# 新しいレストランを追加
st.subheader("✍️ あなたのおすすめを追加")
with st.form("add_restaurant_form"):
    name = st.text_input("店名")
    dish = st.text_input("おすすめ料理")
    location = st.text_input("場所（例: 名古屋市）")  # 入力例を追加
    submitted = st.form_submit_button("追加する")
    
    if submitted:
        if name and dish and location:
            # 場所の形式チェック
            if location.endswith("市"):  # 簡単なチェック（正規表現不要）
                new_entry = pd.DataFrame({
                    "店名": [name],
                    "料理": [dish],
                    "場所": [location]
                })
                data = pd.concat([data, new_entry], ignore_index=True)
                save_data(data)
                st.success(f"店名 '{name}' を追加しました！")
            else:
                st.error("場所は「〇〇市」という形式で入力してください。")
        else:
            st.error("すべてのフィールドを入力してください。")

# 集計とランキング表示
if not data.empty:
    st.subheader("🏆 人気ランキング")
    
    # 店名のランキング
    restaurant_counts = Counter(data["店名"])
    restaurant_ranking = pd.DataFrame(restaurant_counts.items(), columns=["店名", "出現回数"]).sort_values(by="出現回数", ascending=False).head(5)
    st.write("🔝 店名ランキング（トップ5）")
    st.dataframe(restaurant_ranking)
    
    # 料理のランキング
    dish_counts = Counter(data["料理"])
    dish_ranking = pd.DataFrame(dish_counts.items(), columns=["料理", "出現回数"]).sort_values(by="出現回数", ascending=False).head(5)
    st.write("🔝 料理ランキング（トップ5）")
    st.dataframe(dish_ranking)

