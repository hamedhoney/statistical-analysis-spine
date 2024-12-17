
library(pwr)
library(dplyr)

# data <- read.csv("Summary-SpinalLoads.csv")
# data <- read.csv("D:/Dissetation/statistical-analysis-spine/Summary-SpinalLoads.csv")
data <- read.csv("D:/Dissetation/statistical-analysis-spine/Summary-Spinal Loads.csv")


# data <- data %>% filter(Status == "Patient")
data$Decade <- factor(data$Decade)

anova_result <- aov(SuperiorResultant ~ Decade, data = data)


anova_summary <- summary(anova_result)

ss_treatment <- anova_summary[[1]]["Decade", "Sum Sq"]  # Use the first component for ANOVA table
ss_total <- sum((data$SuperiorResultant - mean(data$SuperiorResultant))^2)
eta_squared <- ss_treatment / ss_total

cat("Eta squared (η²) is:", eta_squared, "\n")

Decade_groups <- data %>%
  group_by(Decade) %>%
  summarise(
    mean_load = mean(SuperiorResultant, na.rm = TRUE),
    sd_load = sd(SuperiorResultant, na.rm = TRUE),
    n = n()
  )


overall_mean <- mean(data$SuperiorResultant, na.rm = TRUE)
k <- nrow(Decade_groups)  # Number of Decade groups

# Cohen's f = sqrt(η² / (1 - η²))
# For simplicity, we'll use a small effect size (0.25) for power analysis, but you can adjust based on prior studies

# eta_squared <- 0.080# This corresponds to a medium effect size
cohen_f <- sqrt(eta_squared / (1 - eta_squared))

power_target <- 0.90

# Calculate sample size required for ANOVA
sample_size <- pwr.anova.test(k = k, f = cohen_f, power = power_target)

# Display results
cat("Required sample size per group for power of 90%:", ceiling(sample_size$n), "\n")