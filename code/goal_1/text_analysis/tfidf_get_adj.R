###这里是对adj做tfidf的一个尝试

rm(list = ls())
library(data.table)
library(glmnet)
library(tidyverse)
library(tidytext)

tfidfchinese_dt = as.matrix(read.csv('/Applications/Study/UWM/628/module2/textUsing/tfidfchinese.csv')[,-1])

tfidfchinese_cs = colSums(tfidfchinese_dt)


sum(tfidfchinese_cs>100)
tfidfchinese_cs[tfidfchinese_cs>100]
tfidfchinese_x = tfidfchinese_dt[,tfidfchinese_cs>100]
chinese_y = chineseStars>=3

tfidfchinese_leaveout = sample(1:nrow(tfidfchinese_dt), 20000)
tfidfchinese_fit = glmnet(tfidfchinese_x[-tfidfchinese_leaveout,], chinese_y[-tfidfchinese_leaveout] , family = "binomial", alpha  = 0.9)
#saveRDS(tfidfchinese_fit, '/Applications/Study/UWM/628/module2/textUsing/tfidfchinese_fit.rdata')
#tfidfchinese_fit = readRDS('/Applications/Study/UWM/628/module2/textUsing/tfidfchinese_fit.rdata')
tfidfchinese_Yhat = predict.glmnet(tfidfchinese_fit, tfidfchinese_x[tfidfchinese_leaveout,],s = tfidfchinese_fit$lambda)
(chinese_y[tfidfchinese_leaveout] != (tfidfchinese_Yhat>0)) %>%  colMeans  %>%plot

i=88
tfidfchinese_fit$beta[,i]['slimy']
tfidfchinese_fit$beta[,i]['enthusiastic']
tfidfchinese_fit$beta[,i]['express']
tfidfchinese_fit$beta[,i]['dry']
tfidfchinese_fit$beta[,i]['speedy']
tfidfchinese_fit$beta[,i]['friendly']
tfidfchinese_fit$beta[,i]['bit']
tfidfchinese_fit$beta[,i]['comparable']
tfidfchinese_fit$beta[,i]['oily']
tfidfchinese_fit$beta[,i]['often']
tfidfchinese_fit$beta[,i]['solid']
tfidfchinese_fit$beta[,i]['reasonable']
tfidfchinese_fit$beta[,i]['quality']


tfidfchineseBeta1 = tfidfchinese_fit$beta[,88][abs(tfidfchinese_fit$beta[,88])>0.2]

tfidfchineseBeta1 = tfidfchineseBeta1[-which(names(tfidfchineseBeta1) == 'quality')]
