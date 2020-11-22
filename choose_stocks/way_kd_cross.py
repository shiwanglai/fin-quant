"""
download the data
"""
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import data_dl_tushare as dl
plt.style.use('fivethirtyeight')

rsv_days = 4
#k_days = 3
#d_days = 3
def calc_rsv(dfx):
    close = dfx.close
    high = dfx.high
    low = dfx.low
    date = close.index.to_series()

    ndate = len(dfx)
    print(ndate)
    print("date")
    print(date)
    #period_high = pd.Series(np.zeros(ndate - 8), index = dfx.index[8:])
    period_high = pd.Series(np.zeros(ndate - (rsv_days - 1)), index = dfx.index[(rsv_days - 1):])
    print("peroid high", type(period_high))
    print(period_high.head())
    #print("type np zero(5)", type(np.zeros(5)))
    #print(np.zeros(5))
    #print("type np zero(2, 3)", type(np.zeros((2, 3))))
    #print(np.zeros((2, 3)))
    #period_low = pd.Series(np.zeros(ndate - 8), index = dfx.index[8:])
    period_low = pd.Series(np.zeros(ndate - (rsv_days - 1)), index = dfx.index[(rsv_days - 1):])
    #RSV = pd.Series(np.zeros(ndate - 8), index = dfx.index[8:])
    RSV = pd.Series(np.zeros(ndate - (rsv_days - 1)), index = dfx.index[(rsv_days - 1):])

    #print("RSV for")
    for j in range ((rsv_days - 1), ndate):
        # 4 days, 0/1/2/3
        period = date[j - (rsv_days - 1) : j + 1]
        i = date[j]
        #print("type peroid", type(period))
        #print(period)
        #print(high[period])
        #return

        period_high[i] = high[period].max()
        period_low[i]  = low[period].min()
        # the RSV
        RSV[i] = 100 * (close[i] - period_low[i]) / (period_high[i] - period_low[i])
        period_high.name = 'period high'
        period_low.name  = 'period low'
        RSV.name = 'RSV'
        #print(j, i, RSV[i])

    return RSV

    '''
    # draw RSV
    plt.rcParams['font.sans-serif'] = ['SimHei']
    close1 = close['2020']
    RSV1 = RSV['2020']
    C1_RSV = pd.DataFrame([close1, RSV1]).transpose()
    C1_RSV.plot(subplots = True,
            title = 'Raw SV', figsize = (16, 8))
    plt.show()
    '''

def calc_K(dfx, RSV):
    close = dfx.close
    date = close.index.to_series()
    RSV1 = pd.Series(50, index = date[rsv_days - 2 : rsv_days - 1]).append(RSV)
    RSV1.name = 'RSV'
    print("RSV1 len", len(RSV1))
    print("RSV1 head", RSV1.head(10))
    print("RSV1 tail", RSV1.tail(10))
    print("RSV len", len(RSV))
    print("RSV head", RSV.head(10))
    print("RSV tail", RSV.tail(10))
    #print("date", date.head())
    #print('date[1:3]', date[1:3].head())

    # calc K
    KValue = pd.Series(0.0, index = RSV1.index)
    KValue[0] = 50
    #for i in range(1, len(RSV1) - 2):
    #for i in range(1, len(RSV1)):  # should be this, but lack 2 elements
    for i in range(1, len(RSV1)):
        KValue[i] = 2 / 3 * KValue[i - 1] + RSV1[i] / 3
    KValue.name = 'KValue'

    return KValue

def calc_D(dfx, RSV, KValue):
    close = dfx.close
    date = close.index.to_series()
    #RSV1 = pd.Series([50, 50], index = date[1:3]).append(RSV)
    RSV1 = pd.Series(50, index = date[rsv_days - 2 : rsv_days - 1]).append(RSV)
    RSV1.name = 'RSV'

    # calc D
    DValue = pd.Series(0.0, index = RSV1.index)
    DValue[0] = 50
    #for i in range(1, len(RSV1) - 2):
    for i in range(1, len(RSV1)):  # should be this, but lack 2 elements
        DValue[i] = 2 / 3 * DValue[i - 1] + KValue[i] / 3
    DValue.name = 'DValue'

    return DValue

def draw_kd(dfx, RSV, KValue, DValue):
    KValue = KValue[1:]
    DValue = DValue[1:]
    close = dfx.close

    # draw KD
    plt.figure(figsize=(16, 12))
    #plt.rcParams['font.family'] = ['SimHei']
    plt.subplot(211)
    plt.title('WLY close price')
    plt.plot(close['2020'])
    print("close type", type(close))
    print(close.head())
    print("close[2020] type", type(close['2020-02']))
    print(close['2020-02'].head())
    plt.subplot(212)
    plt.title('WLY RSV && KD')
    plt.plot(RSV['2020'])
    plt.plot(KValue['2020'], linestyle = 'dashed', label = 'K')
    plt.plot(DValue['2020'], linestyle = 'dashed', label = 'D')
    plt.legend(loc='best')
    plt.show()

def buy_sell(dfx, KValue, DValue, RSV):
    sig_price_buy = []
    sig_price_sell = []
    flag = 0
    param = 0
    param2 = 1.10

    close = dfx.close
    print('close type', type(close))
    print(close.head())

    # data to buy && sell
    closedf = close.to_frame()
    print('closedf type', type(closedf))
    print(closedf.head())
    #print(closedf.head())
    KValuedf = KValue.to_frame()
    print('KValuedf type', type(KValuedf))
    print(KValuedf.head())
    DValuedf = DValue.to_frame()
    #print(DValuedf.head())

    data = pd.DataFrame()
    data['close'] = closedf['close']
    data['k'] = KValuedf['KValue']
    data['d'] = DValuedf['DValue']
    data['rsv'] = RSV

    # keep the later
    data = data[145:]

    '''
    # fill the previous unused days
    for i in range(rsv_days):
        sig_price_buy.append(np.nan)
        sig_price_sell.append(np.nan)

    # fill the previous unused days
    #for i in range (rsv_days, len(data)):
    '''
    #for i in range(30):
    for i in range(len(data)):
        if data['k'][i] > data['d'][i] * param2:
            if flag != 1:
                sig_price_buy.append(data['close'][i - param])
                sig_price_sell.append(np.nan)
                flag = 1
                #print("%d buy k=%f(%f) d=%f c=%f" % (i, data['k'][i], data['k'][i] * param2, data['d'][i], data['close'][i]))
            else:
                sig_price_buy.append(np.nan)
                sig_price_sell.append(np.nan)
                #print("%d nan" % (i))
        elif data['k'][i] * param2 < data['d'][i]:
            if flag != 0:
                sig_price_buy.append(np.nan)
                sig_price_sell.append(data['close'][i - param])
                flag = 0
                #print("%d sell k=%f(%f) d=%f c=%f" % (i, data['k'][i], data['k'][i] * param2, data['d'][i], data['close'][i]))
            else:
                sig_price_buy.append(np.nan)
                sig_price_sell.append(np.nan)
                #print("%d nan" % (i))
        else:
            sig_price_buy.append(np.nan)
            sig_price_sell.append(np.nan)
            #print("%d nan" % (i))

    data['Buy'] = sig_price_buy
    data['Sell'] = sig_price_sell

    data.to_csv("buy_sell_datas.csv")

    #return (sig_price_buy, sig_price_sell)
    print(len(data))
    print(data.head())
    print(data.tail())
    return data

def draw_buy_sell(dfx, data):
    '''
    data = pd.DataFrame()
    data['Buy'] = bs[0]
    data['Sell'] = bs[1]
    data.index = dfx.index
    print("data bs")
    print(data.head())
    #data.to_csv("bs_data.csv")
    '''

    plt.figure(figsize=(12,6))
    plt.plot(dfx['close'], label = 'WLY', alpha = 0.3)
    plt.scatter(data.index, data['Buy'], label = 'Buy', marker = '^', color = 'green')
    plt.scatter(data.index, data['Sell'], label = 'Sell', marker = 'v', color = 'red')

    plt.title('Buy Sell Signals')
    plt.xlabel('2020-01-01 - 2020-12-31')
    plt.ylabel('Close Price')
    plt.legend(loc='lower left')
    plt.show()

def benifit_sum(data):
    print("Begin money")
    plus = 0
    minus = 0
    start = 100000
    print(start)

    '''
    data = pd.DataFrame()
    data['Buy'] = bs[0]
    data['Sell'] = bs[1]
    '''
    # dfresult
    dfresult = data[(pd.notna(data.Buy) | pd.notna(data.Sell))]
    #print(dfresult.head())
    dfresult['newcol'] = dfresult.Sell.shift(-1)
    dfresult = dfresult[(pd.isna(dfresult.Sell))]
    dfresult['pct'] = (dfresult.newcol - dfresult.Buy) / dfresult.Buy

    for i in dfresult['pct'].tolist()[: -1]:
        if i < 0:
            print(1 + i)
            start = start * (1 + i)
            print ("Current lost, lost %0.2f, Current money is %0.2f" % (1 + i, start))
            minus += 1
        else:
            print(1 + i)
            start = start * (1 + i)
            print ("Current win, win %0.2f, Current money is %0.2f" % (1 + i, start))
            plus += 1

        i = 0

    print("Strataged Money")
    print("%0.2f" % (start))
    var2 = ((start - 100000) / 100000) * 100
    print("The benifit rate %0.2f%% " % (var2))

    print("The total win %d  lose %d" % (plus, minus))


def do_kdj():
    # fxyy, 600196
    # wly,  000858
    # btjc, 603068
    # xagf, 600596
    #df_stk = dl.read_data_from_file('600196', start='2019-06-01')
    #df_stk = dl.read_data_from_file('600196')
    #df_stk = dl.read_data_from_file('000858')
    #df_stk = dl.read_data_from_file('603068')
    #df_stk = dl.read_data_from_file('600596', start='2019-06-01')
    #df_stk = dl.read_data_from_file('600596')
    df_stk = dl.read_data_from_file('USDT-BTC')
    print(df_stk.head(10))
    #print(df_stk.tail())
    #draw_data(df_stk)

    # calc rsv
    RSV = calc_rsv(df_stk)
    print("RSV...")
    print(RSV.head(10))
    print(RSV.tail(10))
    # calc K
    KValue = calc_K(df_stk, RSV)
    # calc D
    DValue = calc_D(df_stk, RSV, KValue)
    print("KValue...")
    print(KValue.head(10))
    print("DValue...")
    print(DValue.head(10))
    # plot cross
    #draw_kd(df_stk, RSV, KValue, DValue)

    # draw buy sell signal
    data = buy_sell(df_stk, KValue, DValue, RSV)
    draw_buy_sell(df_stk, data)

    # benifit
    benifit_sum(data)


if __name__ == '__main__':
    do_kdj()

