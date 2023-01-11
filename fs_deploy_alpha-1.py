
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
#'''
st.write("`#` 数据加载(约5s)...")
ranking = pd.read_excel(file_name, index_col=0).reset_index().rename(columns={"index": "基金代码"})
st.write("`#` 加载完毕.")
#'''
st.write(f"`#` 呈现结果源于: [{file_name.split('/')[-1]}]({file_name})")

# 布局

left, right = st.columns(2)
left.write("##### 【基金信息】")

# 左侧布局

form = left.form("template_form")
ans = left.selectbox(
    "基金产品",
    options=tuple(ranking['基金代码'].tolist())
)
# 右侧布局

right.write("##### 【量化评分】")
