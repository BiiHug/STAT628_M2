rm(list = ls())
library(data.table)
library(glmnet)
library(tidyverse)
library(tidytext)

chinese = fread('/Applications/Study/UWM/628/module2/textUsing/transchinese.csv', stringsAsFactors = FALSE)
chinese = chinese[,-1]

chineseStars = readRDS('/Applications/Study/UWM/628/module2/textUsing/chineseStars.rdata')
test = data.frame(id = 1:nrow(chinese), text = chinese$text, stringsAsFactors = FALSE)
rm(chinese)

#write.csv(test, '/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv', row.names = F)

#saveRDS(chineseStars, '/Applications/Study/UWM/628/module2/textUsing/chineseStars.rdata')

#which(test$text == '.')
chineseStars = chineseStars[-c(26572,71141)]

qq_tt  = test %>% unnest_tokens(word, text)
str(qq_tt)
qq_dt = cast_sparse(qq_tt, id, word)
#saveRDS(qq_dt, '/Applications/Study/UWM/628/module2/textUsing/chinese_sparse.rdata')
#qq_dt = readRDS('/Applications/Study/UWM/628/module2/textUsing/chinese_sparse.rdata')
qq_cs = colSums(qq_dt)
qq_cs['quality']

sum(qq_cs>100)
qq_cs[qq_cs>100]
qq_x = qq_dt[,qq_cs>100]
qq_y = chineseStars>=3

qq_leaveout = sample(1:nrow(qq_dt), 20000)
qq_fit = glmnet(qq_x[-qq_leaveout,], qq_y[-qq_leaveout] , family = "binomial", alpha  = 0.9)
#saveRDS(qq_fit, '/Applications/Study/UWM/628/module2/textUsing/chinese_fit.rdata')
#qq_fit = readRDS('/Applications/Study/UWM/628/module2/textUsing/chinese_fit.rdata')
qq_Yhat = predict.glmnet(qq_fit, qq_x[qq_leaveout,],s = qq_fit$lambda)
(qq_y[qq_leaveout] != (qq_Yhat>0)) %>%  colMeans  %>%plot

qq_fit$beta[,40] %>% sort(decreasing = TRUE) %>% head(100)
i=50
qq_fit$beta[,i]['jason']
qq_fit$beta[,i]['great']

i=40
qq_fit$beta[,i]['someday']
qq_fit$beta[,i]['great']
qq_fit$beta[,i]['during']
qq_fit$beta[,i]['reasonably']

qq_fit$beta[,i]['a']



tryBeta = qq_fit$beta[,80]


qq_dis = qq_dt[qq_dt[,'food'] > 0,]
which(qq_dt[,'food'] > 0)
test$text[6]
index_dis = as.numeric(rownames(qq_dis))
View(cbind(test$text[index_dis], chineseStars[index_dis]))

qq_fit$beta[,80]['chinese']

j = 39
chineseStars[j]
try_tt = test[j,] %>% unnest_tokens(word, text)

try_result = qq_fit$beta[,i][try_tt$word]
plot(try_result)
text(1:length(try_result), try_result,try_tt$word)
test[j,]

qq_fit$beta[,40] > 0
bestBeta1 = qq_fit$beta[,40][which(qq_fit$beta[,40]!=0)]
#saveRDS(bestBeta1, '/Applications/Study/UWM/628/module2/textUsing/bestBeta1.rdata')
bestBeta1['greatest']
betaDict1 = data.frame(word = names(bestBeta1), score = bestBeta1, row.names = F)

