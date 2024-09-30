# WI-Autonomous-Coding-Challenge
### answer.png
<img src="https://github.com/user-attachments/assets/f9d71392-0e8d-496a-b9f3-4a3a18177d94" width="454" height="605">

### Methodology
I first blurred the image using 2D convolution to reduce noise and small variations in the pixels. I then used color thresholding to create a mask where red areas are white and non-red areas are black. Then I found the contours of the shapes in the mask, which are the outlines of potential cones. For each contour, I calculated its center point using image moments. I only kept the center points located below a certain vertical threshold so that the red lights on the ceiling were not mistaken for cones. Then I calculated the average x-value of the cones and split the cones into left and right groups based on their position. I used linear regression to find the slope and intercept of the line through the left cones and a line through the right cones. Lastly, I drew the lines on the image and saved it as answer.png.
### Failed Attempts
One thing that I tried that didn't work was applying the color thresholding without blurring first. This didn't work because there was too much variation in the red pixels that I couldn't accurately color threshold without either including other red pixels not in the cones or not including all the pixels in the cones. This led to too many contours, which messed up the rest of the code. Another thing I tried was using the linear regression without placing the vertical threshold for the center points. This caused the left line to be off because it included the red lights on the ceiling as cones.
### Libraries Used
OpenCV and NumPy
