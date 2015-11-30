require(xlsx)

data1 <- read.xlsx2("~/Documents/052.xls",1,startRow=6,endRow=45,header=FALSE)
colnames(data1) <- c("Year","Month","CompositeIndex","CompositeChangeRate","TypeAIndex","TypeAIndexChangeRate","TypeBIndex","TypeBIndexChangeRate","TypeCIndex","TypeCIndexChangeRate")

data2 <- read.xlsx2("~/Documents/052.xls",1,startRow=46,endRow=539,header=FALSE)
colnames(data2) <- c("Year","Month","CompositeIndex","CompositeChangeRate","TypeAIndex","TypeAIndexChangeRate","TypeBIndex","TypeBIndexChangeRate","TypeCIndex","TypeCIndexChangeRate")


