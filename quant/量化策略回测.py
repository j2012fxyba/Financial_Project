import jqdata
import pandas as pd
from jqlib.technical_analysis import *


def initialize(context):
    # 设定基准（沪深300）
    set_benchmark('000300.XSHG')
    # 开启动态复权模式
    set_option('use_real_price', True)
    # 标的股票
    g.security = '000001.XSHE'
    # 设置macd默认值
    g.macd_yesterday = 0


#######进行操作的过程#######
def handle_data(context, data):
    security = g.security
    # 计算当天的macd值
    DIF, DEA, _MACD = MACD(security_list=security,
                           check_date=context.current_dt, SHORT=6, LONG=12, MID=9)
    # 获取当日现金
    cash = context.portfolio.cash
    # 如果昨天的macd为负，今日macd为正，则表示出现金叉
    if g.macd_yesterday < 0 and _MACD[security] > 0 and cash > 0:
        order_value(security, cash)
    # 如果昨天的macd为正，今日macd为负，则表示出现死叉
    elif g.macd_yesterday > 0 and _MACD[security] < 0 and \
            context.portfolio.positions[security].closeable_amount > 0:
        order_target(security, 0)

    # 记录当天的macd值，全仓买入时可以不用
    g.macd_yesterday = _MACD[security]


