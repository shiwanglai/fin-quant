"""
download the data
"""
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

def download_data(stock_name):
    #df = ts.get_hist_data('000858')
    df = ts.get_hist_data(stock_name)

    # save
    stock_path_name = '~/dev/data/' + stock_name + '.csv'
    #df.to_csv('000858.csv')
    df.to_csv(stock_path_name)

def read_data_from_file(stock_name, start='2019-06-01', end='2020-12-30'):
    stock_path_name = '~/dev/data/' + stock_name + '.csv'
    dfx = pd.read_csv(stock_path_name)

    # format index to Y-m-d
    dfx.index = dfx.iloc[:,0]
    dfx.index = pd.to_datetime(dfx.index, format='%Y-%m-%d')
    dfx = dfx.iloc[:,1:]

    # ascending
    dfx = dfx.sort_index(ascending=True)

    # get a peroid data
    dfx = dfx[start : end]

    return dfx

def draw_data(dfx):
    # plot it
    plt.figure(figsize=(12,6))
    plt.plot(dfx['close'], label = 'WLY')
    plt.title('Price')
    plt.xlabel('2020-01-01 - 2020-12-31')
    plt.ylabel('Close Price')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    # fxyy, 600196
    # wly,  000858
    # btjc, 603068
    # xagf, 600596
    stks = [ '600196', '000858', '603068', '600596' ]
    for stk in stks:
        download_data(stk)

