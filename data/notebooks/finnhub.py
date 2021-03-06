import finnhub
import pandas as pd
import re
from datetime import datetime
import time

from deephaven.DateTimeUtils import currentTime, secondsToTime, convertDateTime, millis

from deephaven import DynamicTableWriter
import deephaven.Types as dht
import threading


def pull_coins():
    exchanges = finnhub_client.crypto_exchanges()
    temp_ids = []
    for exchange in exchanges:
        long_list = finnhub_client.crypto_symbols(exchange)
        symbols = pd.DataFrame(long_list).loc[:,'symbol']
        temp_ids.append(symbols.values.tolist())

    ids = [item for sublist in temp_ids for item in sublist]

    r=re.compile(".*({}).*".format(search_term))
    return list(filter(r.match, ids))[12:]

ids = pull_coins()

def thread_func():
        for i in range(50):
            for id in ids:
                data = finnhub_client.crypto_candles(id, 15, int(millis(minus(currentTime(),convertPeriod("T"+str(int((24*time_history)))+"H")))/1000), int(datetime.timestamp(datetime.now())))
                coin = id
                if data['s'] =='ok' and len(data['s'])>0:
                    c = (data['c'])
                    h = (data['h'])
                    l = (data['l'])
                    o = (data['o'])
                    t = (data['t'])
                    v = (data['v'])
                    if c != None:
                        for i in range(len(c)): 
                            tableWriter.logRow(coin, float(c[i]), float(h[i]), float(l[i]), float(o[i]), secondsToTime(t[i]), float(v[i]))
            time.sleep(1)



tableWriter = DynamicTableWriter(
    ["Coin", "Close", "High", "Low", "Open", "DateTime", "Volume"],
    #[dht.string, dht.string, dht.string, dht.string, dht.string, dht.string, dht.string, dht.string]

    [dht.string, dht.float64, dht.float64, dht.float64, dht.float64, dht.datetime, dht.float64]
)

coin_data = tableWriter.getTable().formatColumns("Close = Decimal(`#,###.##############`)").formatColumns("High = Decimal(`#,###.##############`)").formatColumns("Low = Decimal(`#,###.##############`)").formatColumns("Open = Decimal(`#,###.##############`)")

thread = threading.Thread(target = thread_func)
thread.start()
