chinese = read.csv('/Applications/Study/UWM/628/module2/chinesereview.csv', stringsAsFactors = FALSE)
chinese = chinese[,-1]

chinese_toronto = chinese[chinese$city == 'Toronto',]
length(table(chinese_toronto$business_id))

chinese_Calgary = chinese[chinese$city == 'Calgary',]
length(table(chinese_Henderson$business_id))

cityCount = function(x) {
  return(length(table(x)))
}

x = tapply(chinese$business_id,chinese$city,cityCount)
y = tapply(chinese$stars,chinese$city,mean)
y[which(x >= 20)]
plot(x,y)

x[162]
x[119]
chinese_Balzac = chinese[chinese$city == 'Balzac',]
qq = chinese[chinese$state == 'WI',]
length(table(qq$name))
qq = qq[-21092,]
qq = chinese_Madison[chinese_Madison$name == 'QQ Express',]
test = data.frame(text = qq$text, index = 1:nrow(qq), stringsAsFactors = FALSE)

x = tapply(qq$stars,qq$RestaurantsPriceRange2,mean)
y = tapply(qq$stars,qq$RestaurantsPriceRange2,mean)

write.csv(test,'/Applications/Study/UWM/628/module2/qq.csv')
