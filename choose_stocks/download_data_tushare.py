"""
download the data
"""

import tushare as ts

def download_data():
    df = ts.get_hist_data('000858')
    df.to_csv('000858.csv')

download_data()

