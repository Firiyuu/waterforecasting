import pandas as pd
import numpy as np

df1 = pd.read_csv("Mandulog.csv")
df2 = pd.read_csv("Rogongon.csv")
df3 = pd.read_csv("Digkilaan.csv")




# generating some test data



df = pd.DataFrame(np.random.random((200,3)))
df['date'] = pd.date_range('2000-1-1', periods=200, freq='D')
df = df.set_index(['date'])
print(df.loc['2000-6-1':'2000-6-10'])

# # building a different index
# timestamp = timestamp * np.random.randn(abs(1))
# df2 = pd.DataFrame({'timestamp': timestamp, 'd': ['val_d', 'val2_d'], 'e': ['val_e', 'val2_e'], 'f': ['val_f', 'val2_f'],'g': ['val_g', 'val2_g']}, index=index)


# # keeping a value in common with the first index
# timestamp = [1440540000, 1450560000]
# df3 = pd.DataFrame({'timestamp': timestamp, 'h': ['val_h', 'val2_h'], 'i': ['val_i', 'val2_i']}, index=index)



# # Setting the timestamp as the index
# df1.set_index('timestamp', inplace=True)
# df2.set_index('timestamp', inplace=True)
# df3.set_index('timestamp', inplace=True)


# # You can convert timestamps to dates but it's not mandatory I think
# df1.index = pd.to_datetime(df1.index, unit='s')
# df2.index = pd.to_datetime(df2.index, unit='s')
# df3.index = pd.to_datetime(df3.index, unit='s')



# Just perform a join and that's it
# result = df1.join(df2, how='outer').join(df3, how='outer')
# result