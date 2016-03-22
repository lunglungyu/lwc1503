require(lmtest)
source('~/Documents/lwc1503/packfyp/grangertestHack.R', chdir = 0);
folder<-format(Sys.time(),format("%Y%m%d_%H%M%S"));
dirdir <- sprintf("%s%s","~/Documents/",folder);
dir.create(path=dirdir,recursive=1);
sc<-read.csv2("~/Documents/lwc1503/packfyp/fypCutStation",header=0,stringsAsFactors = 0)
yearBegin <- 2005;
yearEnd <- 2014;
limlag1 <- as.numeric(5);
limlag2 <- as.numeric(8);
n <- nrow(sc);
#yearBegin<-2014; n<-2;
for (i in c(yearBegin:yearEnd)){
	sad <- seq(as.Date(paste(as.character(i),"-02-01",sep="")), length=12, by="1 month") - 1
	for (j in c(1:n)){
		SrcfileName <- sprintf("%s%s%s%s",sc[j,1],"-",i,".op");
		SrcfileName <- sprintf("%s%s","~/Documents/lwc1503/ChinaAll/",SrcfileName);
		#print(SrcfileName);
		if(file.exists(SrcfileName)){
			d1<- read.csv2(SrcfileName,header=0,skip=1,sep="",dec=".");
			colnames(d1)<- c("STN","WBAN","YEARMODA","TEMP","d1","DEWP","d2","SLP","d3","STP","d4","VISIB","d5","DSP","d6","MXSPD","GUST","MAX","MIN","PRCP","SNDP","FRSHTT");
			d1$YEARMODA <- as.Date(as.character(d1$YEARMODA),"%Y%m%d");
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
						#thisHead  <- c(as.character(i),sc[j,1],sc[k,1]);
						#for (l in c(1:limlag)) {
						#	thisHead  <- c(thisHead,as.character(l));
						#}
						thisOutputFileName <- sprintf("%s-%s-%s.%s",as.character(i),sc[j,1],sc[k,1],"csv");
						thisOutputFileName <- sprintf("%s/%s",dirdir,thisOutputFileName);
						#write.table(t(thisHead), file=thisOutputFileName, append=T, row.names=F, col.names=F,  sep=",");
						for (mm in c(1:12)){
							mm2<-sprintf("%02d", mm);
							begind <- paste(as.character(i),mm2,"01",sep="-");
							endd <- sad[as.numeric(mm)];
							gggg<-sprintf("%s %s %s %s %s",as.character(i),sc[j,1],sc[k,1],begind,endd);
							#print(gggg);
							options(scipen=10);
							thisRec <- c(as.character(mm));
							d1cut<- data.frame(subset(d1,(YEARMODA >= as.Date(begind,"%Y-%m-%d")) & (YEARMODA <= as.Date(endd,"%Y-%m-%d"))));
							d2cut<- data.frame(subset(d2,(YEARMODA >= as.Date(begind,"%Y-%m-%d")) & (YEARMODA <= as.Date(endd,"%Y-%m-%d"))));
							if(nrow(d1cut)==nrow(d2cut) & nrow(d1cut)>0){
								tdata <- data.frame(d1cut$TEMP,d2cut$TEMP);
								colnames(tdata) <- c("t2","t6");
								tdata$t2<-c(0,diff(tdata$t2));
								tdata$t6<-c(0,diff(tdata$t6));
								for(lag in c(limlag1:limlag2)){
									# print(grangertest(t6 ~ t2  ,order=lag, data = tdata));
									thisRec<- c(thisRec,(grangertest(t6 ~ t2  ,order=lag, data = tdata)));
								}
								thisRec<-t(thisRec);
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

