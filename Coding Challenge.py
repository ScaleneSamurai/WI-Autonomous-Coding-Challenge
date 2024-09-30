import cv2
import numpy as np

# Load the image 'red.png'
image = cv2.imread('red.png')

# Create a 4x4 kernel of ones used for blurring the image
kernel = np.ones((4, 4), np.float32) / 25

# Apply the filter to the image using the kernel created above
image = cv2.filter2D(image, -1, kernel)

# Convert the image from BGR to HSV (Hue, Saturation, Value)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the lower and upper bounds for the color red in HSV space
lower_red1 = np.array([0, 190, 80])
upper_red1 = np.array([255, 255, 255])

# Create a mask that isolates pixels in the red range
mask = cv2.inRange(hsv, lower_red1, upper_red1)

# Find the contours (boundaries of shapes) from the masked image
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Initialize a list to store positions of the detected cones
cone_positions = []

# Loop through each contour to find the centroid of each
for contour in contours:
    # Calculate the moments of the contour to determine the center point
    M = cv2.moments(contour)
    # Check if the area is greater than 0
    if M["m00"] > 0:
        # Calculate the x and y coordinates of the centroid
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        # Only include cones that are located below y = 300
        if cy > 300:
            cone_positions.append((cx, cy))

# Initialize variables to calculate the average x position of cones
sum_first_values = 0
count = 0

# Calculate the sum of x-coordinates of all centroids
for x in cone_positions:
    sum_first_values += x[0]
    count += 1

# Calculate the midpoint of the x-coordinates
mid_x = sum_first_values / count

# Initialize two lists to store left and right cones
left_cones = []
right_cones = []

# Loop through the cone positions and classify them as left or right based on mid_x
for x in cone_positions:
    if x[0] < mid_x:
        left_cones.append(x)
    else:
        right_cones.append(x)

# Initialize lists to store the x and y coordinates of left cones
left_x_vals = []
left_y_vals = []

# Loop through the left cones and store their x and y coordinates separately
for x in left_cones:
    left_x_vals.append(x[0])
    left_y_vals.append(x[1])

# Perform a linear fit (find slope m and intercept b) for the left cone positions
m, b = np.polyfit(left_x_vals, left_y_vals, 1)

# Calculate the x coordinates where the left line intersects the top and bottom of the image
left_x_start = (2420 - b) / m
left_x_end = (0 - b) / m

# Initialize lists to store the x and y coordinates of right cones
right_x_vals = []
right_y_vals = []

# Loop through the right cones and store their x and y coordinates separately
for x in right_cones:
    right_x_vals.append(x[0])
    right_y_vals.append(x[1])

# Perform a linear fit (find slope m and intercept b) for the right cone positions
m, b = np.polyfit(right_x_vals, right_y_vals, 1)

# Calculate the x coordinates where the right line intersects the top and bottom of the image
right_x_start = (2420 - b) / m
right_x_end = (0 - b) / m

# Draw the left and right lines on the image
image = cv2.line(image, (int(left_x_start), 2420), (int(left_x_end), 0), (0,0,255), 3)
image = cv2.line(image, (int(right_x_start), 2420), (int(right_x_end), 0), (0,0,255), 3)

# Save the final image as 'answer.png'
cv2.imwrite('answer.png', image)