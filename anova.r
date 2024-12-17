install.packages("lme4")
install.packages("lmerTest")  # For p-values in mixed models
library(lme4)
library(lmerTest)

data <- read.csv("Summary-SpinalLoads.csv")

model <- lmer(SuperiorResultant ~ Sex * Age * Status + (1 | Subject), data = data)
summary(model)

anova(model)

# post-hoc
# install.packages("emmeans")
library(emmeans)

emmeans(model, pairwise ~ sex | age | patient_status)
