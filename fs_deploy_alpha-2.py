
# Zhao Zifeng @ Peking University 

### TODO ###

file_name = 'https://github.com/ZhaZhaFon/ScoringRanking/files/10374068/results_20221231.xlsx'

### TODO ###

import pandas as pd

import streamlit as st

# 标题

st.set_page_config(layout="centered", page_icon="🎓", page_title="")
st.title("基金量化评分 - 主动权益基金")

# 数据

st.write("`#` 数据加载(约30s)...")
ranking = pd.read_excel(file_name, index_col=0).reset_index().rename(columns={"index": "基金代码"})
this_fund = ranking.iloc[0, :]
st.write("`#` 加载完毕(约30s).")

# 布局

left, right = st.columns(2)
left.write("##### 【基金信息】")
form = left.form("template_form")

right.write("##### 【量化评分】")

# 左侧布局




'''
st.write(f"呈现结果源于: [{file_name.split('/')[-1]}]({file_name})")

col1, col2 = st.columns(2)

ans = col1.selectbox(
        "123",
        options=(1, 2, 3)
    )
'''

# 右侧布局