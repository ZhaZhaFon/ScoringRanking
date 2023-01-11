
# Zhao Zifeng @ Peking University 

### TODO ###

file_name = 'https://github.com/ZhaZhaFon/ScoringRanking/files/10374068/results_20221231.xlsx'

### TODO ###

import pandas as pd

import streamlit as st

from pyecharts.charts import *
from pyecharts import options as opts
import streamlit_echarts

# 标题

st.set_page_config(layout="centered", page_icon="🎓", page_title="")
st.title("基金量化评分 - 主动权益基金")

# 数据
#'''
st.write("`#` 数据加载(约5s)...")
ranking = pd.read_excel(file_name, index_col=0).reset_index().rename(columns={"index": "基金代码"})
product_tuple = tuple(ranking['基金代码'].tolist())
manager_tuple = tuple(ranking['基金经理'].tolist())
company_tuple = tuple(ranking['基金公司'].tolist())
st.write("`#` 加载完毕, 呈现结果基于量化评分排名: [{file_name.split('/')[-1]}]({file_name})")

# 雷达图 - 基金产品

def product_radar(this_fund):
    this_scores = [[this_fund['分项合计-产品'].astype('float').round(2),
                    this_fund['盈利得分-产品'].astype('float').round(2),
                    this_fund['回撤控制得分-产品'].astype('float').round(2),
                    this_fund['业绩稳定性得分-产品'].astype('float').round(2),
                    this_fund['风险收益获取能力得分-产品'].astype('float').round(2),
                    this_fund['规模得分-产品'].astype('float').round(2)]]
    average_scores = [[(ranking['分项合计-产品'].sum()/len(ranking)).round(2),
                    (ranking['盈利得分-产品'].sum()/len(ranking)).round(2),
                    (ranking['回撤控制得分-产品'].sum()/len(ranking)).round(2),
                    (ranking['业绩稳定性得分-产品'].sum()/len(ranking)).round(2),
                    (ranking['风险收益获取能力得分-产品'].sum()/len(ranking)).round(2),
                    (ranking['规模得分-产品'].sum()/len(ranking)).round(2)]]
    radar = (
        Radar()
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="基金产品得分", min_=ranking['分项合计-产品'].min(), max_=ranking['分项合计-产品'].max()),
                opts.RadarIndicatorItem(name="盈利能力", min_=ranking['盈利得分-产品'].min(), max_=ranking['盈利得分-产品'].max()),
                opts.RadarIndicatorItem(name="回撤控制", min_=ranking['回撤控制得分-产品'].min(), max_=ranking['回撤控制得分-产品'].max()),
                opts.RadarIndicatorItem(name="业绩稳定性", min_=ranking['业绩稳定性得分-产品'].min(), max_=ranking['业绩稳定性得分-产品'].max()),
                opts.RadarIndicatorItem(name="风险收益获取能力", min_=ranking['风险收益获取能力得分-产品'].min(), max_=ranking['风险收益获取能力得分-产品'].max()),
                opts.RadarIndicatorItem(name="基金规模", min_=1, max_=5)
            ],
            
        )
        .add(series_name=f"{this_fund['基金简称']}（{this_fund['基金代码']}）", 
            data=this_scores,
            color="#CD0000",
            )
        .add(series_name="平均水平", 
            data=average_scores,
            color="#5CACEE",
            )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(selected_mode="multiple",
                                        pos_bottom='bottom',
                                        pos_left='left',),
            title_opts=opts.TitleOpts(title=f"基金产品得分", 
                                    pos_top='top',
                                    title_textstyle_opts=opts.TextStyleOpts(font_family='KaiTi', font_size=20)),
        )
    )
    return radar

# 布局

left, right = st.columns(2)
left.write("##### 【基金池】")

# 左侧布局

form = left.form("template_form")
fundcode = form.selectbox(
    "主动权益基金",
    options=product_tuple,
)
submit = form.form_submit_button("量化评分")

if submit:
    this_fund = ranking[ranking['基金代码']==fundcode].iloc[0, :]
    radar_product = product_radar(this_fund)
    streamlit_echarts.st_pyecharts(
        radar_product
    )

# 右侧布局

st.write("- 主动权益基金: Wind一级投资类型下的普通股票型、偏股混合型、平衡混合型、灵活配置型基金")
st.write("- 基金池: 仅考虑现任基金经理任职>2年、最新规模>2亿元、过去5期平均权益仓位不低于60%的初始基金(A份额)作为样本")


