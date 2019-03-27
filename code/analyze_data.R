library(tidyverse)
library(tidytext)

qq_tt  = test %>% unnest_tokens(word, text)
str(qq_tt)
qq_dt = cast_sparse(qq_tt, index, word)
#nrow(qq_dt)
#table(as.numeric(row.names(qq_dt)) == 1:60230)
#qq$text[21092]
qq_cs = colSums(qq_dt)

sum(qq_cs>20)
qq_cs[qq_cs>20]
qq_x = qq_dt[,qq_cs>20]
qq_y = qq$stars>=3

qq_leaveout = sample(1:nrow(qq_dt), 300)
qq_fit = glmnet(qq_x[-qq_leaveout,], qq_y[-qq_leaveout] , family = "binomial", alpha  = 0.9)
qq_Yhat = predict.glmnet(qq_fit, qq_x[qq_leaveout,],s = qq_fit$lambda)
(qq_y[qq_leaveout] != (qq_Yhat>0)) %>%  colMeans  %>%plot

qq_Yhat[,46]
qq_y[qq_leaveout]

qq_modelSeq = 10
qq_fit$beta[,46] %>% sort(decreasing = TRUE) %>% head(30)

