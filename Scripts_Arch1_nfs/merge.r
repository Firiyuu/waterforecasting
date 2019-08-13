library(NTS)


# Set current working directory.
setwd("D:/Thesis/Roque/Unlearn/New")
print(getwd())

waterleveldata <- read.csv("Mandulog_interpol.csv")
print(waterleveldata)

rainfalldata <- read.csv("Digkilaan_interpol.csv")
print(rainfalldata)

rainfalldata1 <- read.csv("Rogongon_interpol.csv")
print(rainfalldata1)

merged = merge(waterleveldata, rainfalldata,  by.x = "DATETTIME", by.y = "DATETTIME", by.z = "DATETTIME")
write.csv(merged, "merged_f1.csv")


merged = merge(waterleveldata, rainfalldata1,  by.x = "DATETTIME", by.y = "DATETTIME", by.z = "DATETTIME")
write.csv(merged, "merged_f2.csv")
