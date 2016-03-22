args<-commandArgs(TRUE);
require(lmtest)
library(forecast)
library(zoo)
source('~/Documents/lwc1503/packfyp/grangertestHack.R', chdir = 0);
folder<-format(Sys.time(),format("%Y%m%d_%H%M%S"));
dirdir <- sprintf("%s%s","~/Documents/",folder);
dir.create(path=dirdir,recursive=1);
sc<-read.csv2("~/Documents/lwc1503/packfyp/fypCutStation",header=0,stringsAsFactors = 0)
yearBegin <- as.integer(args[1]);
yearEnd <- as.integer(args[2]);
print(yearBegin);
print(yearEnd);
#q();
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
	for (j in c(1:n)){
		SrcfileName <- sprintf("%s%s%s%s",sc[j,1],"-",i,".op");
		SrcfileName <- sprintf("%s%s","~/Documents/lwc1503/ChinaAll/",SrcfileName);
		#print(SrcfileName);
		if(file.exists(SrcfileName)){
			d1<- read.csv2(SrcfileName,header=0,skip=1,sep="",dec=".");
			colnames(d1)<- c("STN","WBAN","YEARMODA","TEMP","d1","DEWP","d2","SLP","d3","STP","d4","VISIB","d5","DSP","d6","MXSPD","GUST","MAX","MIN","PRCP","SNDP","FRSHTT");
			d1$YEARMODA <- as.Date(as.character(d1$YEARMODA),"%Y%m%d");
			#as.numeric(levels(d1$STP))[d1$STP]
			d1 <- merge(AllDateInYear,d1,all.x=TRUE,na.rm=FALSE);
			d1$STP <- na.approx(d1$STP,na.rm=FALSE);
			d1$STP <- replace(d1$STP, is.na(d1$STP), median(d1$STP, na.rm=TRUE));
			for(k in c(1:n)){
				# print(k);
				if(j!=k){
					DstfileName <- sprintf("%s%s%s%s",sc[k,1],"-",i,".op");
					DstfileName <- sprintf("%s%s","~/Documents/lwc1503/ChinaAll/",DstfileName);
					#print(DstfileName);
					if(file.exists(DstfileName)){

						d2<- read.csv2(DstfileName,header=0,skip=1,sep="",dec=".");
						colnames(d2)<- c("STN","WBAN","YEARMODA","TEMP","d1","DEWP","d2","SLP","d3","STP","d4","VISIB","d5","DSP","d6","MXSPD","GUST","MAX","MIN","PRCP","SNDP","FRSHTT");
						d2$YEARMODA <- as.Date(as.character(d2$YEARMODA),"%Y%m%d");
						#as.numeric(levels(d2$STP))[d2$STP]
						d2 <- merge(AllDateInYear,d2,all.x=TRUE,na.rm=FALSE);
						#thisHead  <- c(as.character(i),sc[j,1],sc[k,1]);
						#for (l in c(1:limlag)) {
						#	thisHead  <- c(thisHead,as.character(l));
						#}
						#thisOutputFileName <- sprintf("%s-%s-%s.%s",as.character(i),sc[j,1],sc[k,1],"csv");
						#thisOutputFileName <- sprintf("%s/%s",dirdir,thisOutputFileName);
						#write.table(t(thisHead), file=thisOutputFileName, append=T, row.names=F, col.names=F,  sep=",");
								d2$STP <- na.approx(d2$STP,na.rm=FALSE);
								d2$STP <- replace(d2$STP, is.na(d2$STP), median(d2$STP, na.rm=TRUE));
								#print(d1);
								#print(d2);
						for (mm in c(1:12)){
							thisRec<-c(sc[j,1],sc[k,1],as.character(Year));
							print(sprintf("%s %s %s",as.character(j),as.character(k),as.character(mm)));
							mm2<-sprintf("%02d", mm);
							begind <- paste(as.character(i),mm2,"01",sep="-");
							endd <- sad[as.numeric(mm)];
							#print(begind);
							#print(endd);
							gggg<-sprintf("%s %s %s %s %s",as.character(i),sc[j,1],sc[k,1],begind,endd);
							#print(gggg);
							options(scipen=10);
							thisRec <- c(thisRec,as.character(mm));
							d1cut<- data.frame(subset(d1,(YEARMODA >= as.Date(begind,"%Y-%m-%d")) & (YEARMODA <= as.Date(endd,"%Y-%m-%d"))));
							d2cut<- data.frame(subset(d2,(YEARMODA >= as.Date(begind,"%Y-%m-%d")) & (YEARMODA <= as.Date(endd,"%Y-%m-%d"))));
							#print(d1cut);
							#print(d2cut);
							if(nrow(d1cut)==nrow(d2cut) & nrow(d1cut)>0){
								#print(sprintf("cut rownum:%d",nrow(d1cut)));
								stationaryTS1 <- d1cut$STP;
								stationaryTS2 <- d2cut$STP;
								if(mean(stationaryTS1)>=5000.0)next;
								if(mean(stationaryTS2)>=5000.0)next;
								#stationaryTS1 <- na.approx(stationaryTS1);
								#stationaryTS2 <- na.approx(stationaryTS2);
								#print(str(stationaryTS1));
								#print(str(stationaryTS2));
								stationaryTS1 <- diff(stationaryTS1,differences=2);
								stationaryTS2 <- diff(stationaryTS2,differences=2);
								#print(stationaryTS1);
								#print(stationaryTS2);
								#print(sprintf("have rownum:%d %d",as.integer(nrow(stationaryTS1)),as.integer(nrow(stationaryTS2))));
								tdata <- data.frame(stationaryTS1,stationaryTS2);
								#tdata <- data.frame(d1cut$STP,d2cut$STP);
								colnames(tdata) <- c("t2","t6");
								tdata$t2<-c(0,diff(tdata$t2));
								tdata$t6<-c(0,diff(tdata$t6));
								for(lag in c(limlag1:limlag2)){
									# print(grangertest(t6 ~ t2  ,order=lag, data = tdata));
									thisRec<- c(thisRec,(grangertest(t6 ~ t2  ,order=lag, data = tdata)));
								}
								thisRec<-t(thisRec);
								#print(thisRec);
								write.table(thisRec, file=thisOutputFileName, append=T, row.names=F, col.names=F,  sep=",");
							}else{
								monthfail <- sprintf("%s %s %s %s %s %s %s %s %s %s",sc[j,1],sc[k,1],as.character(i),as.character(mm),nrow(d1),nrow(d2),nrow(d1cut),nrow(d2cut),begind,endd);
								print(monthfail);
							}
						}
					}
				}
			}
		}
	}
}
