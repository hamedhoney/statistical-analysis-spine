library(lme4)
library(lmerTest)

data <- read.csv("Summary-SpinalLoads.csv")
data
# Ensure Age is treated as a factor (categorical)
your_data$Age <- factor(your_data$Age)
# Treat Age, Sex, and Status as fixed effects
# treat Subject and Task as random effects
model <- lmer(SuperiorResultant ~ Age * Sex * Status + (1|Subject) + (1|Trial.Name), data = data)

summary(model)
anova(model)
# post-hoc

library(emmeans)

# For the Age main effect
age_emm <- emmeans(model, ~ Age)
pairs(age_emm, adjust = "tukey")

# For Age*Status interaction
age_status_emm <- emmeans(model, ~ Age * Status)
pairs(age_status_emm, adjust = "tukey")