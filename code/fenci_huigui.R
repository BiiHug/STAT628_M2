library(tidyverse)
library(glmnet)
library(tidytext)


###这里应该是你想要做回归的数据集
###最好把所有qq换为你想要最回归的数据集的名字
###基本的思路是先对所有中餐馆的评论数据做lasso回归，取第40个左右的惩罚项，从拟合的
##beta中提取普适性的修饰词(wonderful, fantasic等)
###这个过程需要对评论的text做哪些处理？我给的py里有一些我做过的处理，可以再考虑一下
##有没有其他需要的操作
###这样我们就可以得到一个普适性的修饰词list(表现为下文中的 names(bestBeta1))，这样
##再对每个餐馆做回归，从评论里面删去这些普适性的词，就可以得到更精确的结果
qq = read.csv('/Applications/Study/UWM/628/module2/textUsing/transqq.csv', stringsAsFactors = F)[,-1]
test = data.frame(id = 1:nrow(qq), text=qq$text, stringsAsFactors = F)
qq_tt  = test %>% unnest_tokens(word, text)
qq_dt = cast_sparse(qq_tt, id, word)
###这一步即为删去普适性的词
#qq_dt = qq_dt[,!(colnames(qq_dt) %in% names(bestBeta1))]
qq_cs = Matrix::colSums(qq_dt)

sum(qq_cs>10)
qq_cs[qq_cs>10]
qq_x = qq_dt[,qq_cs>10]
qq_y = qq$stars>=3

qq_leaveout = sample(1:nrow(qq_dt), 2)
qq_fit = glmnet(qq_x[-qq_leaveout,], qq_y[-qq_leaveout] , family = "binomial", alpha  = 0.9)
qq_Yhat = predict.glmnet(qq_fit, qq_x[qq_leaveout,],s = qq_fit$lambda)
(qq_y[qq_leaveout] != (qq_Yhat>0)) %>%  colMeans  %>%plot
qq_fit$beta[,40] %>% sort(decreasing = TRUE) %>% head(30)