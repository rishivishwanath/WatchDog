from fetch_data.fetch_data_cctx import fetch_l1_bbo
import time
ma={'binance':{'BTC/USDT'},'bybit':{'BTC/USDT'}}

def get_and_push():
    for i in ma:
        for j in ma[i]:
            print(i+" "+j)
            data=fetch_l1_bbo(i,j)
            print(data)

if __name__=="__main__":
    while True:
        get_and_push()
        time.sleep(5)
            