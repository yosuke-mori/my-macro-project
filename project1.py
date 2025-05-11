import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas_datareader as pdr
import numpy as np

# set the start and end dates for the data
start_date = '1955-01-01'
end_date = '2022-01-01'

# download the data from FRED using pandas_datareader
gdp = web.DataReader('JPNRGDPEXP', 'fred', start_date, end_date)
log_gdp = np.log(gdp)


lambdas = [10,100,1600]
cycles = {}
trends = {}

for lam in lambdas:
    cycle, trend = sm.tsa.filters.hpfilter(log_gdp, lamb=lam)
    cycles[lam] = cycle
    trends[lam] = trend

#元データとトレンド成分の比較
plt.figure(figsize=(12,6))
plt.plot(log_gdp, label="Log Real GDP",color = "black")
for lam in lambdas:
    plt.plot(trends[lam],label=f"Trend(lambda={lam})")
plt.title("Log Real GDP and HP Filtered Trends (Japan)")
plt.xlabel("Date")
plt.ylabel("Log GDP")
plt.legend()
plt.grid(True)
plt.show(block=False)

#循環成分の比較
plt.figure(figsize=(12,6))
for lam in lambdas:
    plt.plot(cycles[lam],label=f"Cycle(lambda={lam})")
plt.title("HP Filtered Cicles (Japan)")
plt.xlabel("Date")
plt.ylabel("Cycle")
plt.legend()
plt.grid(True)
plt.show()

