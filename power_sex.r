# Load necessary library
# install.packages("pwr")  # Uncomment this line to install the package if not already installed
library(pwr)
library(dplyr)


# data <- read.csv("Summary-SpinalLoads.csv")
data <- read.csv("D:/Dissetation/statistical-analysis-spine/Summary-SpinalLoads.csv")

# data <- data %>% filter(Status == "Patient")
males <- data[data$Sex == "MALE", "SuperiorResultant"]
females <- data[data$Sex == "FEMALE", "SuperiorResultant"]

mean_male <- mean(males)
mean_female <- mean(females)
sd_male <- sd(males)
sd_female <- sd(females)

# Step 3: Calculate effect size (Cohen's d)
pooled_sd <- sqrt(((length(males) - 1) * sd_male^2 + (length(females) - 1) * sd_female^2) / (length(males) + length(females) - 2))
cohen_d <- abs(mean_male - mean_female) / pooled_sd

# Step 4: Perform power analysis to find sample size for each group
power_target <- 0.90

# Use pwr.t.test for a two-sample t-test
sample_size <- pwr.t.test(d = cohen_d, power = power_target, type = "two.sample", alternative = "two.sided")

# Display results
cat("Required sample size per group for power of 90%:", ceiling(sample_size$n), "\n")
