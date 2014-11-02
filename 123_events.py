import copy
import datetime as dt
import numpy as np
import pandas as pd

import sys

# QSTK Imports
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du

def get_symbols(s_list_index):
    dataobj = da.DataAccess("Yahoo")
    
    return dataobj.get_symbols_from_list(s_list_index)

def get_data(dt_start, dt_end, ls_symbols):
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    ls_keys = ["open", "high", "low", "close", "volume", "actual_close"]
    dataobj = da.DataAccess('Yahoo')
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method="ffill")
        d_data[s_key] = d_data[s_key].fillna(method="bfill")
        d_data[s_key] = d_data[s_key].fillna(1.0)
    return d_data

def get_bollingers(df_prices, i_lookback):
    df_bollingers = np.NAN * copy.deepcopy(df_prices)
    for s_symbol in df_prices.columns:
        ts_price = df_prices[s_symbol]
        ts_mid = pd.rolling_mean(ts_price, i_lookback)
        ts_std = pd.rolling_std(ts_price, i_lookback)
        df_bollingers[s_symbol] = (ts_price - ts_mid) / (ts_std) 
    return df_bollingers

def save_bollingers(df_bollingers, s_out_file_path):
    df_bollingers.to_csv(s_out_file_path, sep=",", header=True, index=True)

def find_bollinger_events(df_bollingers):
    df_events = np.NAN * copy.deepcopy(df_bollingers)
    ldt_timestamps = df_bollingers.index
    for s_symbol in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            f_bollinger_today = df_bollingers[s_symbol].ix[ldt_timestamps[i]]
            f_bollinger_yest = df_bollingers[s_symbol].ix[ldt_timestamps[i - 1]]
            f_bollinger_index = df_bollingers[ls_symbols[-1]].ix[ldt_timestamps[i]]
            if f_bollinger_today < -2.0 and f_bollinger_yest >= -2.0 and f_bollinger_index >= 1.3:
                df_events[s_symbol].ix[ldt_timestamps[i]] = 1
    return df_events

def 123_events(df_prices):
    df_events = np.NAN * copy.deepcopy(df_bollingers)
    ldt_timestamps = df_bollingers.index
    for s_symbol in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            for h in range(1, len(ldt_timestamps)):
                if (df_prices[s_symbol].ix[ldt_timestamps[i+h+1]]-df_prices[s_symbol].ix[ldt_timestamps[i]]
                continue
                else
                    step = 1
                    if (df_prices[s_symbol].ix[ldt_timestamps[i+h+1]]-df_prices[s_symbol].ix[ldt_timestamps[i]] 
            f_bollinger_today = df_bollingers[s_symbol].ix[ldt_timestamps[i]]
            f_bollinger_yest = df_bollingers[s_symbol].ix[ldt_timestamps[i - 1]]
            f_bollinger_index = df_bollingers[ls_symbols[-1]].ix[ldt_timestamps[i]]
            if f_bollinger_today < -2.0 and f_bollinger_yest >= -2.0 and f_bollinger_index >= 1.3:
                df_events[s_symbol].ix[ldt_timestamps[i]] = 1
    return df_events

def generate_order(ldt_dates, t, delta_t, s_symbol, i_num):
    l_buy_order = [ldt_dates[t], s_symbol, "Buy", i_num]  
    i = t + delta_t
    if t + delta_t >= len(ldt_dates):
        i = len(ldt_dates) - 1
    l_sell_order = [ldt_dates[i], s_symbol, "Sell", i_num]
    return l_buy_order, l_sell_order

def generate_orders(df_events, i_num, delta_t):
    t = 0
    ldt_dates = list(df_events.index)
    ls_symbols = list(df_events.columns)
    ls_orders = []
    for t in range(len(ldt_dates)):
        for s_symbol in ls_symbols:
            if df_events.ix[ldt_dates[t], s_symbol] == 1:
                l_buy_order, l_sell_order = generate_order(ldt_dates, t, delta_t, s_symbol, i_num)
                ls_orders.append(l_buy_order)
                ls_orders.append(l_sell_order)
    df_orders = pd.DataFrame(data=ls_orders, columns=["date", "sym", "type", "num"])
    # It is not possible to set "date" as index due duplicate keys
    df_orders = df_orders.sort(["date", "sym", "type"], ascending=[1, 1, 1])
    df_orders = df_orders.reset_index(drop=True)
    return df_orders

def save_orders(df_orders, s_out_file_path):
    na_dates = np.array([[dt_date.year, dt_date.month, dt_date.day] for dt_date in df_orders["date"]])
    df_dates = pd.DataFrame(data=na_dates, columns=["year", "month", "day"])
    del df_orders["date"]
    df_orders = df_dates.join(df_orders)
    df_orders.to_csv(s_out_file_path, sep=",", header=False, index=False)
    
if __name__ == '__main__':
    print "start bollinger_events.py"

    s_list_index = "sp5002012"
    s_index = "SPY"
    s_lookback = sys.argv[1]
    s_delta_t = sys.argv[2]
    s_num = "100"
    s_start = "2008-01-01"
    s_end = "2009-12-31"
    
    s_bollingers_file_path = "data\\q1_bollinger" + ".csv"
    s_events_file_path = "data\\q1_bollinger_events" + ".csv"
    s_events_img_path = "data\\q1_bollinger_events" + ".pdf"
    s_orders_file_path = "data\\q1_orders" + ".csv"
    
    i_lookback = int(s_lookback)
    delta_t = int(s_delta_t)
    i_num = int(s_num)

    dt_start = dt.datetime.strptime(s_start, "%Y-%m-%d")
    dt_end = dt.datetime.strptime(s_end, "%Y-%m-%d")
    
    ls_symbols = get_symbols(s_list_index)
    ls_symbols.append(s_index)
    d_data = get_data(dt_start, dt_end, ls_symbols)
    
    df_bollingers = get_bollingers(d_data["close"], i_lookback)
    save_bollingers(df_bollingers, s_bollingers_file_path)
    
    df_bollinger_events = find_bollinger_events(df_bollingers)
    
    df_orders = generate_orders(df_bollinger_events, i_num, delta_t)
    save_orders(df_orders, s_orders_file_path)
    
    print "end bollinger_events.py"
