library(tidyverse)
library(tidytext)
library(glmnet)
chinese = read.csv('/Applications/Study/UWM/628/module2/chinesereview.csv', stringsAsFactors = FALSE)[,-1]
chineseBus = read.csv('/Applications/Study/UWM/628/module2/chinesebusiness.csv', stringsAsFactors = FALSE)[,-1]

city_count = function(x) {
  return(length(table(x)))
}

chineseCount = tapply(chinese$business_id,chinese$city,city_count)
chineseFew = which(chineseCount <= 3)
chineseSmall = which((chineseCount > 3) & (chineseCount <= 50) )
chineseCluster = which(chineseCount > 50)

city_define = function(x) {
  if (x %in% names(chineseFew)) return(1)
  else if (x %in% names(chineseSmall)) return(2)
  else return(3)
}
###中餐厅的多少似乎还是有点联系？
chinese$amount = sapply(chinese$city, city_define)
tapply(chinese$stars, chinese$amount, mean)

for(i in colnames(chinese)[-c(1,2,4,22,23)]){
  print(table(chinese[i])>10000)
  print(tapply(chinese$stars,chinese[i],mean))
}
###Brunch很高是因为有很多4星餐厅！
chineseBrunch = chinese[chinese$hours == 'brunch',]

###发现这个数据集其实很不均衡，有很多数据很可能是被一两家餐厅主导
###筛出评价较多的餐厅，以及其中的好餐厅/坏餐厅(有用吗？)
validRes = names(table(chinese$business_id))[table(chinese$business_id)>100]
chineseValid = chinese[chinese$business_id %in% validRes,]

avgStarsList = tapply(chineseValid$stars,chineseValid$business_id,mean)
hist(avgStarsList)
goodChineseList = names(which(avgStarsList >= 4))
badChineseList = names(which(avgStarsList <= 3))
goodChineseDf = chineseValid[chineseValid$business_id %in% goodChineseList,]

###伊利诺伊州似乎只有好餐厅没有坏餐厅？
table(goodChineseDf$state)
table(badChineseDf$state)

###business的数据似乎并不能给我们提供太多的有效信息，但他给我们的提示是不同的环境(州、城市)
###可能会对中餐厅的评价造成影响; 并且中餐厅存在一些刻板印象(just eat!, no party!)
table(chineseBus$RestaurantsPriceRange2)
table(chineseBus$OutdoorSeating)
table(chineseBus$HasTV)
table(chineseBus$WiFi)

###try
qq = chinese[chinese$name == 'QQ Express',]
test = data.frame(text = qq$text, index = 1:nrow(qq), stringsAsFactors = FALSE)
qq_tt  = test %>% unnest_tokens(word, text)
str(qq_tt)
qq_dt = cast_sparse(qq_tt, index, word)
qq_cs = colSums(qq_dt)
sum(qq_cs>5)
qq_cs[qq_cs>5]
qq_x = qq_dt[,qq_cs>5]
qq_y = qq$stars>=3

qq_leaveout = sample(1:nrow(qq_dt), 2)
qq_fit = glmnet(qq_x[-qq_leaveout,], qq_y[-qq_leaveout] , family = "binomial", alpha  = 0.9)
qq_Yhat = predict.glmnet(qq_fit, qq_x[qq_leaveout,],s = qq_fit$lambda)
(qq_y[qq_leaveout] != (qq_Yhat>0)) %>%  colMeans  %>%plot

qq_Yhat[,100]
qq_fit$beta[,100] %>% sort(decreasing = TRUE) %>% head(20)



qq = chinese[chinese$state == 'WI',]
test = data.frame(text = qq$text, index = 1:nrow(qq), stringsAsFactors = FALSE)
qq_tt  = test %>% unnest_tokens(word, text)
str(qq_tt)
qq_dt = cast_sparse(qq_tt, index, word)
qq_cs = colSums(qq_dt)
sum(qq_cs>30)
qq_cs[qq_cs>30]
qq_x = qq_dt[,qq_cs>30]
qq_y = qq$stars>=3

qq_leaveout = sample(1:nrow(qq_dt), 300)
qq_fit = glmnet(qq_x[-qq_leaveout,], qq_y[-qq_leaveout] , family = "binomial", alpha  = 0.9)
qq_Yhat = predict.glmnet(qq_fit, qq_x[qq_leaveout,],s = qq_fit$lambda)
(qq_y[qq_leaveout] != (qq_Yhat>0)) %>%  colMeans  %>%plot

qq_Yhat[,100]
qq_fit$beta[,100] %>% sort(decreasing = TRUE) %>% head(30)


qq = chinese[chinese$state == 'OH',]
test = data.frame(text = qq$text, index = 1:nrow(qq), stringsAsFactors = FALSE)
qq_tt  = test %>% unnest_tokens(word, text)
str(qq_tt)
qq_dt = cast_sparse(qq_tt, index, word)
qq_cs = colSums(qq_dt)
sum(qq_cs>30)
qq_cs[qq_cs>30]
qq_x = qq_dt[,qq_cs>30]
qq_y = qq$stars>=3

qq_leaveout = sample(1:nrow(qq_dt), 600)
qq_fit = glmnet(qq_x[-qq_leaveout,], qq_y[-qq_leaveout] , family = "binomial", alpha  = 0.9)
qq_Yhat = predict.glmnet(qq_fit, qq_x[qq_leaveout,],s = qq_fit$lambda)
(qq_y[qq_leaveout] != (qq_Yhat>0)) %>%  colMeans  %>%plot

qq_Yhat[,100]
qq_fit$beta[,100] %>% sort(decreasing = TRUE) %>% head(30)

