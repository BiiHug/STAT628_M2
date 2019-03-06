library(tidyverse)
library(tidytext)
library(glmnet)
library(ggplot2)
library(ggthemes)
library (ggmap)

#chinese = read.csv('/Applications/Study/UWM/628/module2/chinesereview.csv', stringsAsFactors = FALSE)[,-1]
chineseBus = read.csv('/Users/zhangyilun/Desktop/Module2/STAT628_M2-master/data/chinesebusiness.csv', stringsAsFactors = FALSE)[,-1]
us <- c(left = -125, bottom = 25.75, right = -67, top = 60)
#提取数值和行名
ta = sort(table(chineseBus$state),decreasing = T)
ta_val = as.matrix(as.data.frame(ta)[,2])
ta_name = as.matrix(as.data.frame(ta)[,1])
#数据scale
ta_sum = sum(ta_val)
shap_test = ta_val/ta_sum
shap_test_fi = shap_test*80
#输入经纬
ma = matrix(c(44.56664532,-80.84998519,33.729759,-111.431221,38.313515,-117.055374,49.82257774,-64.34799504,40.388783,-82.764915,35.630066,-79.806419,40.590752,-77.209755,53.01669802,-112.8166386,44.268543,-89.616508,40.349457,-88.986137,33.856892,-80.945007,42.165726,-74.948051),ncol = 2,byrow = T)
colnames(ma) = c('lat','lon')
ma = ma[,c(2,1)]
rownames(ma) = c(ta_name[-13,])
sha = matrix(c(shap_test_fi))[-13,]
ma_fin = cbind(ma,sha)
ma_fin = as.data.frame(ma_fin)
rownames(ma_fin) = c(ta_name[-13,])
ma_fin
#移动红点位置
ma_fin$lon[c(1,4)] = c(-88,-72)
ma_fin$lat[c(1,4)] = c(52,50)
#ggmap
get_stamenmap(us, zoom = 4, maptype = "toner-lite") %>% ggmap() + 
  geom_point(aes(lon,lat), data=ma_fin, size = ma_fin[,3], col = 'red', alpha = 0.6) +
  xlab("Longitude") +
  ylab("Latitude") 



