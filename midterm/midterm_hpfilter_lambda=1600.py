import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

# set the start and end dates for the data
start_date = '1994-01-01'
end_date = '2025-01-01'

# download the data of Germany from FRED using pandas_datareader
germany_gdp = web.DataReader('CLVMNACSCAB1GQDE', 'fred', start_date, end_date)
germany_log_gdp = np.log(germany_gdp)

g_cycle, g_trend = sm.tsa.filters.hpfilter(germany_log_gdp, lamb=1600)

# download the data of Japan from FRED using pandas_datareader
japan_gdp = web.DataReader('JPNRGDPEXP', 'fred', start_date, end_date)
japan_log_gdp = np.log(japan_gdp)

j_cycle, j_trend = sm.tsa.filters.hpfilter(japan_log_gdp, lamb=1600)

#calculate standard deviation 
germany_stdev = np.std(g_cycle)
print(f"ドイツ循環成分の標準偏差は{germany_stdev}")

japan_stdev = np.std(j_cycle)
print(f"日本循環成分の標準偏差は{japan_stdev}")

#calculate correlation 
correlation = j_cycle.corr(g_cycle)
print(f"相関係数は{correlation}")

#plot cyclical component of Germany and Japan
plt.figure(figsize = (12,6))
plt.plot(j_cycle, label = "Japan")
plt.plot(g_cycle,label = "Germany")
plt.title("HP Filtered Cyclical Component Comparison (λ=1600)")
plt.xlabel("Date")
plt.ylabel("Cyclical Component (log GDP)")
plt.legend()
plt.grid(True)
#plt.savefig('cyclical_component_comparison.png') 
plt.show()
