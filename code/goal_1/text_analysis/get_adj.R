rm(list = ls())
library(data.table)
library(glmnet)
library(tidyverse)
library(tidytext)

###读取由extract_adj.py得到的adj列表
adj = fread('/Applications/Study/UWM/628/module2/textUsing/chineseadjs.csv')
adjWords = adj$words
##只保留字母
rvPunc = function(x) gsub('[^a-z]', '', x)
adjWords = apply(data.frame(words = adjWords), 2, rvPunc)[,1]
##去掉stopwords
adjWords = adjWords[!(adjWords %in% stopwords::stopwords())]
##只保留频率大于100的adj
adjWords = names(table(adjWords)[table(adjWords)>=100])

###读取由text_adj.py得到的为adj打分作准备的text数据
chinese = fread('/Applications/Study/UWM/628/module2/textUsing/transchinese2.csv', stringsAsFactors = FALSE)
chinese = chinese[,-1]

chineseStars = readRDS('/Applications/Study/UWM/628/module2/textUsing/chineseStars.rdata')
test = data.frame(id = 1:nrow(chinese), text = chinese$text, stringsAsFactors = FALSE)
rm(chinese)

chineseStars = chineseStars[-c(26572,71141)]

###构建review稀疏矩阵
chinese_tt  = test %>% unnest_tokens(word, text)
str(chinese_tt)
chinese_dt = cast_sparse(chinese_tt, id, word)
#saveRDS(chinese_dt, '/Applications/Study/UWM/628/module2/textUsing/chinese_dt.rdata')


###每条评论只保留adj
chinese_dt = chinese_dt[,colnames(chinese_dt) %in% names(table(adjWords))]
chinese_cs = colSums(chinese_dt)
chinese_cs['enthusiastic']

sum(chinese_cs>100)
chinese_cs[chinese_cs>100]
chinese_x = chinese_dt[,chinese_cs>100]
chinese_y = chineseStars>=3

chinese_leaveout = sample(1:nrow(chinese_dt), 20000)
chinese_fit = glmnet(chinese_x[-chinese_leaveout,], chinese_y[-chinese_leaveout] , family = "binomial", alpha  = 0.9)
#saveRDS(chinese_fit, '/Applications/Study/UWM/628/module2/textUsing/chinese_fit.rdata')
#chinese_fit = readRDS('/Applications/Study/UWM/628/module2/textUsing/chinese_fit.rdata')
chinese_Yhat = predict.glmnet(chinese_fit, chinese_x[chinese_leaveout,],s = chinese_fit$lambda)
(chinese_y[chinese_leaveout] != (chinese_Yhat>0)) %>%  colMeans  %>%plot

i=88
chinese_fit$beta[,i]['slimy']
chinese_fit$beta[,i]['enthusiastic']
chinese_fit$beta[,i]['express']
chinese_fit$beta[,i]['dry']
chinese_fit$beta[,i]['speedy']
chinese_fit$beta[,i]['friendly']
chinese_fit$beta[,i]['bit']
chinese_fit$beta[,i]['comparable']
chinese_fit$beta[,i]['oily']
chinese_fit$beta[,i]['often']
chinese_fit$beta[,i]['solid']
chinese_fit$beta[,i]['reasonable']
chinese_fit$beta[,i]['quality']

#根据回归得到最后的adj得分
chineseBeta1 = chinese_fit$beta[,88][abs(chinese_fit$beta[,88])>0.2]

chineseBeta1 = chineseBeta1[-which(names(chineseBeta1) == 'quality')]
chineseBeta1 = chineseBeta1[-which(names(chineseBeta1) == 'bit')]
chineseBeta1 = chineseBeta1[-which(names(chineseBeta1) == 'often')]


#saveRDS(chineseBeta1, '/Applications/Study/UWM/628/module2/textUsing/chineseBeta1.rdata')

