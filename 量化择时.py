# -*- coding:utf-8 -*-
################################################
# 获得平安银行2022-09-01以来的macd数据
from jqlib.technical_analysis import *
security = '000001.XSHE'
DIF,DEA,_MACD =MACD(security_list='000001.XSHE',
                    check_date='2022-09-01',SHORT=12,LONG=26,MID=9)
print (DIF)
print (DEA)
print (_MACD)


################################################
# 获得多只股票的EMV指标
from jqlib.technical_analysis import *
security_list = ['000001.XSHE','000002.XSHE','601211.XSHG']
EMV,MAEMV = EMV(security_list,check_date='2022-09-01', N = 14, M = 9)
print (EMV)
print (MAEMV)


################################################
#UOS
#导入technical analysis库
from jqlib.technical_analysis import *
#定义股票池列表，可以是list
security='000001.XSHE'
#计算并输出UOS值
uos,mauos = UOS(security,check_date='2022-09-01',N1=7,N2=14,N3=28,M=6)
print(uos)
print(mauos)


################################################
# 获得多只股票的GDX指标值    中心线与股票线的关系  称为轨道线
from jqlib.technical_analysis import *
security_list = ['000001.XSHE','000002.XSHE','601211.XSHG']
JAX,YLX,ZCX = GDX(security_list,check_date='2022-09-01', N = 14, M = 9)
for stock in security_list:
    print (stock,'济安线的值为：',JAX[stock])
    print (stock,'压力线的值为：',YLX[stock])
    print (stock,'支撑线的值为：',ZCX[stock])


################################################
# 获得单只股票的JS指标值
from jqlib.technical_analysis import *
security = '000001.XSHE'
_JS,MAJS1,MAJS2,MAJS3 = JS(security, check_date='2022-09-01', N=5,M1=5,M2=10,M3=20)

print (_JS)
print (MAJS1)
print (MAJS2)
print (MAJS3)


################################################
# MA
# 获得一只股票三天的5、10、20日均线
from jqlib.technical_analysis import *
security = '000001.XSHE'
check_dates=['2022-09-05','2022-09-06','2022-09-07']
for check_date in check_dates:
    MA5 = MA(security, check_date=check_date, timeperiod = 5)
    MA10 = MA(security, check_date=check_date, timeperiod = 10)
    MA20 = MA(security, check_date=check_date, timeperiod = 20)

    print (check_date,'5日均线：',MA5[security])
    print (check_date,'10日均线：',MA10[security])
    print (check_date,'20日均线：',MA20[security])


################################################
# 获得一只股票三天的6、12、24、72日VMA均线
from jqlib.technical_analysis import *
security = '000001.XSHE'
check_dates=['2022-09-05','2022-09-06','2022-09-07']
for check_date in check_dates:
    _VMA6 = VMA(security, check_date=check_date, timeperiod = 6)
    _VMA12 =VMA(security, check_date=check_date, timeperiod = 12)
    _VMA24 =VMA(security, check_date=check_date, timeperiod = 24)
    _VMA72 =VMA(security, check_date=check_date, timeperiod = 72)
    print (check_date,'6日均线：',_VMA6[security])
    print (check_date,'12日均线：',_VMA12[security])
    print (check_date,'24日均线：',_VMA24[security])
    print (check_date,'72日均线：',_VMA72[security])


################################################
# 获得一只股票三天的KDJ指标值
from jqlib.technical_analysis import *
security = '000001.XSHE'
check_dates=['2022-09-05','2022-09-06','2022-09-07']
for check_date in check_dates:
    _K,_D,_J = KDJ(security, check_date=check_date, N=9,M1=3,M2=3)
    print(check_date,'K值为：',_K[security])
    print(check_date,'D值为：',_D[security])
    print(check_date,'J值为：',_J[security])


################################################
# 获得多只股票的RSI指标值
from jqlib.technical_analysis import *
security_list = ['000001.XSHE','000002.XSHE','601211.XSHG']
_RSI =RSI(security_list, check_date='2022-09-01', N1 = 6)
for stock in security_list:
    print (stock,'2022-09-01日RSI线的值为：',_RSI[stock])


################################################
# 获得单只股票的多日WR指标值
from jqlib.technical_analysis import *
security = '600031.XSHG'
check_dates=['2022-10-31','2022-11-01','2022-11-02','2022-11-03']
for check_date in check_dates:
    _WR,MAWR = WR(security, check_date=check_date, N=10,N1=3)
    print(check_date,'WR值为：',_WR[security])
    print(check_date,'MAWR值为：',MAWR[security])


################################################
# 获得一只股票三天的BOLL指标值

from jqlib.technical_analysis import *
security = '600031.XSHG'
check_dates=['2022-10-31','2022-11-01','2022-11-02','2022-11-03']
for check_date in check_dates:
    upper,middle,lower = Bollinger_Bands(security, check_date=check_date,timeperiod=20,nbdevup=2,nbdevdn=2)
    print(check_date,f'{security}的上轨道线值为：',upper[security])
    print(check_date,f'{security}的中轨道线值为：',middle[security])
    print(check_date,f'{security}的下轨道线值为：',lower[security])


################################################
# 获得单只股票的多日MIKE指标值

from jqlib.technical_analysis import *
security = '600031.XSHG'
check_dates=['2022-10-31','2022-11-01']
for check_date in check_dates:
    storl,midrl,wekrl,weksl,midsl,stosl=MIKE(security, check_date=check_date, timeperiod=10)
    print(check_date,'storl值为：',storl[security])
    print(check_date,'midrl值为：',midrl[security])
    print(check_date,'wekrl值为：',wekrl[security])
    print(check_date,'weksl值为：',weksl[security])
    print(check_date,'midsl值为：',midsl[security])
    print(check_date,'stosl值为：',stosl[security])


################################################
# 获得一只股票多日内的XS指标值

from jqlib.technical_analysis import *
security = '000001.XSHE'
check_dates=['2022-10-31','2022-11-01']
for check_date in check_dates:
    SUP,SDN,LUP,LDN=XS(security, check_date='2022-09-01',timeperiod=13)

    print(check_date,'SUP值为：',SUP[security])
    print(check_date,'SDN值为：',SDN[security])
    print(check_date,'LUP值为：',LUP[security])
    print(check_date,'LDN值为：',LDN[security])


################################################
# 获得多只股票多日的OBV指标值
from jqlib.technical_analysis import *
security_list = ['000001.XSHE','000002.XSHE','601211.XSHG']
check_dates=['2022-10-31','2022-11-01']
for check_date in check_dates:
    for security in security_list:
        _OBV=OBV(security, check_date=check_date,timeperiod=30)
        print(check_date,f'{security}的OBV值为：',_OBV[security])


################################################
# 获得多只股票的多日VOL指标值

from jqlib.technical_analysis import *
security_list = ['000001.XSHE','000002.XSHE']
check_dates=['2022-10-31','2022-11-01']
for check_date in check_dates:
    for security in security_list:
        _VOL,MAVOL1,MAVOL2=VOL(security, check_date='2022-09-01',M1=5,M2=10)
        print(check_date,f'{security}的VOL值为：',_VOL[security])
        print(check_date,f'{security}的MAVOL1值为：',MAVOL1[security])
        print(check_date,f'{security}的MAVOL2值为：',MAVOL2[security])







