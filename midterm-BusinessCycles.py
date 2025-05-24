import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas_datareader as pdr
import numpy as np

# set the start and end dates for the data
start_date = '1994-01-01'
end_date = '2022-01-01'

# download the data of Germany from FRED using pandas_datareader
germany_gdp = web.DataReader('CLVMNACSCAB1GQDE', 'fred', start_date, end_date)
germany_log_gdp = np.log(germany_gdp)

lambdas = [10,100,1600]
germany_cycles = {}
germany_trends = {}

for lam in lambdas:
    cycle, trend = sm.tsa.filters.hpfilter(germany_log_gdp, lamb=lam)
    germany_cycles[lam] = cycle
    germany_trends[lam] = trend

#元データとトレンド成分の比較
plt.figure(figsize=(12,6))
plt.plot(germany_log_gdp, label="Log Real GDP of Germany",color = "black")
for lam in lambdas:
    plt.plot(germany_trends[lam],label=f"Trend(lambda={lam})")
plt.title("Log Real GDP and HP Filtered Trends (Germany)")
plt.xlabel("Date")
plt.ylabel("Log Real GDP")
plt.legend()
plt.grid(True)
plt.show(block=False)

#循環成分の比較
plt.figure(figsize=(12,6))
for lam in lambdas:
    plt.plot(germany_cycles[lam],label=f"Cycle(lambda={lam})")
plt.title("HP Filtered Cicles (Germany)")
plt.xlabel("Date")
plt.ylabel("Log Real GDP")
plt.legend()
plt.grid(True)
plt.show(block = False)


# download the data of Japan from FRED using pandas_datareader
japan_gdp = web.DataReader('JPNRGDPEXP', 'fred', start_date, end_date)
japan_log_gdp = np.log(japan_gdp)

lambdas = [10,100,1600]
japan_cycles = {}
japan_trends = {}

for lam in lambdas:
    cycle, trend = sm.tsa.filters.hpfilter(japan_log_gdp, lamb=lam)
    japan_cycles[lam] = cycle
    japan_trends[lam] = trend

#元データとトレンド成分の比較
plt.figure(figsize=(12,6))
plt.plot(japan_log_gdp, label="Log Real GDP of Japan",color = "black")
for lam in lambdas:
    plt.plot(japan_trends[lam],label=f"Trend(lambda={lam})")
plt.title("Log Real GDP and HP Filtered Trends (Japan)")
plt.xlabel("Date")
plt.ylabel("Log Real GDP")
plt.legend()
plt.grid(True)
plt.show(block=False)

#循環成分の比較
plt.figure(figsize=(12,6))
for lam in lambdas:
    plt.plot(japan_cycles[lam],label=f"Cycle(lambda={lam})")
plt.title("HP Filtered Cicles (Japan)")
plt.xlabel("Date")
plt.ylabel("Log Real GDP")
plt.legend()
plt.grid(True)
plt.show(block = False)

#標準偏差の計算
germany_std_devs = {lam: np.std(cycle, ddof=1) for lam, cycle in germany_cycles.items()}
print(germany_std_devs)
for lam in lambdas:
    std_dev = germany_std_devs[lam]
    print(f"λ={lam}のとき、標準偏差は{std_dev}")

japan_std_devs = {lam: np.std(cycle, ddof=1) for lam, cycle in japan_cycles.items()}
print(japan_std_devs)
for lam in lambdas:
    std_dev = japan_std_devs[lam]
    print(f"λ={lam}のとき、標準偏差は{std_dev}")

#相関係数の計算
for lam in lambdas:
    japan_cycle = japan_cycles[lam]
    germany_cycle = germany_cycles[lam]
    correlation = japan_cycle.corr(germany_cycle)
    print(f"λ={lam}のとき、相関係数は{correlation}")

#循環成分の描画
for lam in lambdas:
    japan_cycle = japan_cycles[lam]
    germany_cycle = germany_cycles[lam]
    plt.figure(figsize=(12,6))
    plt.plot(japan_cycle, label = "Japan")
    plt.plot(germany_cycle,label = "Germany")
    plt.title(f"HP Filtered Cyclical Component Comparison (λ={lam})")
    plt.xlabel("Date")
    plt.ylabel("Cyclical Component (log GDP)")
    plt.legend()
    plt.grid(True)
    plt.show(block=False)