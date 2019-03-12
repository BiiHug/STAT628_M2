testBeta = readRDS('/Applications/Study/UWM/628/module2/usingData/testBeta.rdata')

cal_small_result = function(k) {
  smallReviewTest = readRDS(paste('/Applications/Study/UWM/628/module2/usingData/small',
                                  k,'.rdata', sep = ''))
  smallReviewTest$id = 1:nrow(smallReviewTest)
  small_tt = smallReviewTest %>% unnest_tokens(word, text)
  small_dt = cast_sparse(small_tt, id, word)
  small_tt_trans = small_dt[,colnames(small_dt) %in% names(testBeta)]
  smallBeta = testBeta[colnames(small_tt_trans)]
  result = small_tt_trans %*% smallBeta
  return(result+3.617422)
}

finalResult = rep(0, nTest)

for(k in 1:19){
  print(k)
  finalResult[((k-1)*n_each_group+1):(k*n_each_group)] = cal_small_result(k)
}

finalResult[((20-1)*n_each_group+1):nTest] = cal_small_result(20)

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
