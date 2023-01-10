
# Zhao Zifeng @ Peking University 

### TODO ###

file_name = 'https://github.com/ZhaZhaFon/ScoringRanking/files/10374068/results_20221231.xlsx'
#file_name = 'https://github.com/ZhaZhaFon/ScoringRanking/blob/master/results_20221231.csv?raw=true'
top = 100

### TODO ###

# 依赖

import numpy as np
import pandas as pd
import os
import time

import streamlit as st

from pyecharts.charts import *
from pyecharts import options as opts

# 标题

st.set_page_config(layout="centered", page_icon="🎓", page_title="")
st.title("基金量化打分 - 主动权益基金")
st.write(f"呈现结果源于: [{file_name.split('/')[-1]}]({file_name}) （仅展示前{top}名）")

# 数据

ranking = pd.read_excel(file_name, index_col=0).reset_index().rename(columns={"index": "基金代码"}).iloc[:top, :]
this_fund = ranking.iloc[0, :]

# 交互式可视化

from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def aggrid_interactive_table(df: pd.DataFrame):
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )
    options.configure_side_bar()
    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )
    return selection

import streamlit_echarts

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

while True:

    time.sleep(0.5)

    ## 交互式雷达图 - 基金产品/经理/公司维度

    radar_product = product_radar(this_fund)

    streamlit_echarts.st_pyecharts(
        radar_product
    )

    ## 交互式表格 - 基金量化打分结果

    selection = aggrid_interactive_table(df=ranking)

    if selection:
        st.write("You selected:")
        st.json(selection["selected_rows"])
        print(selection["selected_rows"])

    