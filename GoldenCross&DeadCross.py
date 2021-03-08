pip install backtesting
pip install matplotlib
pip install mpl_finance     #GoogleColabでmpl_financeが使用できなかったのでインストール

import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance
from mpl_finance import candlestick2_ohlc
import datetime
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting import Backtest
 
%matplotlib inline  #ノートブック上にグラフを描画する
 
usecols = ['time','close','open','high','low']
df = pd.read_csv("usd_10min_api.csv", usecols=usecols, index_col='time', parse_dates=True)
df.tail(2)　　　　#末尾の２行を確認

df.columns = ['Close','Open','High','Low']   #カラム名の頭文字は大文字
df.columns

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()
 
class SmaCross(Strategy):
    n1 = 3
    n2 = 6
 
    def init(self):
        self.sma1 = self.I(SMA, self.data['Close'], self.n1)
        self.sma2 = self.I(SMA, self.data['Close'], self.n2)
    
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

bt = Backtest(df[1500:2000], SmaCross, cash=500, commission=0)   #commisionは取引所の手数料

bt.run()  #テスト結果
bt.plot() #結果を可視化

