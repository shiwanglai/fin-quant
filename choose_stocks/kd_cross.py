"""
download the data
"""
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def get_data():
    df1 = pd.read_csv('~/dev/data/000858.csv')

    # format to Y-m-d
    df1.index = df1.iloc[:,0]
    df1.index = pd.to_datetime(df1.index, format='%Y-%m-%d')
    df1 = df1.iloc[:,1:]

    # get 1 year data
    df1 = df1['2020-12-30':'2020-01-01']
    #print(df1.head())
    print(df1.tail())

    return df1

def draw_data():
    # plot it
    plt.figure(figsize=(12,6))
    #print(df1['close'])
    plt.plot(df1['close'], label = 'WLY')
    plt.title('Price')
    plt.xlabel('2020-01-01 - 2020-12-31')
    plt.ylabel('Close Price')
    plt.legend(loc='upper left')
    plt.show()

def calc_rsv():
    df1 = get_data()
    close = df1.close
    high = df1.high
    low = df1.low
    date = close.index.to_series()
    #print(date)

    ndate = len(df1)
    print(ndate)
    period_high = pd.Series(np.zeros(ndate - 8), \
            index = df1.index[8:])
    period_low = pd.Series(np.zeros(ndate - 8), \
            index = df1.index[8:])
    RSV = pd.Series(np.zeros(ndate - 8), \
            index = df1.index[8:])

    for j in range (3, ndate):
        period = date[j - 3 : j + 1]
        i = date[j]
        #print(j)
        #print(peroid)
        #print(high)
        #print(high[period].max())

        period_high[i] = high[period].max()
        period_low[i]  = low[period].min()
        # the RSV
        RSV[i] = 100 * (close[i] - period_low[i]) \
                / (period_high[i] - period_low[i])
        period_high.name = 'period high'
        period_low.name  = 'period low'
        RSV.name = 'RSV'
        #print("=====")

    #print(RSV)
    #print(RSV['2020']) # not a sequences

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

    RSV1 = pd.Series([50, 50], index = date[1:3]).append(RSV)
    RSV1.name = 'RSV'
    print(RSV1.head())

    # calc K
    KValue = pd.Series(0.0, index = RSV1.index)
    KValue[0] = 50
    #for i in range(1, len(RSV1)):  # should be this, but lack 2 elements
    for i in range(1, len(RSV1) - 2):
        KValue[i] = 2 / 3 * KValue[i - 1] + RSV[i] / 3
    KValue.name = 'KValue'
    print(KValue.head())

    # calc D
    DValue = pd.Series(0.0, index = RSV1.index)
    DValue[0] = 50
    #for i in range(1, len(RSV1)):  # should be this, but lack 2 elements
    for i in range(1, len(RSV1) - 2):
        DValue[i] = 2 / 3 * DValue[i - 1] + KValue[i] / 3
    DValue.name = 'DValue'
    print(DValue.head())

    KValue = KValue[1:]
    DValue = DValue[1:]

    # draw KD
    plt.figure(figsize=(16, 12))
    plt.rcParams['font.family'] = ['SimHei']
    plt.subplot(211)
    plt.title('WLY close price')
    plt.plot(close['2020'])
    plt.subplot(212)
    plt.title('WLY RSV && KD')
    plt.plot(RSV['2020'])
    plt.plot(KValue['2020'], linestyle = 'dashed', label = 'K')
    plt.plot(DValue['2020'], linestyle = 'dashed', label = 'D')
    plt.legend(loc='best')
    plt.show()

    # data to buy && sell
    closedf = close.to_frame()
    print(closedf.head())
    KValuedf = KValue.to_frame()
    print(KValuedf.head())
    DValuedf = DValue.to_frame()
    print(DValuedf.head())

    data = pd.DataFrame()
    data['close'] = closedf['close']
    data['k'] = KValuedf['KValue']
    data['d'] = DValuedf['DValue']

    # dfresult
    dfresult = data[(pd.notna(data.Buy) | pd.notna(data.Sell))]
    print(dfresult.head())
    dfresult['newcol'] = dfresult.Sell.shift(-1)
    dfresult = dfresult[(pd.isna(dfresult.Sell))]
    dfresult['pct'] = (dfresult.newcol - dfresult.Buy) / dfresult.Buy

def buy_sell(data):
    sig_price_buy = []
    sig_price_sell = []
    flag = -1
    param = 0
    param2 = 1.10

    for i in range(len(data)):
        if data['k'][i] * param2 > data['d'][i]:
            if flag != 1:
                sig_price_buy.append(data['close'][i - param])
                sig_price_sell.append(np.nan)
                flag = 1
            else:
                sig_price_buy.append(np.nan)
                sig_price_sell.append(np.nan)
        elif data['k'][i] * param2 < data['d'][i]:
            if flag != 0:
                sig_price_buy.append(np.nan)
                sig_price_sell.append(data['close'][i - param])
                flag = 0
            else:
                sig_price_buy.append(np.nan)
                sig_price_sell.append(np.nan)
        else:
            sig_price_buy.append(np.nan)
            sig_price_sell.append(np.nan)

    return (sig_price_buy, sig_price_sell)

def draw_buy_sell(data):
    buy_sell = buy_sell(data)
    data['Buy'] = buy_sell[0]
    data['Sell'] = buy_sell[1]

    plt.figure(figsize=(12,6))
    plt.plot(df1['close'], label = 'WLY', alpha = 0.3)
    plt.scatter(data.index, data['Buy'], label = 'Buy', marker = '^', color = 'green')
    plt.scatter(data.index, data['Sell'], label = 'Sell', marker = 'v', color = 'red')

    plt.title('Buy Sell Signals')
    plt.xlabel('2020-01-01 - 2020-12-31')
    plt.ylabel('Close Price')
    plt.legend(loc='lower left')
    plt.show()

def benifit_sum(dfresult):
    print("Begin money")
    plus = 0
    minus = 0
    start = 100000
    print(start)

    for i in dfresult['pct'].to_list()[: -1]:
        if i < 0:
            print(1 + i)
            start = start * (1 * i)
            print ("Current lost, lost %0.2f, Current money is %0.2f" % (1 + i, start))
            minus += 1
        else:
            print(1 + i)
            start = start * (1 * i)
            print ("Current win, win %0.2f, Current money is %0.2f" % (1 + i, start))
            plus += 1

        i = 0

    print("Strataged Money")
    print("%0.2f" % (start))
    var2 = ((start - 100000) / 100000) * 100
    print("The benifit rate %0.2f%% " % (var2))

    print("The total win %d  lose %d" % (plus, minus))


def do_kdj():
    #get_data()
    #draw_data()
    calc_rsv()
    # calc rsv
    # calc K
    # calc D
    # plot cross

do_kdj()

