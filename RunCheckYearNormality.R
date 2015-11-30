require(lmtest)
library(nortest);
library(forecast);
#library(zoo);
source('~/Documents/lwc1503/packfyp/grangertestHack.R', chdir = 0);
folder<-format(Sys.time(),format("%Y%m%d_%H%M%S"));
dirdir <- sprintf("%s%s","~/Documents/",folder);
dir.create(path=dirdir,recursive=1);
sc<-read.csv2("~/Documents/lwc1503/packfyp/fypCutStation",header=0,stringsAsFactors = 0)
yearBegin <- 2003;
yearEnd <- 2012;
n <- nrow(sc);
normPeriod <- c();
notNormPeriod <- c();
normPeriod2 <- c();
notNormPeriod2 <- c();
#yearBegin<-2014; n<-2;
dfneed = vector(,20);
for(j in c(1:20))dfneed[j]<-0;
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
	#print(n);
	noncount <- 0;
	count <- 0;
	count2 <- 0;
	noncount2 <- 0;
	for (j in c(1:n)){
		SrcfileName <- sprintf("%s%s%s%s",sc[j,1],"-",i,".op");
		SrcfileName <- sprintf("%s%s","~/Documents/lwc1503/ChinaAll/",SrcfileName);
		#print(SrcfileName);
		if(file.exists(SrcfileName)){
			d1<- read.csv2(SrcfileName,header=0,skip=1,sep="",dec=".");
			colnames(d1)<- c("STN","WBAN","YEARMODA","TEMP","d1","DEWP","d2","SLP","d3","STP","d4","VISIB","d5","DSP","d6","MXSPD","GUST","MAX","MIN","PRCP","SNDP","FRSHTT");
			d1$YEARMODA <- as.Date(as.character(d1$YEARMODA),"%Y%m%d");
			d1 <- merge(AllDateInYear,d1,all.x=TRUE);
			#print(nrow(d1));
			testResult<-shapiro.test(d1$TEMP);
			#print(sprintf("%d %d",i,j));
			if(testResult$p.value<0.05){
				noncount <- noncount+1;
			}else{
				count <- count+1;
			}
			testResult2<-ad.test(d1$TEMP);
			if(testResult2$p.value<0.05){#same in direction
				noncount2 <- noncount2+1;
				notNormPeriod2 <- c(notNormPeriod2,as.integer(i));
			}else{
				count2 <- count2 +1;
				normPeriod2 <- c(normPeriod2,as.integer(i));
			}
			need<-ndiffs(d1$TEMP);
			if(need>0)dfneed[need] <- dfneed[need]+1;
			#print(shapiro.test(d1$TEMP));
		}else {
			print("d1 not exist");
			print(sc[j,1]);
		}
	}
	print(sprintf("Shapiro-Wilk, Norm: %d NonNorm: %d",as.integer(count),as.integer(noncount)));
	print(sprintf("Anderson-Darling Test ,Norm: %d NonNorm: %d",as.integer(count2),as.integer(noncount2)));
	print(dfneed);
}
print(dfneed);

