import pandas as pd





def get_rainy(series):
     datetime_ = series['DATETIME']

     rainy = ['12', '1/', '2','3','4','5']
     years_ = ['/2013', '/2014', '/2015', '/2016','/2017','/2018']



     list_ = []
     for year in years_:
        #2013 2018
     	
     	for rain in rainy: 
            dates_ = datetime_.loc[datetime_.str.startswith(rain, na=False)  & datetime_.str.contains(year)]
            search_  = dates_.tolist()
            frames = series[series['DATETIME'].isin(search_)]
            list_.append(frames)


  

     dataframe_12_5 = pd.concat(list_).reset_index(drop=True)
     dataframe_12_5.to_csv('sample_rain_1.csv')
    
     return dataframe_12_5


def get_dry(series):

     datetime_ = series['DATETIME']

     dry_ = ['6', '7', '8','9','10/','11']
     years_ = ['/2013', '/2014', '/2015', '/2016','/2017','/2018']



     list_ = []
     for year in years_:
        #2013 2018
     	
     	for dry in dry_: 
            dates_ = datetime_.loc[datetime_.str.startswith(dry, na=False)  & datetime_.str.contains(year)]
            search_  = dates_.tolist()
            frames = series[series['DATETIME'].isin(search_)]
            list_.append(frames)


  

     dataframe_6_11 = pd.concat(list_).reset_index(drop=True)
     dataframe_6_11.to_csv('sample_dry_1.csv')
    
     return dataframe_6_11
