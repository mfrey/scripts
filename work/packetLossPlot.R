# A script for generating the bar plots depicting the packet losses of a series 
# of experiments. In addition, a box plot is generated. 

# Data looks the follow way:
# 
#  65 62 4 64129
#  ...
#
# The columns indicate (in their particular order): transmitted packets, received 
# packets, packet loss in %, time

# Author: Michael Frey

# add dependency to ggplot for generating plots
library(ggplot2,lib.loc="~/.R/library");

# a function which creates a data.frame()
createDataFrame <- function(data, column){
  numericValueList <- c(as.numeric(data[,column]));
  dataFrame <- data.frame(iteration=factor(c(1:length(numericValueList)), levels=c(1:length(numericValueList))), packet_loss=numericValueList); 
  return (dataFrame);
}

# read the files in a directory
files <- dir();

# box plot data.frame
boxPlotDataFrame <- data.frame();

# iterate over every file in the directory
for(i in 1:length(files)){
  # read the file into a table
  packets <- read.table(file=files[i], header=FALSE);
  # create the headlines for the table
  colnames(packets) <- c("transmitted", "received", "packet loss", "time");
  # transform table into a data.frame containing the packet losses
  dataFrame <- createDataFrame(packets, 3);
  # fill up the box plot data frame
  numericValueList <- c(as.numeric(packets[,3]));
  rbind(boxPlotDataFrame,data.frame(id=c(rep(1,length(numericValueList))),packet_loss=numericValueList)) -> boxPlotDataFrame;
  # write png to file 'packet_loss_bar' +  files[i] + '.png'
  png(file=paste("packet_loss_bar", files[i], ".png"));
  # create plot
  barPlot <- ggplot(data=dataFrame, aes(x=iteration, y=packet_loss));
  barPlot <- barPlot + scale_x_discrete('iteration') + scale_y_continuous('packet loss [%]') + geom_bar();
  print(barPlot);
  # finish writing data
  dev.off();
}

# write the box plot
png(file=paste("packet_loss_box",".png"));
file <- ggplot(data=boxPlotDataFrame, aes_string(x="1", y="packet_loss"));
file <- file + scale_x_continuous('series') + scale_y_continuous('packet loss [%]')
file <- file + scale_x_continuous(breaks=NULL)
file <- file + geom_boxplot();
print(file);
dev.off();



