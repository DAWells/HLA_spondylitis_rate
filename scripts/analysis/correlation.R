
library(ggplot2)

aa <- read.csv("data/processed/allele_freq_disease_rate.csv")
outliers <- aa[c(26),]
aa <- aa[c(-26),]
aa <- aa[!is.na(aa$Rate10.4),]

hist(aa$allele_freq)
hist(log(aa$allele_freq))

hist(aa[,'Rate10.4'])
hist(log(aa[,'Rate10.4']))


m1 <- lm(Rate10.4~allele_freq, data=aa)
plot(m1)
summary(m1)
new_data <- data.frame(
    allele_freq = seq(
        min(aa$allele_freq),
        max(aa$allele_freq),
        length.out = 100
    )
)
preds <- predict(m1, newdata = new_data, interval = "prediction")
confs <- predict(m1, newdata = new_data, interval = "confidence")
new_data$fit <- preds[, "fit"]
new_data$lwr_pred <- preds[, "lwr"]
new_data$upr_pred <- preds[, "upr"]
new_data$lwr_conf <- confs[, "lwr"]
new_data$upr_conf <- confs[, "upr"]
ggplot(aa, aes(allele_freq, Rate10.4)) +
  geom_point() +
  geom_line(data = new_data, aes(y = fit), color = "blue") +
  geom_ribbon(data = new_data, aes(y=fit,ymin = lwr_conf, ymax = upr_conf), alpha = 0.2, fill = "green") +
  geom_ribbon(data = new_data, aes(y=fit, ymin = lwr_pred, ymax = upr_pred), alpha = 0.1, fill = "red")

l1 <- lm(log(Rate10.4)~allele_freq, data=aa)
# plot(l1)
summary(l1)
new_data <- data.frame(
    allele_freq = seq(
        min(aa$allele_freq),
        max(aa$allele_freq),
        length.out = 100
    )
)
preds <- predict(l1, newdata = new_data, interval = "prediction")
confs <- predict(l1, newdata = new_data, interval = "confidence")
new_data$fit <- preds[, "fit"]
new_data$lwr_pred <- preds[, "lwr"]
new_data$upr_pred <- preds[, "upr"]
new_data$lwr_conf <- confs[, "lwr"]
new_data$upr_conf <- confs[, "upr"]
ggplot(aa, aes(allele_freq, log(Rate10.4))) +
  geom_point() +
  geom_point(data=outliers, colour="red")+
  geom_line(data = new_data, aes(y = fit), color = "blue") +
  geom_ribbon(data = new_data, aes(y=fit,ymin = lwr_conf, ymax = upr_conf), alpha = 0.2, fill = "green") +
  geom_ribbon(data = new_data, aes(y=fit, ymin = lwr_pred, ymax = upr_pred), alpha = 0.1, fill = "red")

ggplot(aa, aes(allele_freq, Rate10.4)) +
  geom_point() +
  geom_point(data=outliers, colour="red")+
  geom_line(data = new_data, aes(y = exp(fit)), color = "blue") +
  geom_ribbon(data = new_data, aes(y=exp(fit),ymin = exp(lwr_conf), ymax = exp(upr_conf)), alpha = 0.2, fill = "green") +
  geom_ribbon(data = new_data, aes(y=exp(fit), ymin = exp(lwr_pred), ymax = exp(upr_pred)), alpha = 0.1, fill = "red")
