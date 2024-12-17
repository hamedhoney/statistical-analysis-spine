# Load necessary library
# install.packages("pwr")  # Uncomment this line to install the package if not already installed
library(pwr)
library(dplyr)

# Step 1: Read the CSV file
# Assuming the CSV has two columns: 'Group' (Male/Female) and 'Load'
# data <- read.csv("Summary-SpinalLoads.csv")
data <- read.csv("D:/Dissetation/statistical-analysis-spine/Summary-SpinalLoads.csv")

# Step 2: Calculate the mean and standard deviation for both groups
data <- data %>% filter(Sex == "FEMALE")
controls <- data[data$Status == "Control", "SuperiorResultant"]
patients <- data[data$Status == "Patient", "SuperiorResultant"]

mean_controls <- mean(controls)
mean_patients <- mean(patients)
sd_controls <- sd(controls)
sd_patients <- sd(patients)

# Step 3: Calculate effect size (Cohen's d)
pooled_sd <- sqrt(((length(controls) - 1) * sd_controls^2 + (length(patients) - 1) * sd_patients^2) / (length(controls) + length(patients) - 2))
cohen_d <- abs(mean_controls - mean_patients) / pooled_sd

# Step 4: Perform power analysis to find sample size for each group
power_target <- 0.60

# Use pwr.t.test for a two-sample t-test
sample_size <- pwr.t.test(d = cohen_d, power = power_target, type = "two.sample", alternative = "two.sided")

# Display results
cat("Required sample size per group for power of 90%:", ceiling(sample_size$n), "\n")
