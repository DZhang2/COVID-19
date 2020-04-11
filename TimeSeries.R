setwd('/Users/davidzhang/Desktop/COVID-19/cleaned_data/daily/georgia')
files = list.files(path = '.')
#look closer at mortality rates
data = read.csv(files[1], header = FALSE)[1]
for(file in files) {
  values = read.csv(file, header = FALSE)
  temp = values[4]
  data = append(data, temp)
}
#data not organized properly so only look at top 10 
#counties in Georgia for Analysis; also more efficient

new_data = read.csv(files[19], header = FALSE)

