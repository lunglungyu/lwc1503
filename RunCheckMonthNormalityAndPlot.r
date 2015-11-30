require(lmtest)
source('~/Documents/lwc1503/packfyp/grangertestHack.R', chdir = 0);
folder<-format(Sys.time(),format("%Y%m%d_%H%M%S"));
dirdir <- sprintf("%s%s","~/Documents/",folder);
dir.create(path=dirdir,recursive=1);
sc<-read.csv2("~/Documents/lwc1503/packfyp/fypCutStation",header=0,stringsAsFactors = 0)
yearBegin <- 2005;
yearEnd <- 2014;
n <- nrow(sc);
normPeriod <- c();
notNormPeriod <- c();
normPeriod2 <- c();
notNormPeriod2 <- c();
library(nortest);
tot = vector(,12);
totnon = vector(,12);
tot2 = vector(,12);
tot2non = vector(,12);
outImage <- sprintf("normImage/allResult.png");
#outImage <- sprintf("normImage/allResult2.png");
print(outImage);
png(outImage);
monthc <-c(1:12);
xrange <- range(monthc);
yrange <- c(1,100);
#yrange <- range(vec);
#outImage <- sprintf("normImage/shapiro-%d.png",i);
#png(outImage);
plot(xrange,yrange,type="n",xlab="Month",ylab="Count");

for(j in c(1:12))tot[j]<-0;
for(j in c(1:12))totnon[j]<-0;
for(j in c(1:12))tot2[j]<-0;
for(j in c(1:12))tot2non[j]<-0;
for (i in c(yearBegin:yearEnd)){
	print(sprintf("Year %d",as.integer(i)));
	sad <- seq(as.Date(paste(as.character(i),"-02-01",sep="")), length=12, by="1 month") - 1
	count <- 0;
	noncount <- 0;
	count2 <- 0;
	noncount2 <- 0;
	vec = vector(,12);
	vec2 = vector(,12);
	vecnon = vector(,12);
	vec2non = vector(,12);
	for(j in c(1:12))vec[j]<-0;
	for(j in c(1:12))vec2[j]<-0;
	for(j in c(1:12))vecnon[j]<-0;
	for(j in c(1:12))vec2non[j]<-0;
	for (j in c(1:n)){
		SrcfileName <- sprintf("%s%s%s%s",sc[j,1],"-",i,".op");
		SrcfileName <- sprintf("%s%s","~/Documents/lwc1503/ChinaAll/",SrcfileName);
		#print(SrcfileName);
		if(file.exists(SrcfileName)){
			d1<- read.csv2(SrcfileName,header=0,skip=1,sep="",dec=".");
			colnames(d1)<- c("STN","WBAN","YEARMODA","TEMP","d1","DEWP","d2","SLP","d3","STP","d4","VISIB","d5","DSP","d6","MXSPD","GUST","MAX","MIN","PRCP","SNDP","FRSHTT");
			d1$YEARMODA <- as.Date(as.character(d1$YEARMODA),"%Y%m%d");
			for (mm in c(1:12)){
				options(scipen=10);
				mm2<-sprintf("%02d", mm);
				yyyymm<-sprintf("%s_%04d%02d", sc[j,1],i,mm);
				begind <- paste(as.character(i),mm2,"01",sep="-");
				endd <- sad[as.numeric(mm)];
				d1cut<- data.frame(subset(d1,(YEARMODA >= as.Date(begind,"%Y-%m-%d")) & (YEARMODA <= as.Date(endd,"%Y-%m-%d"))));
				if(nrow(d1cut)>0){
					testResult<-shapiro.test(d1cut$TEMP);
					if(testResult$p.value<0.05){
						noncount <- noncount+1;
						notNormPeriod <- c(notNormPeriod,yyyymm);
						vecnon[mm]<-vecnon[mm]+1;
					}else{
						count <- count +1;
						normPeriod <- c(normPeriod,yyyymm);
						vec[mm]<-vec[mm]+1;
					}
					testResult2<-ad.test(d1cut$TEMP);
					if(testResult2$p.value<0.05){#same in direction
						noncount2 <- noncount2+1;
						notNormPeriod2 <- c(notNormPeriod2,yyyymm);
						vec2non[mm]<-vec2non[mm]+1;
					}else{
						count2 <- count2 +1;
						normPeriod2 <- c(normPeriod2,yyyymm);
						vec2[mm]<-vec2[mm]+1;
					}

				}else{
					print("0 row");
				}
			}
		}else{
			print("file not exist");
		}
	}
	lines(x=monthc,y=vec,type="b",col="green");
	lines(x=monthc,y=vecnon,type="b",col="red");
	#dev.off();
	#outImage <- sprintf("normImage/ad-%d.png",i);
	#png(outImage);
	#plot(xrange,yrange,type="n");
	#lines(x=monthc,y=vec2,type="b",col="purple");
	#lines(x=monthc,y=vec2non,type="b",col="orange");
	#dev.off();
	print(sprintf("Shapiro-Wilk, Norm: %d NonNorm: %d",as.integer(count),as.integer(noncount)));
	print(vec);
	print(vecnon);
	print(sprintf("Anderson-Darling Test ,Norm: %d NonNorm: %d",as.integer(count2),as.integer(noncount2)));
	print(vec2);
	print(vec2non);
	tot <- tot+vec;
	tot2 <- tot2+vec2;
	totnon <- totnon+vecnon;
	tot2non <- tot2non+vec2non;
}
legend(xrange[1],yrange[2],c("Normal distributed(Shapiro-Wilk)","Non-normal distributed(Shaprio-Wilk)"),lwd=c(1.5,1.5),col=c("green","red"));
#legend(xrange[1],yrange[2],c("Normal distributed(Anderson-Darling)","Non-normal distributed(Anderson-Darling)"),lwd=c(1.5,1.5),col=c("purple","orange"));
#dev.off();
