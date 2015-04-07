#' ---
#' title: "MLB Payroll Analysis"
#' author: "Nicholas Ezyk"
#' date: "21 March 2015"
#' output: pdf_document
#' ---


#loading the payroll data from the Python document
payroll <- read.table("~/Documents/payroll.txt", header=TRUE, quote="\"")

summary(payroll)

bank <- payroll$PayrollMillions
wins <- payroll$X2014Wins

#displaying the mean and sd of payroll and wins (out of 162, of course)
mean(bank)
sd(bank)
mean(wins)
sd(wins)

#setting a linear regression
reg <- lm(wins ~ bank)
summary(reg)
#the regression is valid to significance < .10 (p-value .05072),
#but the R-squared is only .1296, a weak correlation

#a means of comparing the histogram to a normal distribution
histNorm <- function(x, densCol = "darkblue"){
  m <- mean(x)
  std <- sqrt(var(x))
  h <- max(hist(x,plot=FALSE)$density)
  d <- dnorm(x, mean=m, sd=std)
  maxY <- max(h,d)
  hist(x, prob=TRUE,
       xlab="x", ylim=c(0, maxY),
       main="(Probability) Histogram with Normal Density")
  curve(dnorm(x, mean=m, sd=std),
        col=densCol, lwd=2, add=TRUE)
}

#showing the histogram with normal distribution line
histNorm(reg$residuals, "purple")

#QQplots and Shapiro-Wilk test
qqnorm(reg$residuals)
qqline(reg$residuals)
shapiro.test(reg$residuals)
#p-value is .383; this can be considered a normal distribution

plot(reg$fitted.values,reg$residuals)
abline(h = 0)
#variances are wide, but in a channel

install.packages("lmtest", repos="http://cran.rstudio.com/")
library(lmtest)
bptest(reg)
#p-value of .849 give; we can assume variances are constant throughout the distribution

hats <- hatvalues(reg)

hatmu <- mean(hats)
hats[hats > 2 * hatmu]
#we get teams 14 and 19 with high leverage; the Dodgers and Yankees with their astronomical payrolls