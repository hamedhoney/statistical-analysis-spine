if (!require(rms)) install.packages("rms")

library(rms)

# Load the CSV file with spinal load data
# data <- read.csv("Summary-SpinalLoads.csv")
data <- read.csv("D:/Dissetation/statistical-analysis-spine/Summary-SpinalLoads.csv")
# Assuming the CSV contains columns 'SpinalLoad' and 'Gender'
# Filter the data for males and females
male_data <- data[data$Sex == "MALE", "SuperiorResultant"]
female_data <- data[data$Sex == "FEMALE", "SuperiorResultant"]

# Function to calculate p-value based on spinal loads of males and females
tmpfun <- function(male_loads, female_loads, n) {
  # Take samples from the data
  male_sample <- sample(male_loads, n, replace = TRUE)
  female_sample <- sample(female_loads, n, replace = TRUE)

  # Create a combined data frame with a 'Gender' column
  spinal_loads <- c(male_sample, female_sample)
  gender <- factor(c(rep("MALE", n), rep("FEMALE", n)))

  # Fit a linear model to differentiate males and females
  fit <- lrm(gender ~ spinal_loads)

  # Return the p-value
  return(fit$stats[5])
}

# Function to perform power analysis and calculate sample size
calculate_sample_size <- function(male_data, female_data, alpha = 0.05, power = 0.8, max_n = 100) {
  for (n in 10:max_n) {
    # Replicate the simulation to calculate the proportion of p-values below alpha
    out <- replicate(1000, tmpfun(male_data, female_data, n))
    if (mean(out < alpha) >= power) {
      return(n)  # Return the sample size needed for the desired power
    }
  }
  return(NA)  # Return NA if the sample size exceeds the maximum
}

# Call the function with desired parameters
sample_size <- calculate_sample_size(male_data, female_data)
cat("Required sample size for desired power:", sample_size, "\n")
