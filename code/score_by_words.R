library(tidyverse)
library(tidytext)

transChinese2 = fread('/Applications/Study/UWM/628/module2/textUsing/transchinese2.csv', stringsAsFactors = FALSE)
transChinese2 = transChinese2[,-1]

get_duanju = function(theWord, wordsScore){
  wordLocation = which(theWord == names(wordsScore))
  puncLocation = which('duanju' == names(wordsScore))
  duanjuList = list()
  length(duanjuList) = length(wordLocation)
  for(i in (1:length(wordLocation))){
    start = tail(puncLocation[which(puncLocation < wordLocation[i])],1)
    if(length(start) == 0) start = 0
    end = head(puncLocation[which(puncLocation > wordLocation[i])],1)
    if(length(end) == 0) end = length(wordsScore) + 1
    juzi = wordsScore[(start+1):(end-1)]
    adj = juzi[which(abs(juzi)>0)]
    if(length(adj) == 0) adj = NA
    score = mean(adj)
    duanjuList[[i]][[1]] = juzi; duanjuList[[i]][[2]] = adj; duanjuList[[i]][[3]] = score
  }
  return(duanjuList)
}

get_score = function(word, name){
  returnList = list()
  location = which(transChinese2$name == name)
  real_test = data.frame(id = 1:length(location), text=transChinese2$text[location], stringsAsFactors = F)
  real_qq_tt  = real_test %>% unnest_tokens(word, text)
  real_qq_dt = cast_sparse(real_qq_tt, id, word)
  rowSums200 = which(rowSums(real_qq_dt[,-which(colnames(real_qq_dt) == 'duanju')])<=200)
  real_qq_dt = real_qq_dt[rowSums200,]
  real_test = real_test[rowSums200,]
  
  appear = which(real_qq_dt[,word]>0)
  appearRatio = length(appear)/nrow(real_qq_dt)
  appearList = list()
  length(appearList) = length(appear)
  for(i in (1:length(appear))){
    j = appear[i]
    try_qq_tt = real_test[j,] %>% unnest_tokens(word, text)
    wordsScore = rep(0, length(try_qq_tt$word))
    names(wordsScore) = try_qq_tt$word
    wordsScore[names(wordsScore) %in% names(chineseBeta1)] = chineseBeta1[names(wordsScore[names(wordsScore) %in% names(chineseBeta1)])]
    appearList[[i]] = get_duanju(word, wordsScore)
  }
  returnList[[1]] = appearList
  returnList[[2]] = appearRatio
  return(returnList)
}

score_summary = function(score_result, ratio){
  returnList = list()
  wordsList = c()
  for(i in (1:length(score_result))){
    for(j in (1:length(score_result[[i]]))){
      wordsList = append(wordsList,score_result[[i]][[j]][[2]])
    }
  }
  wordsList = wordsList[!is.na(wordsList)]
  returnList[[1]] = wordsList
  returnList[[2]] = mean(wordsList)
  returnList[[3]] = mean(wordsList) * ratio
  return(returnList)
}

table(transChinese2$name[which(transChinese2$city == 'Madison')])

name = 'QQ Express'
word = 'price'
score_result = get_score(word, name)
score_summary(score_result)

