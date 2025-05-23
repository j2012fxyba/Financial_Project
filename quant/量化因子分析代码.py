# -*- coding:utf-8 -*-
################################################
# 10-2
# 导入函数库
import pandas
from jqfactor import Factor, analyze_factor
warnings.filterwarnings('ignore')


class MA10(Factor):
    # 因子名称为“ma10”
    name = 'ma10'
    # 最长时间窗口为10天
    max_window = 10

    # 来设置依赖的基础因子（收盘价）
    dependencies = ['close']

    def calc(self, data):
        return data['close'][-10:].mean()


# 使用自定义因子的类进行单因子分析
far = analyze_factor(factor=MA10, start_date='2022-01-01', end_date='2022-03-01', weight_method='mktcap',
                     universe='000300.XSHG', industry='jq_l1', quantiles=8, periods=(1, 5, 10))

# 分析结束后通过不同属性获取数据
far.ic_monthly  # 月度信息系数


################################################
# 10-3
from jqfactor import analyze_factor
from jqfactor import Factor

#自定义因子的类
class MA5(Factor):

    name = 'ma5'
    max_window = 5
    dependencies = ['close']

    def calc(self, data):
        return data['close'][-5:].mean()

#使用自定义因子的类进行单因子分析
far = analyze_factor(factor=MA5, start_date='2022-01-01', end_date='2022-03-01', weight_method='mktcap', universe='000300.XSHG', industry='jq_l1', quantiles=8, periods=(1,5,10))

# 绘制图表
far.create_full_tear_sheet(demeaned=False, group_adjust=False, by_group=False, turnover_periods=None, avgretplot=(5, 15), std_bar=False)


################################################
# 10-4
# 导入函数库
from jqfactor import Factor
import numpy as np 

class ALPHA013(Factor):
    # 设置因子名称
    name = 'alpha013'
    # 设置获取数据的时间窗口长度
    max_window = 1
    # 设置依赖的数据
    dependencies = ['high','low','volume','money']

    # 计算因子的函数， 需要返回一个 pandas.Series, index 是股票代码，value 是因子值
    def calc(self, data):

    # 最高价的 dataframe ， index 是日期， column 是股票代码
        high = data['high']

        # 最低价的 dataframe ， index 是日期， column 是股票代码
        low = data['low']

        #计算 vwap
        vwap = data['money']/data['volume']

        # 返回因子值， 这里求平均值是为了把只有一行的 dataframe 转成 series
        return (np.power(high*low,0.5) - vwap).mean()

#使用自定义因子的类进行单因子分析
far = analyze_factor(factor=ALPHA013, start_date='2022-01-01', end_date='2022-03-01', weight_method='mktcap', universe='000300.XSHG', industry='jq_l1', quantiles=8, periods=(1,5,10))

# 绘制图表
far.create_full_tear_sheet(demeaned=False, group_adjust=False, by_group=False, turnover_periods=None, avgretplot=(5, 15), std_bar=False)


################################################
# 10-5
# 基本面因子应用实例（首席质量因子）
from jqfactor import Factor


class mygross(Factor):
    # 设置因子名称
    name = 'mygross'
    # 设置获取数据的时间窗口长度
    max_window = 1
    # 设置依赖的数据
    dependencies = ['total_operating_revenue', 'total_operating_cost', 'total_assets']

    # 计算因子的函数，需要返回一个pandas.Series, index是股票代码， value是因子值
    def calc(self, data):
        # 获取单季度的营业总收入数据,index是日期，column是股票代码，value是营业总收入
        total_operating_revenue = data['total_operating_revenue']
        # 获取单季度的营业总成本数据
        total_operating_cost = data['total_operating_cost']
        # 获取总资产
        total_assets = data['total_assets']
        # 计算gross_profitability
        gross_profitability = (total_operating_revenue - total_operating_cost) / total_assets
        # 由于gross_ profitability 是一个一行n列的dataframe, 可以直接求mean转成serles
        return gross_profitability.mean()
    # 使用自定义因子的类进行单因子分析


far = analyze_factor(factor=mygross, start_date='2022-01-01', end_date='2022-03-01', weight_method='mktcap',
                     universe='000300.XSHG', industry='jq_l1', quantiles=8, periods=(1, 5, 10))

# 绘制图表
far.create_full_tear_sheet(demeaned=False, group_adjust=False, by_group=False, turnover_periods=None,
                           avgretplot=(5, 15), std_bar=False)

