library(ggplot2)

# data <- read.csv("D:/Dissetation/statistical-analysis-spine/Summary-SpinalLoads.csv")
data <- read.csv("Summary-SpinalLoads.csv")
ggplot(data, aes(x = Age, y = SuperiorResultant, group = Subject, color = Subject)) +
  geom_line(alpha = 0.3) +  # Individual subject trajectories
  geom_point(size = 2) +    # Data points
  stat_summary(aes(group = 1), fun = mean, geom = "line", color = "#09ff00", size = 1.5) +  # Overall trend
  facet_grid(Sex ~ Status) +
  labs(title = "Spinal Load vs Age: Individual Trajectories and Overall Trend",
       x = "Age Category", y = "Spinal Load") +
  theme_minimal() +
  theme(legend.position = "none")  # Hide subject legend for clarity