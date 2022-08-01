from stock_code import ts_codes
from get_data import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import mplfinance as mpf
from pandas.plotting import scatter_matrix
import numpy as np

class Stock:
    def __init__(self, stock_name, ts_code):
        self.stock_name = stock_name
        self.ts_code = ts_code
        self.data = get_data(self.ts_code)


def draw_vol(stocks):
    plt.figure(figsize=(20, 8), dpi=120)
    for stock in stocks:
        vol = stock.data['vol']
        trade_date = stock.data['trade_date']
        trade_date = pd.to_datetime(trade_date)
        plt.plot(trade_date, vol, label=stock.stock_name)

    plt.title('2012-2022 交易量', fontsize='12', fontproperties=font)
    plt.xlabel('日期', fontsize=10, fontproperties=font)
    plt.ylabel('交易量', fontsize=10, fontproperties=font)
    plt.legend(prop=font)

    if save_fig == True:
        plt.savefig('./imgs/2012-2022 交易量.png')

    plt.show()

def draw_close_vol(stocks, start_date):
    start_date = '2015-01-01'
    for stock in stocks:
        fig = plt.figure(figsize=(20, 10), dpi=120)
        vol = stock.data['vol'][stock.data['trade_date'] >= start_date]
        trade_date = pd.to_datetime(stock.data['trade_date'])[stock.data['trade_date'] >= start_date]
        close = stock.data['close'][stock.data['trade_date'] >= start_date]
        ax = fig.add_subplot(111)
        ax.plot(trade_date, vol, label="交易量")
        ax2 = ax.twinx()
        ax2.plot(trade_date, close, label="收盘价", c='r')
        plt.title('2022 {}收盘价与交易量'.format(stock.stock_name), fontsize='12', fontproperties=font)
        ax.legend(loc=2, borderaxespad=1., prop=font)
        ax2.legend(loc=1, borderaxespad=1., prop=font)

        if save_fig == True:
            plt.savefig('./imgs/{}收盘价与交易量.png'.format(stock.stock_name))

        plt.show()

def draw_matrix(stocks, start_date):
    # plt.figure(figsize=(10, 10), dpi=120)
    for stock in stocks:
        # fig = plt.figure(figsize=(10, 10), dpi=120)
        data = stock.data[stock.data['trade_date'] >= start_date]
        scatter_matrix(data[['open', 'high', 'low', 'close', 'pre_close', 'change', 'vol', 'amount']], )
        plt.suptitle(stock.ts_code)
        if save_fig == True:
            plt.savefig('./imgs/{}相关系数图.png'.format(stock.stock_name))

        plt.show()

def draw_correlation(stocks, start_date):
    start_date = '2022-01-01'
    for stock in stocks:
        data = stock.data[stock.data['trade_date'] >= start_date]
        cov = np.corrcoef(data[['open', 'high', 'low', 'close', 'pre_close', 'change', 'vol', 'amount']].T,)
        img = plt.matshow(cov)
        plt.colorbar(img, ticks=[-1, 0, 1])
        plt.title('{}相关系数图'.format(stock.stock_name), fontproperties=font)
        if save_fig == True:
            plt.savefig('./imgs/{}相关系数图.png'.format(stock.stock_name))

        plt.show()

def draw_candle(stocks, start_date, end_date):
    for stock in stocks:
        data = stock.data
        data['trade_date'] = pd.to_datetime(data['trade_date'])
        data = data[(stock.data['trade_date'] >= start_date) & (stock.data['trade_date'] <= end_date)]
        # print(data)
        data = data[['open', 'high', 'low', 'close', 'vol', 'trade_date']]
        data['trade_date'] = pd.to_datetime(data['trade_date'])
        data.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date']
        data = data.set_index('Date')
        mpf.plot(data, type='candle', title='{} 2022 candle graph'.format(stock.ts_code), style=my_style, volume=True, savefig='./imgs/{}{}蜡烛图'.format(stock.stock_name, end_date.split('-')[0]))

        plt.show()



def get_stocks():
    tsCodes = ts_codes()
    stocks = []
    for stock_name, ts_code in tsCodes.items():
        stock = Stock(stock_name, ts_code)
        stocks.append(stock)
    return stocks

if __name__=='__main__':
    font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
    my_style = mpf.make_mpf_style(base_mpf_style='binance',
                                  rc={'font.family': 'SimSun'})
    save_fig = True
    stocks = get_stocks()
    draw_vol(stocks=stocks)
    draw_close_vol(stocks=stocks, start_date='2015-01-01')
    draw_matrix(stocks=stocks, start_date='2022-01-01')
    draw_correlation(stocks=stocks, start_date='2022-01-01')
    draw_candle(stocks, '2021-01-01', '2021-10-01')
    draw_candle(stocks, '2021-10-02', '2022-07-01')