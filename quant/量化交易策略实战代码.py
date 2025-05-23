# -*- coding:utf-8 -*-
################################################
#双均线量化交易策略
"""
双均线策略
金叉时买入，死叉时卖出
"""

def initialize(context):
    g.security = "000333.XSHE"
    g.short_count = 5
    g.long_count = 10
    g.unit = "1d"
    run_daily(market_open,time="every_bar")    # 每分钟交易
    
    
def market_open(context):
    #获取5日均线
    short_ma = get_ma(g.security,g.short_count,g.unit)
    #获取10日均线
    long_ma = get_ma(g.security,g.long_count,g.unit)
    
    #金叉买入
    if get_golden_signal(short_ma,long_ma):
        print(f"金叉买入,MA{g.short_count}={short_ma},MA{g.long_count}={long_ma}")
        order_target(g.security, 100)
    elif get_death_signal(short_ma,long_ma):
        print("卖出所有股票,MA{g.short_count}={short_ma},MA{g.long_count}={long_ma}")
        #卖出所有股票
        order_target(g.security, 0)
        
    
    

def get_ma(security:str,count:int,unit:str)->list:
    """
    计算移动平均值MA(count)
    """
    #获取count+1的收盘价
    df = attribute_history(security, count+1, unit, ["close"]) 
    
    #计算当前的ma
    now_ma = df[1:count+1]["close"].rolling(count).mean()[-1]
    #计算上次的ma
    pre_ma = df[:count]["close"].rolling(count).mean()[-1]
    return [pre_ma,now_ma]
    
    
def get_golden_signal(
    short_ma:list,
    long_ma:list
)->bool:
    """
    判断是否是金叉
    金叉：True
    """
    return (short_ma[0] < long_ma[0] and short_ma[1] >= long_ma[1])
    
def get_death_signal(
    short_ma:list,
    long_ma:list
)->bool:
    """
    判断是否是死叉
    死叉：True
    """
    return (short_ma[0] > long_ma[0] and short_ma[1] <= long_ma[1])
################################################
#KD指标量化交易策略实战
'''
超买超卖型技术指标，即随机指标KD
实现K在20左右向上交叉D时，则全仓买入
K在80左右向下交叉D时，全仓卖出
'''

import jqdata
from jqlib.technical_analysis import *

def initialize(context):
    """初始化函数"""
    # 设定基准
    set_benchmark('000300.XSHG')
    # 开启动态复权
    set_option('use_real_price', True)
    # 股票类每笔交易时的手续费是：
    # 买入时佣金万分之三
    # 卖出时佣金万分之三加千分之一的印税
    # 每笔交易最低扣5元钱
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        close_today_commission=0,
        min_commission=5
    ), type='stock')
    # 开盘前运行
    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG')
    # 开盘时运行
    run_daily(market_open, time='open', reference_security='000300.XSHG')
    # 收盘后运行
    run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')


def before_market_open(context):
    """开盘前运行函数"""
    # 输出运行时间
    log.info('before_market_open运行时间：' + str(context.current_dt.time()))
    # 交易股票
    g.security = '000001.XSHE'


def market_open(context):
    """开盘时运行函数"""
    # 输出运行时间
    log.info('market_open运行时间：' + str(context.current_dt.time()))
    security = g.security
    # 调用KD函数，获取该函数的K值和D值
    K1, D1 = KD(security, check_date=context.current_dt, N=9, M1=3, M2=3)
    # 取得当前的现金
    cash = context.portfolio.available_cash
    # 如果K在20左右向上交叉D时，则全仓买入
    if K1[security] >= 20 and K1[security] > D1[security]:
        # 记录这次买入
        log.info('买入股票 %s' % (security))
        # 用所有cash买入股票
        order_value(security, cash)
    # 如果K在80左右向下交叉D，并且目前有头寸，则全仓卖出
    elif K1[security] < 80 and K1[security] < D1[security] and context.portfolio.positions[
        security].closeable_amount > 0:
        # 记录这次卖出
        log.info('卖出股票 %s' % (security))
        # 卖出所有股票，使这只股票的最终持有量为0
        order_target(security, 0)


def after_market_close(context):
    """收盘后运行函数"""
    # 输出运行时间
    log.info('after_market_close运行时间：' + str(context.current_dt.time()))
    # 得到当天的所有成效记录
    trades = get_trades()
    for _trade in trades.values():
        log.info('成交记录：' + str(_trade))
    log.info('一天的交易结束，祝你心情愉快')


################################################
#MA-RSI量化交易策略
from jqdata import *
from jqlib.technical_analysis import *
import numpy as np
import pandas as pd


## 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    #设置开启避免未来数据模式
    set_option("avoid_future_data", True)        
    # True为开启动态复权模式，使用真实价格交易
    set_option('use_real_price', True) 
    # 设定成交量比例
    set_option('order_volume_ratio', 1)
    # 股票类交易手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    # 持仓数量
    g.stocknum = 10
    
    
    g.hold_cnt = 0
    
    # 开盘时运行
    run_daily(trade, time='14:50', reference_security='000300.XSHG')
    
# 选股
def check_stocks(context):
    # 获取当天时间
    now = context.current_dt
    # 创建买入股票池 
    g.buylist = []
    # 拉取除st、科创板、创业板、退市、次新(>200days)的所有股票
    security_list = get_all_stock(context,now,200)
    # 过滤跌停的股票
    # security_list = filter_limitdown_stock(context,security_list)
    # 筛选股票
    q = query(valuation.code).filter(
	    valuation.code.in_(security_list), 
	    valuation.market_cap > 500  # 市值大于500亿
	    ).order_by(
        indicator.inc_net_profit_annual.desc()    # 按净利润同比增长率降序排列
        )       
    security_list = list(get_fundamentals(q).code)
    
    # 获取现价
    h = get_bars(security_list, count = 1, unit = '1d',end_dt = now, fields = ['close'],include_now=True)
    # 获取MA200均线值
    MA200 = MA(security_list, check_date = now, timeperiod=200, unit = '1d', include_now = True)
    #取得RSI值
    RSI10 = RSI(security_list, check_date = now, N1 = 10)
    
    # 按条件筛选
    for security in security_list:
        MA_True = h[security]['close'] > MA200[security]    # 收盘价高于MA200
        RSI_True = RSI10[security] < 25      # RSI10小于30
        if MA_True and RSI_True:    # 两者都满足
            g.buylist.append(security)
            if len(g.buylist) == g.stocknum:
                break
    log.info('今日买入股票池：'+str(g.buylist))
    return g.buylist

# 拉取非st、非科创板、非创业板、非退市、非次新股 的所有股票
def get_all_stock(context,now,ndays):
    df = get_all_securities(types=['stock'], date=now)
    df = df[(~df['display_name'].str.contains("ST")) &
            (~df['display_name'].str.contains("退")) & 
            (~df['display_name'].str.contains("\*")) &
            ((df.index.str[0:3]!='300') &
            (df.index.str[0:3]!='688'))]
    return [str(stock) for stock in df.index if (context.current_dt.date()-df.loc[stock,'start_date']).days>ndays] #判断上市天数是否满足要求


# 交易
def trade(context):
    log.info('天数：'+str(g.hold_cnt))
    # 获取当天时间
    now = context.current_dt
    # 获取持仓股票
    holding_list = list(context.portfolio.positions.keys())
    # 获取持仓股票现价
    h = get_bars(holding_list, count = 1, unit = '1d',end_dt = now, fields = ['close'],include_now=True)
    # 按条件买卖
    if len(holding_list) == 0:  # 没有持仓，买入目标股票
        buy_list = check_stocks(context)
        for security in buy_list:  
            Cash = context.portfolio.cash/len(buy_list)
            order_value(security,Cash)
            g.hold_cnt = 1
            log.info('买入股票：'+str(security))
    elif  g.hold_cnt > 0 and g.hold_cnt < 11:   # 不足11天，筛选 RSI>40 或 下跌超过-5% 的股票卖出
        g.hold_cnt += 1
        for security in holding_list:
            RSI10 = RSI(security, check_date = now, N1 = 10)
            current_price = h[security]['close']    # 现价  
            cost = context.portfolio.positions[security].avg_cost   # 买入价
            if RSI10[security] > 40 or current_price < 0.95*cost:
                order_target_value(security, 0)
                log.info('卖出股票：'+str(security))
            else:
                break
    elif g.hold_cnt == 11:  # 达到11天，卖出持仓股票
        buy_list = check_stocks(context)
        for security in holding_list:   # 卖出股票，判断是否不在买入目标股票
            if security not in buy_list:
                order_target_value(security, 0)
                log.info('卖出股票：'+str(security))
                g.hold_cnt = 0
        for security in buy_list:   # 买入股票，判断是否不在持仓股票池
            if security not in holding_list:
                Cash = context.portfolio.cash/len(buy_list)
                order_value(security,Cash)
                g.hold_cnt = 1
                log.info('买入股票：'+str(security))
    else:
        log.info('出错啦！！')


################################################
#能量型指标量化交易策略
from jqdata import *
from jqlib.technical_analysis import *

#初始化函数
def initialize(context):
    #选定交易股票
    g.security = '000001.XSHE'
    #设定基准
    set_benchmark('000300.XSHG')
    #开启动态复权模式（真实价格）
    set_option('use_real_price',True)
    """
    设定交易费
    买入时佣金万分之三
    卖出时佣金万分之三加千分之一印花税
    每笔交易佣金最低扣5元
    """
    set_order_cost(OrderCost(close_tax=0.001,open_commission=0.0003,close_commission=0.0003,min_commission=5),type='stock')
    

#盘中运行函数
def handle_data(context,data):
    #计算能量指标
    security = g.security
    #计算情绪指标BRAR
    BR1,AR1 = BRAR(security,check_date=context.current_dt,N=26)
    #计算中间意愿指标CR
    CR1,MA1,MA2,MA3,MA4 = CR(security,check_date=context.current_dt,N=26,M1=10,M2=20,M3=40,M4=62)
    #计算成交量变异率指标VR
    VR1,MAVR1 = VR(security,check_date=context.current_dt,N=26,M=6)
    #取得当前现金
    cash = context.portfolio.cash
    
    #识别买入信号
    #若当前有余额，且AR<100、BR<100、BR<AR、CR<100、VR<100
    if AR1[security] < 100 and BR1[security] < 100 and BR1[security] < AR1[security] and CR1[security] < 100 and VR1[security]<100 and cash > 0:
        #买入股票
        order_value(security,cash)
        #记录日志
        log.info("买入股票%s" % (security))
    #识别卖出信号
    #若AR>150、BR>150、CR>150、VR>150,并且有持仓
    elif AR1[security] > 150 and BR1[security] > 150 and CR1[security] > 150 and VR1[security] > 150 and context.portfolio.positions[security].closeable_amount > 0:
        #全部卖出
        order_target(security,0)
        #记录日志
        log.info("卖出股票%s" % (security))
        
    
    
    
    
    




################################################
#BOLL指标量化交易策略实战
# 导入函数库
from jqdata import *
from jqlib.technical_analysis import *


# 初始化函数，设定基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5),
                   type='stock')

    g.security = '600000.XSHG'  # 航天彩虹
    g.k = 2  # 股票特性参数，即N的取值


# 盘中BOLl量化策略
def handle_data(context, data):
    # 获取该股票20日收盘价
    sr = attribute_history(g.security, 20)['close']
    # 取得过去20日的平均价格
    ma = sr.mean()
    # numpy和pandas的std()均可计算标准差
    # up线(压力线)：20日均线+N*SD(20日收盘价标准差)
    up = ma + g.k * sr.std()
    # down线(支撑线)：20日均线-N*SD(20日收盘价标准差)
    down = ma - g.k * sr.std()

    # 股票开盘价格
    p = get_current_data()[g.security].day_open
    # 取得当前的现金
    cash = context.portfolio.available_cash
    # portfolio.positions持仓标的信息
    if p < down and g.security not in context.portfolio.positions:
        # 跌破下限买入信号且没有持仓
        order_value(g.security, cash)
    elif p > up and g.security in context.portfolio.positions:
        # 涨破上限卖出信号且有持仓
        order_target(g.security, 0)  # 卖出所有股票,使这只股票的最终持有量为0
################################################
#新能源股票轮动量化交易策略实战
# 导入函数库
import jqdata
## 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 设定新能源指数作为基准
    set_benchmark('399808.XSHE')
    # True为开启动态复权模式，使用真实价格交易
    set_option('use_real_price', True)
    # 设定成交量比例
    set_option('order_volume_ratio', 1)
    # 股票类交易手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, \
    open_commission=0.0003, close_commission=0.0003,\
    close_today_commission=0, min_commission=5), type='stock')
    # 运行函数, 按周运行，在每周第一个交易日运行
    run_weekly(chenk_stocks, weekday=1, time='before_open') #选股
    run_weekly(trade, weekday=1, time='open') #交易



# 选股函数

def chenk_stocks(context):
    # 得到新能源指数成分股
    g.stocks = get_index_stocks('399808.XSHE')
    # 查询股票的市净率，并按照市净率升序排序
    if len(g.stocks) > 0:
        g.df = get_fundamentals(
            query(
                valuation.code,valuation.pb_ratio
                ).filter(
                    valuation.code.in_(g.stocks
                    )
                ).order_by(
                    valuation.pb_ratio.asc()
                )
            )
        # 找出最低市净率的一只股票
        g.code = g.df['code'][0]


# 交易函数
def trade(context):
    if len(g.stocks) > 0:
        code = g.code
    # 如持仓股票不是最低市净率的股票，则卖出
    for stock in context.portfolio.positions.keys():
        if stock != code:
            order_target(stock,0)
    # 持仓该股票
    if len(context.portfolio.positions) > 0:
        return
    else:
        order_value(code, context.portfolio.cash)

################################################
#低估值股票量化交易策略
'''
1.市净率小于1；
2.负债比例低于于市场平均值;
3.企业的流动资产至少是流动负债的1.2倍;
4.每月一次调仓；
5.可加入止损(十天HS300跌幅达10%清仓)；
'''
import jqdata


## 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 设定指数
    g.stockindex = '000300.XSHG'
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # True为开启动态复权模式，使用真实价格交易
    set_option('use_real_price', True)
    # 设定成交量比例
    set_option('order_volume_ratio', 1)
    # 股票类交易手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, \
                             open_commission=0.0003, close_commission=0.0003, \
                             close_today_commission=0, min_commission=5), type='stock')
    # 最大持仓数量
    g.stocknum = 5

    ## 自动设定调仓月份（如需使用自动，注销下段）
    f = 12  # 调仓频率
    g.Transfer_date = list(range(1, 13, 12 // f))
    
    #根据大盘止损
    run_daily(broader_stoploss, time='open') 

    ## 按月调用程序
    run_monthly(trade, monthday=20, time='open')



## 选股函数
def check_stocks(context):
    # 获取沪深成分股
    security = get_index_stocks(g.stockindex)

    Stocks = get_fundamentals(query(
        valuation.code,
        valuation.pb_ratio,
        balance.total_assets,
        balance.total_liability,
        balance.total_current_assets,
        balance.total_current_liability
    ).filter(
        valuation.code.in_(security),
        valuation.pb_ratio < 1,  # 市净率低于1
        balance.total_current_assets / balance.total_current_liability > 1.2  # 流动资产至少是流动负债的1.2倍
    ))

    # 计算股票的负债比例
    Stocks['Debt_Asset'] = Stocks['total_liability'] / Stocks['total_assets']
    # 获取负债比率的市场均值
    me = Stocks['Debt_Asset'].median()
    # 获取满足上述条件的股票列表
    Codes = Stocks[Stocks['Debt_Asset'] < me].code

    return list(Codes)


## 根据局大盘止损，具体用法详见dp_stoploss函数说明
def broader_stoploss(context):
    stoploss = bm_stoploss(kernel=2, n=3, threshold=0.1)
    if stoploss:
        if len(context.portfolio.positions) > 0:
            for stock in list(context.portfolio.positions.keys()):
                order_target(stock, 0)


## 大盘止损函数
def bm_stoploss(kernel=2, n=10, threshold=0.03):
    '''
    方法1：当大盘N日均线(默认60日)与昨日收盘价构成“死叉”，则发出True信号
    方法2：当大盘N日内跌幅超过阈值，则发出True信号
    '''
    # 止损方法1：根据大盘指数N日均线进行止损
    if kernel == 1:
        t = n + 2
        hist = attribute_history('000300.XSHG', t, '1d', 'close', df=False)
        temp1 = sum(hist['close'][1:-1]) / float(n)
        temp2 = sum(hist['close'][0:-2]) / float(n)
        close1 = hist['close'][-1]
        close2 = hist['close'][-2]
        if (close2 > temp2) and (close1 < temp1):
            return True
        else:
            return False
    # 止损方法2：根据大盘指数跌幅进行止损
    elif kernel == 2:
        hist1 = attribute_history('000300.XSHG', n, '1d', 'close', df=False)
        if ((1 - float(hist1['close'][-1] / hist1['close'][0])) >= threshold):
            return True
        else:
            return False


## 交易函数
def trade(context):
    # 获取当前月份
    months = context.current_dt.month
    # 如果当前月为交易月
    if months in g.Transfer_date:
        ## 获得Buylist
        Buylist = check_stocks(context)

        ## 卖出
        if len(context.portfolio.positions) > 0:
            for stock in context.portfolio.positions.keys():
                if stock not in Buylist:
                    order_target(stock, 0)

        ## 分配资金
        if len(context.portfolio.positions) < g.stocknum:
            Num = g.stocknum - len(context.portfolio.positions)
            Cash = context.portfolio.cash / Num
        else:
            Cash = 0

        ## 买入
        if len(Buylist) > 0:
            for stock in Buylist:
                if stock not in context.portfolio.positions.keys():
                    order_value(stock, Cash)
    else:
        return




################################################
# 大小盘轮动量化交易策略
# 导入函数库
from jqdata import *
from datetime import datetime
import math
import pandas as pd
import statsmodels.api as sm
import numpy as np
strBig='000300.XSHG'
strSmall='399006.XSHE'
strMarket='000047.XSHG'
index=[strBig,strSmall,strMarket]
etfBig='510300.XSHG'
etfSmall='159915.XSHE'
g.result={etfBig:0,etfSmall:0}
#获取当日信号
def get_signal(tradeDate):
    start_date=datetime.strptime(tradeDate,'%Y-%m-%d')-timedelta(days=1000)
    start_date=start_date.strftime('%Y-%m-%d')
    #获取数据
    data=get_price(index, start_date=start_date, end_date=tradeDate, 
               frequency='daily', fields='close', fq='pre')['close']
    data=data/data.shift(250)
    data.dropna(inplace=True)
    #计算RS
    for c in data.columns:
        if c!=strMarket:
            data[c]=data[c]-data[strMarket]+1
    data=data.drop(strMarket,1)
    for c in data.columns:
        data[c]=data[c].apply(lambda x:math.log(x,10))
    #计算RS的HP滤波
    diff=data[strBig]-data[strSmall]
    cycle, trend = sm.tsa.filters.hpfilter(diff, lamb=10000)
    #计算前20个数据的一阶导数及二阶导数
    t1=[]
    for pos in range(-20,0): 
        X=list(np.arange(20))
        X=sm.add_constant(X)
        est=sm.OLS(trend.iloc[pos-20:pos],X)
        est=est.fit()
        t1.append(est.params['x1'])#一阶导数
    X=list(np.arange(20))
    X=sm.add_constant(X)
    est1=sm.OLS(t1,X)
    est1=est1.fit()
    t2=est1.params[1]#二阶导数
    result={}
    #通过四象限结果计算交易信息，推导持仓比例
    if t1[-1]>0 and t2>0:
        result[etfBig]=1
        result[etfSmall]=0
    if t1[-1]>0 and t2<0:
        result[etfBig]=0.5
        result[etfSmall]=0.5
    if t1[-1]<0 and t2>0:
        result[etfBig]=0.5
        result[etfSmall]=0.5
    if t1[-1]<0 and t2<0:
        result[etfBig]=0
        result[etfSmall]=1
    return result
# 初始化函数，设定基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 输出内容到日志 log.info()
    log.info('初始函数开始运行且全局只运行一次')
    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')

    run_monthly(market_open,monthday=1)

## 开盘时运行函数
def market_open(context):
    result=get_signal(context.previous_date.strftime('%Y-%m-%d'))
    if not (g.result[etfBig]==result[etfBig] and g.result[etfSmall]==result[etfSmall]):
        order_target_value(etfBig,0)
        order_target_value(etfSmall,0)
        cash = context.portfolio.available_cash
        order_target_value(etfBig,result[etfBig]*cash)
        order_target_value(etfSmall,result[etfSmall]*cash)
        g.result=result


################################################
#逆三因子量化交易策略
#逆三因子量化交易策略
#导入函数库
from jqdata import *
from jqlib.alpha191 import *
from jqfactor import get_factor_values
import pandas as pd
import numpy as np
from jqfactor import standardlize,winsorize

#初始化函数
def initialize(context):
    #设定基准
    set_benchmark('000300.XSHG')
    #开启动态复权模式
    set_option('use_real_price',True)
    #输入日志
    log.info('初始函数开始运行且全局只运行一次')
    
    g.securities = []
    g.stock_list = []
    
    """
    设定股票交易费
    买入时佣金万分之三
    卖出时佣金万分之三加千分之一印花税
    每笔佣金最低不能低于5元
    """
    set_order_cost(OrderCost(close_tax=0.001,open_commission=0.0003,close_commission=0.0003,\
                    min_commission=5),type='stock')
    
    #开盘前运行
    run_daily(before_market_open,time='before_open',reference_security='000300.XSHG')
    #开盘时运行
    run_daily(market_open,time='open',reference_security='000300.XSHG')
    #收盘后运行
    run_daily(after_market_close,time='after_close',reference_security='000300.XSHG')

#开盘前运行函数
def before_market_open(context):
    #每月第一个交易日
    if context.current_dt.month != context.previous_date.month:
        #获取全市场股票，过滤ST
        stocks = list(get_all_securities(types=['stock'], date=context.current_dt).index)
        stocks_st = pd.DataFrame()
        stocks_st['stocks'] = stocks
        
        stocks_st['st'] = get_extras('is_st',stocks, end_date=context.previous_date,count=1).iloc[0,:].values
        stocks_1 = list(stocks_st.loc[stocks_st.st==0,'stocks'].values)
        
        #获取size因子，标准化并去尾
        size_0 = get_factor_values(stocks_1,['size'],end_date=context.previous_date,count=1)
        sizes = size_0['size']
        stock_pd = pd.DataFrame()
        stock_pd['stocks'] = sizes.columns
        stock_pd['size'] = winsorize(standardlize(sizes.iloc[0,:].values,inf2nan=True,axis=1),\
                            qrange=[0.05,0.93],inclusive=True,inf2nan=True,axis=1)
        stock_pd.sort_values(by='size',ascending=True,inplace=True) 
        stock_list = list(stock_pd.iloc[:200,:].stocks.values)
        g.stock_list = stock_list
        
        #计算全市场逆三因子
        stocks = g.stock_list
        
        bp0 = get_factor_values(stocks,['residual_volatility','VROC12','size'],end_date=context.previous_date,\
              count=1)
        
        bp = bp0['size']
        
        res = bp0['residual_volatility']
        
        vroc = bp0['VROC12']
        vroc.fillna(0,inplace=True)
        
        bp2 = pd.DataFrame()
        bp2['stocks'] = bp.columns
        
        
        #标准化并去尾逆三因子，计算zscore
        bp2['size'] = winsorize(standardlize(bp.iloc[0,:].values,inf2nan=True,axis=1),\
                            qrange=[0.05,0.93],inclusive=True,inf2nan=True,axis=1)
        bp2['residual_volatility'] = winsorize(standardlize(res.iloc[0,:].values,inf2nan=True,axis=1),\
                            qrange=[0.05,0.93],inclusive=True,inf2nan=True,axis=1)   
        bp2['VROC12'] =  winsorize(standardlize(vroc.iloc[0,:].values,inf2nan=True,axis=1),\
                            qrange=[0.05,0.93],inclusive=True,inf2nan=True,axis=1)
        bp2['zscore'] = bp2['residual_volatility'] + bp2['VROC12'] + bp2['size']
        
        #获取排名前50的股票
        bp2.sort_values(by='zscore',ascending=True,inplace=True)
        bp2 = bp2.iloc[:50,:]
        
        g.securities = list(bp2.stocks.values)
    
#开盘时运行函数
def market_open(context):
    securities = g.securities
    #根据逆三因子的结果进行交易
    for security in context.portfolio.positions:
        if security not in set(securities):
            order_target(security,0)
    cash = context.portfolio.available_cash
    for security in securities:
        if context.portfolio.positions[security].closeable_amount == 0 :
            order_value(security, cash/50)

#收盘后运行函数
def after_market_close(context):
    #打印每日成交记录
    trades = get_trades()
    for _trade in trades.values():
        log.info('成交记录：'+str(_trade))
    log.info('一天结束')
    log.info('#####################################################################')
    
        
        
        
        
        


    
    
    
    
    
    
    
                    
