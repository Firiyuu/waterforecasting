import pandas as pd
import datetime as dt

df_a = pd.read_csv("imputed.csv")
df_b = pd.read_csv("imputed_mean_1.csv")

reference_date = dt.datetime(2019,1,1) # Arbitrary date used for reference
df_a.index = df_a['TIME'].apply(lambda x: reference_date + pd.DateOffset(seconds=x))
df_b.index = df_b['TIME'].apply(lambda x: reference_date + pd.DateOffset(seconds=x))

new_a = df_a['RAINFALL'].groupby(pd.TimeGrouper(freq='30T')).apply(lambda x: x.tolist())
new_b = df_b['WATERLEVEL'].groupby(pd.TimeGrouper(freq='30T')).apply(lambda x: x.tolist())

merged_df = pd.concat({'RAINFALL': new_a, 'WATERLEVEL': new_b}, axis = 1, sort=True)

merged = merged_df.index = (merged_df.index - reference_date).seconds # Return to original Time format

merged_df.to_csv(r'merged.csv')
