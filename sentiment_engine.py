import pandas as pd
import yfinance as yf
import requests
from datetime import datetime

def fear_greed():

    url="https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

    r=requests.get(url).json()

    return r["fear_and_greed"]["score"]


def vix_sentiment():

    vix=yf.Ticker("^VIX").history(period="1d")["Close"].iloc[-1]

    score=max(0,min(100,100-vix*2))

    return score


def futures_sentiment():

    tickers=["ES=F","NQ=F","YM=F","RTY=F"]

    scores=[]

    for t in tickers:

        data=yf.Ticker(t).history(period="2d")

        change=(data["Close"][-1]-data["Close"][-2])/data["Close"][-2]

        scores.append(change)

    avg=sum(scores)/len(scores)

    sentiment=(avg+0.02)*2500

    sentiment=max(0,min(100,sentiment))

    return sentiment


def global_sentiment():

    fg=fear_greed()

    vix=vix_sentiment()

    fut=futures_sentiment()

    score=fg*0.4+vix*0.3+fut*0.3

    return round(score,2)


score=global_sentiment()

data={
"time":[datetime.utcnow()],
"sentiment":[score]
}

df=pd.DataFrame(data)

df.to_csv("sentiment.csv",mode="a",header=False,index=False)

print(score)
