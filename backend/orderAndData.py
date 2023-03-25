import logging
import pickle
import os
# stocks not to watch for stategy one
stock_not_to_trade_sgty_one = ['lupin', 'cipla', 'ntpc',
                               'powergrid', 'gail', 'ongc', 'ioc', 'itc', 'coalindia', 'oil', 'pfc']

fnostock = open(os.path.dirname(os.path.abspath(__file__)) +
                "/../data/FNOstocks.csv")
fnostock = fnostock.readlines()

def get_hitorical_data(kite, instrument_token, from_date, to_date, interval):
    try:
        candles = kite.historical_data(
            instrument_token=instrument_token, from_date=from_date, to_date=to_date, interval=interval)
        return candles
    except Exception as e:
        logging.debug(f"Error in getting historical data {e}")


def get_stock_list_stgy_one(kite) -> list:
    try:
        path = os.getcwd()+'\data\stocket_stretegy_one' 
        if os.path.isfile(path):
            with open(path,'rb') as f:
                stocks_stgy_one = pickle.load(f)
            return stocks_stgy_one
        stocks_stgy_one = []
        instruments = kite.instruments()
        fno_symbols=[]
        for stock in fnostock:
            sym=stock.split(',')[1]
            fno_symbols.append(sym.split('\n')[0])
        for instrument in instruments:
            try:
                if instrument['exchange'] == 'NSE' and instrument['instrument_type'] == 'EQ' \
                    and instrument['tradingsymbol'] not in stock_not_to_trade_sgty_one and \
                    instrument['tradingsymbol'] in fno_symbols:
                    name = "NSE"+":"+instrument['tradingsymbol']
                    print(name)
                    stock_ltp = kite.ltp(name)[name]['last_price']
                    if stock_ltp > 100 and stock_ltp < 10000:
                        stocks_stgy_one.append(instrument)
            except Exception as e:
                logging.debug(f"Error getting stock+ {e}")
                continue
        with open(path,'wb') as f:
            pickle.dump(stocks_stgy_one,f)
        return stocks_stgy_one
    except Exception as e:
        logging.debug(f"Error getting stock list+ {e}")
