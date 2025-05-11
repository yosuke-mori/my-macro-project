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

# apply a Hodrick-Prescott filter to the data to extract the cyclical component
cycle, trend = sm.tsa.filters.hpfilter(log_gdp, lamb=1600)

# Plot the original time series data
plt.plot(log_gdp, label="Original GDP (in log)")

# Plot the trend component
plt.plot(trend, label="Trend")

# Add a legend and show the plot
plt.legend()
plt.show()


lambdas = [10,100,1600]
cycles = {}
trends = {}

for lam in lambdas:
    cycle, trend = sm.tsa.filters.hpfilter(log_gdp, lamb=lam)
    cycles[lam] = cycle
    trends[lam] = trend

plt.figure(figsize=(12,6))
plt.plot(log_gdp, label="Log Real GDP",color = "black")
for lam in lambdas:
    plt.plot(trends[lam],label=f"Trend(lambda={lam})")
plt.title("Log Real GDP and HP Filtered Trends (Japan)")
plt.xlabel("Date")
plt.ylabel("Log GDP")
plt.legend()
plt.grid(True)
plt.show()


lambdas = [10, 100, 1600, 3000]
titles = [f"λ = {lam}" for lam in lambdas]

plt.figure(figsize=(14, 10))
for i, lam in enumerate(lambdas):
    cycle, trend = sm.tsa.filters.hpfilter(log_gdp, lamb=lam)
    plt.subplot(2, 2, i + 1)
    plt.plot(log_gdp, label="Original Log GDP", color='blue')
    plt.plot(trend, label=f"HP Trend (λ={lam})", color='red', linestyle='--')
    plt.title(titles[i])
    plt.xlabel("Year")
    plt.ylabel("Log GDP")
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.show()