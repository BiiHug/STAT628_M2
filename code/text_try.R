library(tidyverse)
library(tidytext)

qq = read.csv('/Applications/Study/UWM/628/module2/textUsing/transqq.csv', stringsAsFactors = F)
test = data.frame(id = 1:nrow(qq), text=qq$text, stringsAsFactors = F)
qq_tt  = test %>% unnest_tokens(word, text)
str(qq_tt)
qq_dt = cast_sparse(qq_tt, id, word)
qq_dt[,'tofu']

qq_dt[,'don\'t']
qq$text[15]
qq_dt[,'mapo']

qq_dt[,'n\'t']

qq$text[7]
qq$text[55]

qq_cs = Matrix::colSums(qq_dt)


a = qq_dt[,'good']
b = qq_dt[,'chicken']
z = !(a==0 | b==0) 
cor(a[z],b[z])

sum(qq_cs>20)
qq_cs[qq_cs>5]
qq_x = qq_dt[,qq_cs>5]
qq_y = qq$stars>=3

qq_leaveout = sample(1:nrow(qq_dt), 2)
qq_fit = glmnet(qq_x[-qq_leaveout,], qq_y[-qq_leaveout] , family = "binomial", alpha  = 0.9)
qq_Yhat = predict.glmnet(qq_fit, qq_x[qq_leaveout,],s = qq_fit$lambda)
(qq_y[qq_leaveout] != (qq_Yhat>0)) %>%  colMeans  %>%plot

qq_Yhat[,46]
qq_y[qq_leaveout]

qq_modelSeq = 10
qq_fit$beta[,100] %>% sort(decreasing = TRUE) %>% head(30)
