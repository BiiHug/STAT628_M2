reviewTest = fread("/Applications/Study/UWM/628/module2/reviewtest.csv")[,c(3,5)]
testOkList = as.numeric(readRDS('/Applications/Study/UWM/628/module2/usingData/bii.rdata'))
testEmpList = which(!(1:1321274) %in% testOkList)
reviewTest2 = reviewTest[testOkList,]
nTest = nrow(reviewTest2)

colnames(reviewTest2) [1] = 'id'
rm(reviewTest)


n_each_group = nTest %/% 20
save_small_group = function(k) {
  saveRDS(reviewTest2[((k-1)*n_each_group+1):(k*n_each_group),],
          paste('/Applications/Study/UWM/628/module2/usingData/small',
                                k,'.rdata', sep = ''))
}

for (k in 1:19) save_small_group(k)
saveRDS(reviewTest2[((20-1)*n_each_group+1):nTest,],
        paste('/Applications/Study/UWM/628/module2/usingData/small',
              20,'.rdata', sep = ''))
