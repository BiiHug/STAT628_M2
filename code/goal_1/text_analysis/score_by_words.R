###这一部分我们进行评论的断句与单词附近形容词的提取

library(tidyverse)
library(tidytext)

transChinese3 = fread('/Applications/Study/UWM/628/module2/textUsing/transchinese3.csv', stringsAsFactors = FALSE)
transChinese3 = transChinese3[,-1]

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
    if(length(adj) == 0) adj = c('average'=0)
    score = mean(adj)
    if(length(adj) == 0) score = 0
    duanjuList[[i]][[1]] = juzi; duanjuList[[i]][[2]] = adj; duanjuList[[i]][[3]] = score
  }
  return(duanjuList)
}

get_score = function(word, name){
  returnList = list()
  location = which(transChinese3$name == name)
  real_test = data.frame(id = 1:length(location), text=transChinese3$text[location], stringsAsFactors = F)
  real_qq_tt  = real_test %>% unnest_tokens(word, text)
  real_qq_dt = cast_sparse(real_qq_tt, id, word)
  rowSums200 = which(rowSums(real_qq_dt[,-which(colnames(real_qq_dt) == 'duanju')])<=200)
  real_qq_dt = real_qq_dt[rowSums200,]
  real_test = real_test[rowSums200,]
  
  if(!(word %in% colnames(real_qq_dt))) return(NULL)
  appear = which(real_qq_dt[,word]>0)
  if(length(appear) == 0) return(NULL)
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

name = 'Nani Restaurant'
word = 'dim'
score_result = get_score(word, name)
score_result[[1]]
score_summary(score_result[[1]], score_result[[2]])[[3]]

get_scorelist_city = function(word, area){
  numList = table(transChinese3$name[which(transChinese3$city == area)])
  nameList = names(numList)
  nameList = nameList[which(numList > 20)]
  scoreList = c()
  for(name in nameList){
    score_result = get_score(word, name)
    score = score_summary(score_result[[1]], score_result[[2]])[[3]]
    if(length(score) == 0) score = 0
    scoreList[name] = score
  }
  return(sort(scoreList, decreasing = T))
}
get_scorelist_city('dim','Madison')

topPrice = head(get_scorelist_city('price', 'Madison'),5)
topService = head(get_scorelist_city('service', 'Madison'),5)
topFood = head(get_scorelist_city('food', 'Madison'),5)

get_city_rank = function(area){
  foodList = get_scorelist_city('food', area)
  serviceList = get_scorelist_city('service', area)[names(foodList)]
  priceList = get_scorelist_city('price', area)[names(foodList)]
  rankFrame = data.frame(food = foodList, service = serviceList, price = priceList)
  return(rankFrame)
}

Madison_rank = get_city_rank('Madison')


get_scorelist_state = function(word, area){
  numList = table(transChinese3$name[which(transChinese3$state == area)])
  nameList = names(numList)
  nameList = nameList[which(numList > 20)]
  scoreList = c()
  for(name in nameList){
    score_result = get_score(word, name)
    score = score_summary(score_result[[1]], score_result[[2]])[[3]]
    if(length(score) == 0) score = 0
    scoreList[name] = score
  }
  return(rank(-sort(scoreList, decreasing = T)))
}

get_state_rank = function(area){
  foodList = get_scorelist_state('food', area)
  serviceList = get_scorelist_state('service', area)[names(foodList)]
  priceList = get_scorelist_state('price', area)[names(foodList)]
  rankFrame = data.frame(food = foodList, service = serviceList, price = priceList)
  return(rankFrame)
}

WI_rank = get_state_rank('WI')


get_scorelist_all = function(word){
  numList = table(transChinese3$name)
  nameList = names(numList)
  nameList = nameList[which(numList > 20)]
  scoreList = c()
  for(name in nameList){
    score_result = get_score(word, name)
    score = score_summary(score_result[[1]], score_result[[2]])[[3]]
    if(length(score) == 0) score = 0
    scoreList[name] = score
  }
  return(rank(-sort(scoreList, decreasing = T)))
}

get_all_rank = function(){
  foodList = get_scorelist_all('food')
  serviceList = get_scorelist_all('service')[names(foodList)]
  priceList = get_scorelist_all('price')[names(foodList)]
  rankFrame = data.frame(food = foodList, service = serviceList, price = priceList)
  return(rankFrame)
}

all_rank = get_all_rank()
#saveRDS(all_rank, '/Applications/Study/UWM/628/module2/textUsing/all_rank.rdata')
all_rank['QQ Express',]

avg_star = tapply(transChinese3$stars, transChinese3$name, mean)
avg_star = avg_star[rownames(all_rank)]
all_rank = cbind(all_rank, avg_star)

food_cor = -cor(all_rank$food, all_rank$avg_star)
service_cor = -cor(all_rank$service, all_rank$avg_star)
price_cor = -cor(all_rank$price, all_rank$avg_star)

trans_Madison_rank = Madison_rank
trans_Madison_rank$food = Madison_rank$food*food_cor
trans_Madison_rank$service = Madison_rank$service*service_cor
trans_Madison_rank$price = Madison_rank$price*price_cor

trans_Madison_rank$sum = trans_Madison_rank$food+
                          trans_Madison_rank$service+
                          trans_Madison_rank$price
all_rank['QQ Express',]

final_Madison_rank = Madison_rank[order(trans_Madison_rank$sum),]
final_Madison_rank$final_rank = 1:nrow(final_Madison_rank)

final_Madison_rank['Nani Restaurant',]
