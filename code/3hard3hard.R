testBeta = qq_fit$beta[,80]
saveRDS(testBeta, '/Applications/Study/UWM/628/module2/usingData/testBeta.rdata')

logiBeta = readRDS('/Applications/Study/UWM/628/module2/usingData/logiBeta.rdata')
gauBeta = readRDS('/Applications/Study/UWM/628/module2/usingData/gauBeta.rdata')

cal_small_result = function(k) {
  smallReviewTest = readRDS(paste('/Applications/Study/UWM/628/module2/usingData/small',
                                  k,'.rdata', sep = ''))
  smallReviewTest$id = 1:nrow(smallReviewTest)
  small_tt = smallReviewTest %>% unnest_tokens(word, text)
  small_dt = cast_sparse(small_tt, id, word)
  
  small_tt_trans_logi = small_dt[,colnames(small_dt) %in% names(logiBeta)]
  smallBeta_logi = logiBeta[colnames(small_tt_trans_logi)]
  logi_result = small_tt_trans_logi %*% smallBeta_logi + 3.594748
  
  small_tt_trans_gau = small_dt[,colnames(small_dt) %in% names(gauBeta)]
  smallBeta_gau = gauBeta[colnames(small_tt_trans_gau)]
  gau_result = small_tt_trans_gau %*% smallBeta_gau + 3.594748
}

finalResult = rep(0, nTest)

for(k in 1:20){
  print(k)
  finalResult[groupList[[k]][[2]]] = cal_small_result(k)
}

length(finalResult)
plot(density(finalResult))

for(k in testEmpList) {
  finalResult = append(finalResult, 3, (k-1))
}

for(i in 1:length(finalResult)){
  if(finalResult[i]<1) finalResult[i] = 1
  if(finalResult[i]>5) finalResult[i] = 5
}
plot(density(finalResult))

realResult = data.frame(Id = 1:length(finalResult), Expected = finalResult)
write.csv(realResult, '/Applications/Study/UWM/628/module2/usingData/prediction.csv',
          row.names = FALSE)
