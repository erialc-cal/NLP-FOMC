
rm(list=ls())

setwd('/Users/etiennelenaour/Desktop/Stage/csv_files')

data <- read.csv('df_traitement_finale_posi.csv', header=T)



lm_model <- lm(Score ~ Chair + nasdaq_value  + Name, data = data)
summary(lm_model)
