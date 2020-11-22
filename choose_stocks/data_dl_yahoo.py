"""
download the data
"""
from pandas_datareader import data as pdr
import datetime
#import pandas as pd

#import matplotlib.pyplot as plt

def download_data(stock_name):
    df = pdr.get_data_yahoo(stock_name, start=datetime.datetime(2019, 6, 1),
            end=datetime.datetime(2020,12,31))

    # sort from latest to former
    df = df.sort_index(ascending=False)

    # let label lower case
    df = df.rename(columns=str.lower)
    print(df.head())
    print(len(df))

    # check index duplicated
    df = df[~df.index.duplicated()]

    # save
    stock_path_name = '~/dev/data/' + stock_name + '.csv'
    #df.to_csv('000858.csv')
    df.to_csv(stock_path_name)

'''
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
'''

if __name__ == '__main__':
    '''
    # fxyy, 600196
    # wly,  000858
    # btjc, 603068
    # xagf, 600596
    stks = [ '600196', '000858', '603068', '600596' ]
    for stk in stks:
        download_data(stk)
    '''
    #stk = "APPL"
    stk = "USDT-BTC"
    download_data(stk);

