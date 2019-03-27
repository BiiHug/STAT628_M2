rm(list = ls())
library(data.table)
library(glmnet)
library(tidyverse)
library(tidytext)

chineseOld = fread('/Applications/Study/UWM/628/module2/chinesereview.csv', stringsAsFactors = FALSE)
chinese = chinese[,-1]

chineseStars = chinese$stars
test = data.frame(id = 1:nrow(chinese), text = chinese$text, stringsAsFactors = FALSE)
rm(chinese)

#write.csv(test, '/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv', row.names = F)
test = fread('/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv', stringsAsFactors = FALSE)
test = test[-c(26572,71141),]
#saveRDS(chineseStars, '/Applications/Study/UWM/628/module2/textUsing/chineseStars.rdata', )

#which(test$text == '.')
#chineseStars = chineseStars[-c(26572,71141)]

qq_tt  = test %>% unnest_tokens(word, text)
str(qq_tt)
qq_dt = cast_sparse(qq_tt, id, word)
#saveRDS(qq_dt, '/Applications/Study/UWM/628/module2/textUsing/chinese_sparse.rdata')
qq_cs = colSums(qq_dt)
qq_cs['slimy']

sum(qq_cs>500)
qq_cs[qq_cs>500]
qq_x = qq_dt[,qq_cs>500]
qq_y = chineseStars>=3

qq_leaveout = sample(1:nrow(qq_dt), 20000)
qq_fit = glmnet(qq_x[-qq_leaveout,], qq_y[-qq_leaveout] , family = "binomial", alpha  = 0.9)
#saveRDS(qq_fit, '/Applications/Study/UWM/628/module2/textUsing/chinese_fit.rdata')
qq_Yhat = predict.glmnet(qq_fit, qq_x[qq_leaveout,],s = qq_fit$lambda)
(qq_y[qq_leaveout] != (qq_Yhat>0)) %>%  colMeans  %>%plot

qq_fit$beta[,40] %>% sort(decreasing = TRUE) %>% head(30)

qq_dis = qq_dt[qq_dt[,'complaints'] > 0,]

index_dis = as.numeric(rownames(qq_dis))
View(cbind(test$text[index_dis], chineseStars[index_dis]))
