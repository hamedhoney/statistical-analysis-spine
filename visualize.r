library(ggplot2)
library(dplyr)

data <- read.csv("Summary-SpinalLoads.csv")
data

# Assuming your data frame is called 'data'
plot_data <- data %>%
  group_by(Age, Sex, Status) %>%
  summarise(
    mean_load = mean(SuperiorResultant, na.rm = TRUE),
    se_load = sd(SuperiorResultant, na.rm = TRUE) / sqrt(n())
  )

ggplot(plot_data, aes(x = Age, y = mean_load, color = Sex, group = Sex)) +
  geom_line() +
  geom_point() +
  geom_errorbar(aes(ymin = mean_load - se_load, ymax = mean_load + se_load), width = 0.2) +
  facet_wrap(~ Status) +
  labs(title = "Impact of Age on Spinal Load by Sex and Patient Status",
       x = "Age Category",
       y = "Mean Spinal Load",
       color = "Sex") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))