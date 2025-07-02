
library(ggplot2)

fulldata <- read.csv("data/processed/allele_freq_disease_rate.csv")
outliers <- fulldata[fulldata$country %in% c("Finland"),]
knownrates <- fulldata[!is.na(fulldata$Rate10.4),]
knownrates <- knownrates[!knownrates$country %in% c("Finland"),]
predrates <- fulldata[is.na(fulldata$Rate10.4),]

hist(knownrates$allele_freq)
hist(log(knownrates$allele_freq))

hist(knownrates[,'Rate10.4'])
hist(log(knownrates[,'Rate10.4']))


m1 <- lm(Rate10.4~allele_freq, data=knownrates)
plot(m1)
summary(m1)
new_data <- data.frame(
    allele_freq = seq(
        min(knownrates$allele_freq),
        max(knownrates$allele_freq),
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
ggplot(knownrates, aes(allele_freq, Rate10.4)) +
  geom_point() +
  geom_line(data = new_data, aes(y = fit), color = "blue") +
  geom_ribbon(data = new_data, aes(y=fit,ymin = lwr_conf, ymax = upr_conf), alpha = 0.2, fill = "green") +
  geom_ribbon(data = new_data, aes(y=fit, ymin = lwr_pred, ymax = upr_pred), alpha = 0.1, fill = "red")

l1 <- lm(log(Rate10.4)~allele_freq, data=knownrates)
# plot(l1)
summary(l1)
trends <- data.frame(
    allele_freq = seq(
        min(knownrates$allele_freq),
        max(knownrates$allele_freq),
        length.out = 100
    )
)
preds <- predict(l1, newdata = trends, interval = "prediction")
confs <- predict(l1, newdata = trends, interval = "confidence")
trends$fit <- preds[, "fit"]
trends$lwr_pred <- preds[, "lwr"]
trends$upr_pred <- preds[, "upr"]
trends$lwr_conf <- confs[, "lwr"]
trends$upr_conf <- confs[, "upr"]

predrates$predrate <- predict(l1, newdata=predrates)
inrange <- predrates$allele_freq >= min(trends$allele_freq) & predrates$allele_freq <= max(trends$allele_freq)
predrates_inrange <-  predrates[inrange,]
predrates_outrange <-  predrates[!inrange,]

ggplot(knownrates, aes(allele_freq, log(Rate10.4))) +
  geom_ribbon(data = trends, aes(y=fit,ymin = lwr_conf, ymax = upr_conf), alpha = 0.2, fill = NA, outline.type = "both", linetype = "dashed",colour="black") +
  geom_ribbon(data = trends, aes(y=fit, ymin = lwr_pred, ymax = upr_pred), alpha = 0.4, fill = "lightgrey")+
  geom_point(size=3) +
  geom_point(data=predrates_inrange, aes(y=predrate), colour="darkcyan", shape=1, size=3)+
  geom_point(data=predrates_outrange, aes(y=predrate), colour="orange", shape=1, size=3)+
  geom_point(data=outliers, colour="firebrick", size=3)+
  # geom_line(data = trends, aes(y = fit), color = "black") +
  xlab("Allele B27 frequency")+
  ylab("log Rate per 10,000")+
  xlim(0,0.082)+
  ylim(0,6)+
  theme_bw()
  ggsave("cor.png")

knownrates$type <- "known"
knownrates$predrate <- NA
predrates_inrange$type <- "predin"
predrates_outrange$type <- "predout"

known_pred_rates <- rbind(
  knownrates,
  rbind(
    predrates_inrange,
    predrates_outrange
  )
)
write.csv(known_pred_rates, "data/processed/known_pred_rates.csv")

# ggplot(knownrates, aes(allele_freq, Rate10.4)) +
#   geom_ribbon(data = trends, aes(y=exp(fit),ymin = exp(lwr_conf), ymax = exp(upr_conf)), alpha = 0.2, fill = NA, outline.type = "both", linetype = "dashed",colour="black") +
#   geom_ribbon(data = trends, aes(y=exp(fit), ymin = exp(lwr_pred), ymax = exp(upr_pred)), alpha = 0.4, fill = "lightgrey")+
#   geom_point() +
#   geom_point(data=predrates_inrange, aes(y=exp(predrate)), colour="darkgreen", shape=1)+
#   geom_point(data=predrates_outrange, aes(y=exp(predrate)), colour="orange", shape=1)+
#   geom_point(data=outliers, colour="red")+
#   geom_line(data = trends, aes(y = exp(fit)), color = "black") +
#   theme_bw()

ggplot(aa, aes(allele_freq, Rate10.4)) +
  geom_point() +
  geom_point(data=outliers, colour="red")+
  geom_line(data = new_data, aes(y = exp(fit)), color = "blue") +
  geom_ribbon(data = new_data, aes(y=exp(fit),ymin = exp(lwr_conf), ymax = exp(upr_conf)), alpha = 0.2, fill = "green") +
  geom_ribbon(data = new_data, aes(y=exp(fit), ymin = exp(lwr_pred), ymax = exp(upr_pred)), alpha = 0.1, fill = "red")
