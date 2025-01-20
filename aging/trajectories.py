import json
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Path where motion.json files are stored
path = 'E:/Quanitifying EMG/data/20/Visit/trials/15/*/'  # Assuming subject folders are nested

# List all the motion.json files in the directory (you can modify this if needed)
files = glob.glob(os.path.join(path, 'motion.json'))
path = 'E:/Quanitifying EMG/data/21/Visit/trials/15/*/'  # Assuming subject folders are nested
files = files + glob.glob(os.path.join(path, 'motion.json'))
path = 'E:/Quanitifying EMG/data/22/Visit/trials/15/*/'  # Assuming subject folders are nested
files = files + glob.glob(os.path.join(path, 'motion.json'))
path = 'E:/Quanitifying EMG/data/25/Visit/trials/15/*/'  # Assuming subject folders are nested
files = files + glob.glob(os.path.join(path, 'motion.json'))

# Initialize lists to store data from all files
all_lumbar_angles = []
all_lumbar_velocities = []

# Initialize variables to track the min/max across all files
min_lumbar_angle = float('inf')
max_lumbar_angle = float('-inf')
min_lumbar_velocity = float('inf')
max_lumbar_velocity = float('-inf')

# Iterate through each motion.json file
for file in files:
    # Load the JSON data from the file
    with open(file, 'r') as f:
        motion = json.load(f)
    
    # Extract lumbar angle (position) and lumbar velocity (velocity)
    lumbar_angle = np.array(motion['analyses'][0]['position']['signal'])-np.mean(motion['analyses'][0]['position']['signal'])
    lumbar_velocity = np.array(motion['analyses'][0]['velocity']['signal'])
    
    # Store the data
    all_lumbar_angles.append(lumbar_angle)
    all_lumbar_velocities.append(lumbar_velocity)
    
    # Update the global min and max values
    min_lumbar_angle = min(min_lumbar_angle, np.min(lumbar_angle))
    max_lumbar_angle = max(max_lumbar_angle, np.max(lumbar_angle))
    min_lumbar_velocity = min(min_lumbar_velocity, np.min(lumbar_velocity))
    max_lumbar_velocity = max(max_lumbar_velocity, np.max(lumbar_velocity))
    # Plotting the Phase Plot for each file with a unique color
    plt.plot(lumbar_angle, lumbar_velocity,)  # Using the colormap for different colors

# Flatten the lists for plotting
all_lumbar_angles = np.concatenate(all_lumbar_angles)
all_lumbar_velocities = np.concatenate(all_lumbar_velocities)

# Plotting the Phase Plot (Lumbar Angle vs. Lumbar Velocity)
# plt.figure(figsize=(8, 8))
# plt.plot(all_lumbar_angles, all_lumbar_velocities, label="Phase Plot")

# Set the axis limits based on the min/max range
plt.xlim(min_lumbar_angle, max_lumbar_angle)
plt.ylim(min_lumbar_velocity, max_lumbar_velocity)

# Adding labels and title
plt.title("Phase Plot of Lumbar Angle vs. Lumbar Velocity Across All Subjects")
plt.xlabel("Lumbar Angle (Degrees)")
plt.ylabel("Lumbar Velocity (Degrees/Second)")
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.legend()

plt.gca().set_aspect(.25, adjustable='box') 

plt.tight_layout()
plt.show()
