import pandas as pd
import numpy as np

pwt90 = pd.read_stata('https://www.rug.nl/ggdc/docs/pwt90.dta')

oecd_countries = [
    'Australia', 'Austria', 'Belgium', 'Canada', 'Denmark', 'Finland', 'France',
    'Germany', 'Greece', 'Iceland', 'Ireland', 'Italy', 'Japan', 'Netherlands',
    'New Zealand', 'Norway', 'Portugal', 'Spain', 'Sweden', 'Switzerland',
    'United Kingdom', 'United States'
]

data = pwt90[
    pwt90['country'].isin(oecd_countries) &
    pwt90['year'].between(1990, 2019)
]

relevant_cols = ['countrycode', 'country', 'year', 'rgdpna', 'rkna', 'pop', 'emp', 'avh', 'labsh']
data = data[relevant_cols].dropna()

# Calculate additional variables
data['alpha'] = 1 - data['labsh']
#data["L_term"] = data["emp"]
data["L_term"] = data["emp"] * data["avh"]
data['y_n'] = data['rgdpna'] / (data['L_term']) 
data['k_n'] = data['rkna'] / (data['L_term'])  

def calculate_growth_rates(country_data):
    
    start_year_actual = country_data['year'].min()
    end_year_actual = country_data['year'].max()

    start_data = country_data[country_data['year'] == start_year_actual].iloc[0]
    end_data = country_data[country_data['year'] == end_year_actual].iloc[0]

    years = end_data['year'] - start_data['year']

    g_y = ((end_data['y_n'] / start_data['y_n']) ** (1/years) - 1) * 100

    g_k = ((end_data['k_n'] / start_data['k_n']) ** (1/years) - 1) * 100

    alpha_avg = (start_data['alpha'] + end_data['alpha']) / 2.0
    capital_deepening_contrib = alpha_avg * g_k
    tfp_growth_calculated = g_y - capital_deepening_contrib
    
    tfp_share = (tfp_growth_calculated / g_y)
    cap_share = (capital_deepening_contrib / g_y)

    return {
        'Country': start_data['country'],
        'Growth Rate': round(g_y, 2),
        'TFP Growth': round(tfp_growth_calculated, 2),
        'Capital Deepening': round(capital_deepening_contrib, 2),
        'TFP Share': round(tfp_share, 2),
        'Capital Share': round(cap_share, 2)
    }


results_list = data.groupby('country').apply(calculate_growth_rates).dropna().tolist()
results_df = pd.DataFrame(results_list)

avg_row_data = {
    'Country': 'Average',
    'Growth Rate': round(results_df['Growth Rate'].mean(), 2),
    'TFP Growth': round(results_df['TFP Growth'].mean(), 2),
    'Capital Deepening': round(results_df['Capital Deepening'].mean(), 2),
    'TFP Share': round(results_df['TFP Share'].mean(), 2),
    'Capital Share': round(results_df['Capital Share'].mean(), 2)
}
results_df = pd.concat([results_df, pd.DataFrame([avg_row_data])], ignore_index=True)

print("\nGrowth Accounting in OECD Countries: 1990-2019 period")
print("="*85)
print(results_df.to_string(index=False))

"""
(参考)L_termをdata["emp"]にした場合

Growth Accounting in OECD Countries: 1990-2019 period
=====================================================================================
       Country  Growth Rate  TFP Growth  Capital Deepening  TFP Share  Capital Share
     Australia         1.28        0.72               0.56       0.56           0.44
       Austria         0.97        0.39               0.58       0.40           0.60
       Belgium         0.72        0.16               0.56       0.22           0.78
        Canada         0.93        0.36               0.57       0.39           0.61
       Denmark         1.19        0.59               0.60       0.49           0.51
       Finland         1.44        0.82               0.62       0.57           0.43
        France         0.93        0.31               0.62       0.34           0.66
       Germany         1.13        0.56               0.57       0.50           0.50
        Greece         1.00        0.02               0.98       0.02           0.98
       Iceland         1.36        1.03               0.33       0.76           0.24
       Ireland         2.75        1.40               1.36       0.51           0.49
         Italy         0.48       -0.25               0.74      -0.52           1.52
         Japan         0.84       -0.53               1.37      -0.64           1.64
   Netherlands         0.89        0.51               0.39       0.57           0.43
   New Zealand         0.79        0.46               0.34       0.58           0.42
        Norway         1.24        0.63               0.61       0.51           0.49
      Portugal         1.36        0.21               1.15       0.15           0.85
         Spain         0.95       -0.07               1.01      -0.07           1.07
        Sweden         1.87        1.34               0.53       0.72           0.28
   Switzerland         0.50        0.11               0.40       0.21           0.79
United Kingdom         1.39        0.99               0.40       0.71           0.29
 United States         1.66        1.04               0.61       0.63           0.37
       Average         1.17        0.49               0.68       0.35           0.65
"""