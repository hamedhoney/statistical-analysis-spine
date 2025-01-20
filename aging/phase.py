import json
import numpy as np
import matplotlib.pyplot as plt

# Simulating cyclic kinematic data (lumbar angle and lumbar velocity)
path = 'E:/Quanitifying EMG/data/60/Visit/trials/10/Low Back Slow Lateral Range Features/'
motion = json.load(open(path+'motion.json'))
# Simulate real (lumbar angle) and imaginary (lumbar velocity) parts of the kinematic data

# Real part: Lumbar angle (sine wave)
lumbar_angle = np.array(motion['analyses'][0]['position']['signal'])

# Imaginary part: Lumbar velocity (derivative of lumbar angle, cosine wave)
lumbar_velocity = np.array(motion['analyses'][0]['velocity']['signal'])

# Plotting the Phase Plot (Lumbar Angle vs. Lumbar Velocity)
plt.figure(figsize=(8, 8))
plt.plot(lumbar_angle, lumbar_velocity, label="Phase Plot", color="b")

# Adding labels and title
plt.title("Phase Plot of Lumbar Angle vs. Lumbar Velocity")
plt.xlabel("Lumbar Angle (Degrees)")
plt.ylabel("Lumbar Velocity (Degrees/Second)")
plt.grid(True)
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.legend()

# Display the plot
plt.gca().set_aspect('equal', adjustable='box')  # Ensure equal scaling on both axes
plt.tight_layout()
plt.show()
