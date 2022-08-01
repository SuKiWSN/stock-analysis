import tushare as ts
import pandas as pd

def get_data(ts_code):
    pro = init()
    start_date = '20120101'
    end_date = '20220701'

    data = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    data.to_csv('./data/{}.csv'.format(ts_code), index=False)
    return data

def get_data_from_csv(ts_code):
    data = pd.read_csv('./data/{}.csv'.format(ts_code))
    # df = pd.DataFrame(data)
    # df['trade_date'] = pd.to_datetime(df['trade_date'])
    return data

def init():
    token = '206760a1bd32119e240149d18822d849034afe138dc8538a2609afa1'
    pro = ts.pro_api(token=token)
    return pro