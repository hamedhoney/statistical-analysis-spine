
# Random Effects Model:
# Your current mixed-effects model with Subject as a random effect is still appropriate and helps account for individual variability.
# Statistical Approaches:
# a) Include Subject-Centered Effects:
# We can create a subject-centered version of the categorical age variable. This approach, sometimes called "within-cluster centering" for categorical variables, can help separate within-subject from between-subject effects.
# Here's how you might implement this in R:

library(lme4)
library(lmerTest)
library(dplyr)

# Create subject-centered age variable
your_data <- your_data %>%
  group_by(Subject) %>%
  mutate(
    MeanAge = mean(as.numeric(Age)),
    CenteredAge = as.numeric(Age) - MeanAge
  ) %>%
  ungroup()

# Modify your model
model <- lmer(SpinalLoad ~ Age + CenteredAge + Sex * Status + (1|Subject), data = your_data)

summary(model)
anova(model)

library(ggplot2)

ggplot(your_data, aes(x = Age, y = SpinalLoad, group = Subject, color = Subject)) +
  geom_line(alpha = 0.3) +  # Individual subject trajectories
  geom_point(size = 2) +    # Data points
  stat_summary(aes(group = 1), fun = mean, geom = "line", color = "red", size = 1.5) +  # Overall trend
  facet_grid(Sex ~ Status) +
  labs(title = "Spinal Load vs Age: Individual Trajectories and Overall Trend",
       x = "Age Category", y = "Spinal Load") +
  theme_minimal() +
  theme(legend.position = "none")  # Hide subject legend for clarity
