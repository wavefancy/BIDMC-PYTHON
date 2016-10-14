# Compare the rates of two possision distribution.
# Input format: name, count1, count2, backgroundCount1, background2.
# Alternative test: count1 > count2 (greater)
# Output the pvalue at the last column. 

library(rateratio.test)
library(abind)

inData = read.table(file("stdin"))

#PossionCompPvalue = function(oCount1, oCount2, background1, background2){
PossionCompPvalue = function(x){
  oRare = c(x[1],x[2])
  background = c(x[3],x[4])
  
  #rateratio.test(c(2,9),c(n,m))
  rateratio.test(oRare, background,alternative = "greater")$p.value
}

x = apply(inData[,2:5],1,PossionCompPvalue)
out = abind(inData,x)

write.table(out, stdout(), col.names = F, row.names = F, quote = F, sep='\t')

