
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
options_df = ranking['基金代码'] + ' ' + ranking['基金简称']
product_tuple = tuple(ranking['基金代码'].tolist())
manager_tuple = tuple(ranking['基金经理'].tolist())
company_tuple = tuple(ranking['基金公司'].tolist())
options_tuple = tuple(options_df.iloc[:, 0].tolist())
st.write(f"`#` 加载完毕, 呈现结果基于量化评分排名: [{file_name.split('/')[-1]}]({file_name})")

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
    radar_product = (
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
    return radar_product

# 雷达图 - 基金经理

def manager_radar(this_fund):
    this_scores = [[this_fund['分项合计-经理'].astype('float').round(2),
                    this_fund['盈利得分-经理'].astype('float').round(2),
                    this_fund['风控得分-经理'].astype('float').round(2),
                    this_fund['规模得分-经理'].astype('float').round(2),
                    this_fund['投资经验得分-经理'].astype('float').round(2)]]
    average_scores = [[(ranking['分项合计-经理'].sum()/len(ranking)).round(2),
                       (ranking['盈利得分-经理'].sum()/len(ranking)).round(2),
                       (ranking['风控得分-经理'].sum()/len(ranking)).round(2),
                       (ranking['规模得分-经理'].sum()/len(ranking)).round(2),
                       (ranking['投资经验得分-经理'].sum()/len(ranking)).round(2)]]
    radar_manager = (
        Radar()
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="基金经理得分", min_=ranking['分项合计-经理'].min(), max_=ranking['分项合计-经理'].max()),
                opts.RadarIndicatorItem(name="盈利能力", min_=ranking['盈利得分-经理'].min(), max_=ranking['盈利得分-经理'].max()),
                opts.RadarIndicatorItem(name="风险控制", min_=ranking['风控得分-经理'].min(), max_=ranking['风控得分-经理'].max()),
                opts.RadarIndicatorItem(name="管理规模", min_=1, max_=5),
                opts.RadarIndicatorItem(name="投资经验", min_=1, max_=5)
            ],
            
        )
        .add(series_name=f"{this_fund['基金经理']}", 
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
                                        pos_bottom='bottom'),
            title_opts=opts.TitleOpts(title=f"基金经理得分", 
                                      pos_top='top', 
                                      pos_left='left',
                                      title_textstyle_opts=opts.TextStyleOpts(font_family='KaiTi', font_size=20)),
        )
    )
    return radar_manager

# 雷达图 - 基金公司

def company_radar(this_fund):
    this_scores = [[this_fund['分项合计-公司'].astype('float').round(2),
                    this_fund['短期业绩得分-公司'].astype('float').round(2),
                    this_fund['长期业绩得分-公司'].astype('float').round(2)]]
    average_scores = [[(ranking['分项合计-公司'].sum()/len(ranking)).round(2),
                       (ranking['短期业绩得分-公司'].sum()/len(ranking)).round(2),
                       (ranking['长期业绩得分-公司'].sum()/len(ranking)).round(2)]]
    radar_company = (
        Radar()
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="基金公司得分", min_=ranking['分项合计-公司'].min(), max_=ranking['分项合计-公司'].max()),
                opts.RadarIndicatorItem(name="短期业绩水平", min_=ranking['短期业绩得分-公司'].min(), max_=ranking['短期业绩得分-公司'].max()),
                opts.RadarIndicatorItem(name="长期业绩水平", min_=ranking['长期业绩得分-公司'].min(), max_=ranking['长期业绩得分-公司'].max())
            ],
            
        )
        .add(series_name=f"{this_fund['基金公司']}", 
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
                                        pos_bottom='bottom'),
            title_opts=opts.TitleOpts(title=f"基金公司得分", 
                                      pos_top='top', 
                                      pos_left='left',
                                      title_textstyle_opts=opts.TextStyleOpts(font_family='KaiTi', font_size=20)),
        )
    )
    return radar_company

# 布局

left, right = st.columns(2)

# 左侧布局

left.write("##### 【基金池】")
form_left = left.form("template_form")
ans = form_left.selectbox(
    label="主动权益基金",
    options=options_tuple,
)

radar_type = form_left.radio(
    label="量化评分维度",
    options=["基金产品", "基金经理", "基金公司"],
)
submit = form_left.form_submit_button("量化评分")

# 右侧布局

fundcode = ans.split(' ')[0]
#fundname = ans.split(' ')[1].split('/')[0]

right.write("##### 【基本信息】")
#right.write(f'- 基金产品: {fundname}({fundcode})')

# 提交

if submit:
    this_fund = ranking[ranking['基金代码']==fundcode].iloc[0, :]
    radar_product = product_radar(this_fund)
    radar_manager = manager_radar(this_fund)
    radar_company = company_radar(this_fund)
    if radar_type == "基金产品":
        streamlit_echarts.st_pyecharts(radar_product)
    if radar_type == "基金经理":
        streamlit_echarts.st_pyecharts(radar_manager)
    if radar_type == "基金公司":
        streamlit_echarts.st_pyecharts(radar_company)

# 排名表格

st.write("##### 【量化评分排名】")
ranking.iloc[:, 6:] = ranking.iloc[:, 6:].astype('float').round(2)
st.dataframe(ranking)

# 备注

st.write("- 数据来源: Wind")
st.write("- 主动权益基金: Wind一级投资类型下的普通股票型、偏股混合型、平衡混合型、灵活配置型基金")
st.write("- 基金池: 仅考虑现任基金经理任职>2年、最新规模>2亿元、过去5期平均权益仓位不低于60%的初始基金(A份额)作为样本")
