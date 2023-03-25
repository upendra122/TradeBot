import datetime
import orderAndData
import os
import json

def checkIFfollowingS1(data):
    # print(data)

    lenOfd = len(data)
    # print(lenOfd)
    if(lenOfd == 1):
        return True
    #lenOfd = min(lenOfd, 6)
    firstCandleLow = data[0]['low']
    firstCandleHigh = data[0]['high']
    for i in range(1, lenOfd):
        if(data[i]['low'] < firstCandleLow or data[i]['high'] > firstCandleHigh):
            return False
    return True


def backtest_stretegy_one(kite, stocks_stgy_one):
    #data = request.get_json(force=True)
    final_stats = {"win": 0, "lose": 0}
    all_stats_list = {}
    path=os.getcwd()
    for stock in stocks_stgy_one:
        if stock['segment']=='INDICES':
            continue
        stock_data_for_ml = open(path+"\data\stockdatafirst6candle.csv", "w+")
        print("Testing "+str(stock["tradingsymbol"]))
        file = open(path+"\data\Tempbacktest.txt", "a")
        print(stock)
        Token = stock['instrument_token']
        #Days = data['days']
        Days = 2000
        today_date = datetime.datetime.now()
        stats = {"win": 0, "lose": 0, "winrate": 0, "loserate": 0}

        for day in range(Days):

            start_time = today_date - datetime.timedelta(days=day)
            if start_time.weekday() == 5 or start_time.weekday() == 6:
                continue
            start_time = start_time.replace(hour=9, minute=15)
            end_time = today_date - datetime.timedelta(days=day)
            end_time = end_time.replace(hour=13, minute=30)
            try:
                candles=orderAndData.get_hitorical_data(kite,Token,start_time,end_time,"15minute")
            except Exception as e:
                print("Historic Api failed: {}"+str(e))
                pass
            if not candles or len(candles) < 6:
                continue
            if checkIFfollowingS1(candles[:6]):
                f_c_h = candles[0]['high']
                f_c_l = candles[0]['low']
                final_i = 0
                fail_flag = 0
                mldata_line = stock['tradingsymbol']+","
                for i in range(0, 6):
                    mldata_line += str(candles[i]['open'])+","+str(candles[i]['high']) + \
                        ","+str(candles[i]['low'])+","+str(candles[i]['close'])+","+str(candles[i]['volume'])+","
                for i in range(6, len(candles)):
                    if candles[i]['high'] > f_c_h:
                        target = f_c_h+(f_c_h*0.7)/100
                        stoploss = f_c_h - (f_c_h)/100
                        for j in range(i, len(candles)):
                            if candles[j]['high'] >= target:
                                stats["win"] = stats["win"]+1
#                                print('[+]win on ' +
  #                                    start_time.strftime("%Y-%m-%d %H:%M"))
                                fail_flag = 1
                                mldata_line += "1\n"
                                break
                            if candles[j]['low'] <= stoploss:
                                stats["lose"] = stats["lose"]+1
#                                print('[-]lose on ' +
 #                                     start_time.strftime("%Y-%m-%d %H:%M"))
                                fail_flag = 1
                                mldata_line += "0\n"
                                break
                        break
                    if candles[i]['low'] < f_c_l:
                        target = f_c_l-(f_c_l*0.7)/100
                        stoploss = f_c_l + (f_c_l)/100
                        for j in range(i, len(candles)):
                            if candles[j]['low'] <= target:
                                stats["win"] = stats["win"]+1
                                fail_flag = 1
                                mldata_line += "1\n"
 #                               print('[+]win on ' +
  #                                    start_time.strftime("%Y-%m-%d %H:%M"))
                                break
                            if candles[j]['high'] >= stoploss:
                                stats["lose"] = stats["lose"]+1
                                fail_flag = 1
                                mldata_line += "0\n"
#                                print('[-]lose on ' +
#                                     start_time.strftime("%Y-%m-%d %H:%M"))
                                break
                        break
                if fail_flag == 0:
                    mldata_line += "0\n"
                stock_data_for_ml.write(mldata_line)
        stock_data_for_ml.close()
        total_t = (stats["lose"]+stats["win"])
        if total_t:
            winrate = (stats["win"])/total_t
        else:
            winrate = 0
        if total_t:
            loserate = (stats["lose"])/total_t
        else:
            loserate = 0
        stats["winrate"] = winrate
        stats["loserate"] = loserate
        final_stats["win"] += stats["win"]
        final_stats["lose"] += stats["lose"]
        all_stats_list[stock['tradingsymbol']] = stats
        print(stock['tradingsymbol'])
        print('[!]winrate '+str(winrate))
        file.write(stock['tradingsymbol']+" : " +
                   str(winrate)+":"+str(loserate)+":"+str(stats["win"]+stats["lose"])+"\n")
        file.close()
        print('[!]loserate '+str(loserate))
        print('[!]Trade Taken ' +
              " "+str((stats["lose"]+stats["win"]))+" in " + str(Days) + "days")
    json_object = json.dumps(all_stats_list, indent=4)
    with open(path+"/data/statsnonfno.json", "w") as outfile:
        outfile.write(json_object)
    if (final_stats["lose"]+final_stats["win"]):
        winrate = (final_stats["win"])/(final_stats["lose"]+final_stats["win"])
        loserate = (final_stats["lose"]) / \
            (final_stats["lose"]+final_stats["win"])
    else:
        winrate = 0
        loserate = 0
    print('[!]winrate '+str(winrate))
    print('[!]loserate '+str(loserate))
    print('[!]Trade Taken ' +
          " "+str((final_stats["lose"]+final_stats["win"]))+" in " + str(Days) + "days")

    return final_stats
