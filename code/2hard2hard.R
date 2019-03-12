rm(list = ls())
library(data.table)
library(glmnet)
library(tidyverse)
library(tidytext)

group_train_test = function(nTrain, nTest, k){
  groupList = list()
  indexTrainList = 1:nTrain ; indexTestList = 1:nTest
  kTrainRow = nTrain %/% k ; kTestRow = nTest %/% k
  
  for(i in 1:k){
    ithGroupList = list()
    ithGroupList[[1]] = sample(indexTrainList, kTrainRow)
    ithGroupList[[2]] = sample(indexTestList, kTestRow)
    indexTrainList = setdiff(indexTrainList, ithGroupList[[1]])
    indexTestList = setdiff(indexTestList, ithGroupList[[2]])
    groupList[[i]] = ithGroupList
  }
  
  groupList[[k]][[1]] = append(groupList[[k]][[1]], indexTrainList)
  groupList[[k]][[2]] = append(groupList[[k]][[2]], indexTestList)
  return(groupList)
}

save_group = function(k) {
  ithReviewMerge = rbind(reviewTrain2[groupList[[k]][[1]],],
                         reviewTest2[groupList[[k]][[2]],])
  saveRDS(ithReviewMerge, paste('/Applications/Study/UWM/628/module2/usingData/',
                     k,'.rdata', sep = ''))
}

k = 7

get_group_result = function(k) {
  ithReviewMerge = readRDS(paste('/Applications/Study/UWM/628/module2/usingData/',
                                                 k,'.rdata', sep = ''))
  ithReviewMerge$id = 1:nrow(ithReviewMerge)
  qq_tt  = ithReviewMerge %>% unnest_tokens(word, text)
  qq_dt = cast_sparse(qq_tt, id, word)
  qq_cs = Matrix::colSums(qq_dt)
  print(sum(qq_cs>1000))
  
  qq_x = qq_dt[1:length(groupList[[k]][[1]]),qq_cs>1000]
  qq_y1 = trainStars[groupList[[k]][[1]]] >=3
  qq_y2 = trainStars[groupList[[k]][[1]]]
  
  qq_leaveout = sample(1:length(groupList[[k]][[1]]), 20000)
  qq_fit1 = glmnet(qq_x[-qq_leaveout,], qq_y1[-qq_leaveout] , family = "binomial", alpha  = 0.9)
  qq_Yhat1 = predict.glmnet(qq_fit1, qq_x[qq_leaveout,],s = qq_fit1$lambda)
  (qq_y1[qq_leaveout] != (qq_Yhat1>0)) %>%  colMeans  %>%plot
  trans_stars = (1/(1+exp(-qq_Yhat1)))%/%0.2+1 
  hist(trans_stars[,1])
  qq_Yhat1 = qq_x[qq_leaveout,] %*% qq_fit1$beta[,90] + 0.852
  saveRDS(qq_fit1$beta[,90], '/Applications/Study/UWM/628/module2/usingData/logiBeta.rdata')
  sqrt(mean((qq_y2[qq_leaveout] - trans_stars[,1])^2))
  
  qq_fit2 = glmnet(qq_x[-qq_leaveout,], qq_y2[-qq_leaveout] , family = "gaussian", alpha  = 0.9)
  qq_Yhat2 = predict.glmnet(qq_fit2, qq_x[qq_leaveout,],s = qq_fit2$lambda)
  qq_Yhat2 = qq_x[qq_leaveout,] %*% qq_fit2$beta[,80] + 3.594748
  saveRDS(qq_fit2$beta[,80], '/Applications/Study/UWM/628/module2/usingData/gauBeta.rdata')
  lambdaLength = length(qq_Yhat2[1,])
  y = c()
  for(i in 1:lambdaLength){
    y[i] = sqrt(mean((qq_y2[qq_leaveout] - qq_Yhat2[,i])^2))
  }
  plot(y)
  
  result = c()
  noLogi = which(trans_stars == 5)
  result[noLogi] = qq_Yhat2[noLogi, 80]
  result[-noLogi] = trans_stars[-noLogi]
  for(i in 1:length(result)){
    if(result[i]>5) result[i] = 5
  }
  plot(density(result))
  
  sqrt(mean((qq_y2[qq_leaveout] - result)^2))
  
  lambdaLength = length(qq_Yhat[1,])
  y = c()
  for(i in 1:lambdaLength){
    y[i] = sqrt(mean((qq_y[qq_leaveout] - qq_Yhat[,i])^2))
  }
  plot(y)
  plot(density(qq_y))
  greatLambda = qq_fit$lambda[which(y == min(y))]
  qq_fit$beta[,43] %>% sort(decreasing = TRUE) %>% head(30)
  plot(density(qq_Yhat[,43]))
  
  qq_Yhat[,43] - qq_x[qq_leaveout,] %*% qq_fit$beta[,43]
  
  mean(qq_y)
  
  prediction = predict.glmnet(qq_fit, 
                              qq_x[-(1:length(groupList[[k]][[1]])),qq_cs>500],
                              s = greatLambda)
  for(i in 1:length(prediction)){
    if(prediction[i]<1) prediction[i] = 1
    if(prediction[i]>5) prediction[i] = 5
  }
  return(prediction)
}

reviewTrain = fread("/Applications/Study/UWM/628/module2/yelpDataframe2.csv")
colnames(reviewTrain)
reviewTest = fread("/Applications/Study/UWM/628/module2/reviewtest.csv")
colnames(reviewTest)

trainEmpList = which(reviewTrain$text == '.')
testEmpList = which(reviewTest$text == '.')
trainStars = reviewTrain$star
saveRDS(trainStars, '/Applications/Study/UWM/628/module2/usingData/trainStar.rdata')
trainStars = as.numeric(readRDS('/Applications/Study/UWM/628/module2/usingData/trainStar.rdata'))

reviewTrain2 = reviewTrain[,c(2,4)]
rm(reviewTrain)
reviewTest2 = reviewTest[-testEmpList,c(3,5)]
colnames(reviewTest2) [1] = 'id'
rm(reviewTest)

nTrain = nrow(reviewTrain2)
nTest = nrow(reviewTest2)

resultList = rep(0, nTest+5)
resultList[testEmpList] = 3

#groupList = group_train_test(5364611, 1321269, 20)
#saveRDS(groupList, '/Applications/Study/UWM/628/module2/usingData/groupList.rdata')
groupList = readRDS('/Applications/Study/UWM/628/module2/usingData/groupList.rdata')
#for(i in 3:20) save_group(i)
#rm(reviewTest2)
#rm(reviewTrain2)

preResultList = c()
append(preResultList,get_group_result(1))

sum(qq_fit$beta[,80] != 0)

smallReviewTest = ithReviewMerge[-(1:length(groupList[[k]][[1]])),]
smallReviewTest$id = 1:nrow(smallReviewTest)
small_tt = smallReviewTest %>% unnest_tokens(word, text)
small_dt = cast_sparse(small_tt, id, word)

sum(colnames(small_dt) %in% names(qq_fit$beta[,80]))

small_tt_trans = small_dt[,colnames(small_dt) %in% names(qq_fit$beta[,80])]

colnames(small_tt_trans) [1:10]
smallBeta = qq_fit$beta[,80][colnames(small_tt_trans)]

smallBeta[1:10]
result = small_tt_trans %*% smallBeta
plot(density(result[,1]+mean(qq_y)))
hist(result[,1]+mean(qq_y))
