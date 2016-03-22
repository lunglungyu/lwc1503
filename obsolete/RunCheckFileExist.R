require(lmtest)
source('~/Documents/lwc1503/packfyp/grangertestHack.R', chdir = 0);
folder<-format(Sys.time(),format("%Y%m%d_%H%M%S"));
dirdir <- sprintf("%s%s","~/Documents/",folder);
dir.create(path=dirdir,recursive=1);
sc<-read.csv2("~/Documents/lwc1503/packfyp/fypCutStation",header=0,stringsAsFactors = 0)
yearBegin <- 2013;
yearEnd <- 2015;
limlag1 <- as.numeric(1);
limlag2 <- as.numeric(5);
n <- nrow(sc);
#yearBegin<-2014; n<-2;
for (i in c(yearBegin:yearEnd)){
	print("Year");
	print(i);
	sad <- seq(as.Date(paste(as.character(i),"-02-01",sep="")), length=12, by="1 month") - 1
	Year <- i;
	YearBegin <- paste(as.character(Year),"-01-01",sep="");
	YearEnd <-  paste(as.character(Year),"-12-31",sep="");
	AllDateInYear <- data.frame(seq.Date(as.Date(YearBegin),as.Date(YearEnd),"day"));
	colnames(AllDateInYear) <- c("YEARMODA");
	thisOutputFileName <- sprintf("%s.%s","abc","csv");
	thisOutputFileName <- sprintf("%s/%s",dirdir,thisOutputFileName);
	print(n);
	for (j in c(1:n)){
		SrcfileName <- sprintf("%s%s%s%s",sc[j,1],"-",i,".op");
		SrcfileName <- sprintf("%s%s","~/Documents/lwc1503/ChinaAll/",SrcfileName);
		#print(SrcfileName);
		if(file.exists(SrcfileName)){
			d1<- read.csv2(SrcfileName,header=0,skip=1,sep="",dec=".");
			colnames(d1)<- c("STN","WBAN","YEARMODA","TEMP","d1","DEWP","d2","SLP","d3","STP","d4","VISIB","d5","DSP","d6","MXSPD","GUST","MAX","MIN","PRCP","SNDP","FRSHTT");
			d1$YEARMODA <- as.Date(as.character(d1$YEARMODA),"%Y%m%d");
			d1 <- merge(AllDateInYear,d1,all.x=TRUE);
		}else {
			print(sprintf("%d %s not exist",i,sc[j,1]));
		}
	}
}

