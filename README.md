## Writeup Template

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)
[calibration]: ./writeup_images/calibration.png "Calibration"
[undistorted]: ./writeup_images/distorted_vs_undistorted_full.png "Undistorted"
[undistorted1]: ./output_images/undistorted_images/straight_lines1.jpg "Road Transformed"
[threshold_comparison]: ./writeup_images/threshold_comparison.png "Threshold plot"
[binary_activation]: ./output_images/thresholded_images/straight_lines1.jpg "Binary Example"
[binary_activation1]: ./writeup_images/binary_activation.png "Binary Example"
[perspective_roi_histogram]: ./writeup_images/perspective_roi_histogram.png "Warp Example"
[curve_image]: ./output_images/curve_images/straight_lines1.jpg "Fit Visual"
[line_plot]: ./output_images/line_images/straight_lines1.png "Line Plot"
[output]: ./output_images/final_output/straight_lines1.jpg "Output"
[video1]: ./res_vid.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf. 

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in ["./calibrate.py"](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/calibrate.py) and is used in  blocks ln[3], ln[33] in the file called [`advanced_lane_lines.ipynb`](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/advanced_lane_lines.ipynb).  

The functionality is wrapped inside a class `Calibrate(images,nx,ny)` that stores the necessary information once instantiated with the parameters:
* images: List of filepaths to the images for calibration
* nx: number of inside corners along x
* ny: number of inside corners along y 

To undistort an image simply call `undistort(img)` on the instance object.

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][calibration]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][undistorted1]
The complete list of undistorted images is available [here](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/tree/master/output_images/undistorted_images)
#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

The code for this step is contained in ["./thresholdutil.py"](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/thresholdutil.py) which contains utility functions for the thresholding and in blocks ln[4], ln[7] in the file called [`advanced_lane_lines.ipynb`](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/advanced_lane_lines.ipynb), which defines the `threshold_pipeline(img)` and runs the sample code.


In order to identify the lane lines I used the following method:
* Find the yellow line using a high low threshold on Hue Saturation and Value for the spectrum of yellow.
* Find the white line using a high low threshold on Hue Saturation and Lightness for the spectrum of white.
* Find additional missing points using applying magnitude and gradient on a grayscale image as well as on the saturation channel
* Activate if either one of the above is activated.
* Use a low Ligtness threshold and deactivating all these points at the end of the previous result.

This gave me a good set of points for the lane lines. The complete comparison of these is provided in the plot below.


![alt text][threshold_comparison]

This is done as the function `threshold_pipeline(img)` defined in ln: 4 of [`advanced_lane_lines.ipynb`](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/advanced_lane_lines.ipynb)

The final binary activation of a test image is obtained as follows:
![alt text][binary_activation1]
The complete list of binary activated images is available [here](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/tree/master/output_images/thresholded_images)
#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a class called `PerspectiveTransform(src,dst)`, which appears in the file [`./perspectivetransform.py`](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/perspectivetransform.py).  The class needs to be instantiated with the following parameters:
* src: Source Coordinates for perspective transform
* dst: Destination Coordinates for perspective transform.
To transform the image two methods are provided:
    1. `transform(img)`: Perspective transforms the image from source points to destination points.
    2. `inverse_transform(img`: Perspective transforms the image back to source points from destination points.

I chose the hardcode the source and destination points in the following manner:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| (230, 693)    | (300, 719)    | 
| (591, 450)    | (300, 0)      |
| (689, 450)    | (980, 0)      |
| (1076, 693)   | (980, 719)    |

I followed this up with a Region of Interest mask that cut out most of unnecessary information such as the bushes and the sky.

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image. The following image shows in green the perspective `src` coordinates,
in purple the `Region of Interest mask` coordinates, and in the second perspective transformed image in blue the `dst` coordinates.
The plot also shows the histogram applied on the image.

![alt text][perspective_roi_histogram]

The complete list of Perspective transformed images is available [here](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/tree/master/output_images/perspective_images)

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did applied the sliding window  with histogram mean approach to plot a second degree polynomial on to the detected lane lines. This code is distributed in the following files:
* ln: 79 of [`advanced_lane_lines.ipynb`](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/advanced_lane_lines.ipynb) contains a sample run of the code to fit lines.
* [`curve.py`](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/curve.py) contains a class `Curve()` that keeps track of information regarding the 2nd order curve such as the coefficients of current fit, all the detected x and y indices for the current frame. the conversion rate of pixel to meters, radius of curvature etc. This class also provides the following methods:
    1. `get_fit(ploty)`: returns the list of x co-ordinates corresponding a given set of y coordinates with respect to the coefficients of the curve.
    2. `update_radius_of_curvature()`: calculates the radius of curvature.
    3. `set_current_fit(current_fit, allx, ally):` set the current fit coefficents and detected x and y coordinates. This function automatically updates the radius of curvature.
* [`curveutil.py`](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/curveutil.py) This file contains the function `find_base_curve(binary_warped, left_curve, right_curve)` which calculates the coefficients of the left and right curve as well as returns the image with sliding window and good indices marked.

![alt text][curve_image]
The complete list of good indices identified images is available [here](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/tree/master/output_images/curve_images)

To fit the curve fist we take a histogram of y axis on the lower half of the image and identify the peaks on left and right as base points for the sliding window search. Then we calclulate all the activated points within the window margin of 100 and height 80 as good indices and take a mean of it to find the base for the next window. This process is continued to get all the indices for the lane line. Then we fit a 2nd order curve on the good indices for left and right each to get their corresponding coefficents. This is saved inside the left and right Curve() instances as well as the list of good x,y indices for each.

A sample plot of the fit curve is shown below:
![alt text][line_plot]
The complete list of plots on test images is available [here](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/tree/master/output_images/line_images)

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

As mentioned in the previous section I have placed the code for finding the radius of curvature as part of `curve.py` in the method `update_radius_of_curvature()`. To find the radius of curvature first i find the max y value among the good indices. I then use the equation to find the radius of curvature as follows:
Rcurve= ((1+ (2Ay+B)^2)^(3/2)) / (2A)
where the coefficients are obtained from the good indice points for each curve.

I calculated the position of the vehicle in ln[75] in [`advanced_lane_lines.ipynb`](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/advanced_lane_lines.ipynb).

To find the position of the vehicle:
* I first assumed that the car is at the centre of the image. So the car position was equal to `img.shape[1] / 2`
* Then I calculated the lane centre by finding the bottom x values for the lane at y =720 for left and right each, then taking the average of left and right ((lx+rx)/2).
* Then the distance of the car from the centre could be calculated as (lane centre - car centre) * x_meter_per_pixel_conversion_rate.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step ln[80] in [`advanced_lane_lines.ipynb`](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/advanced_lane_lines.ipynb).
 calling the function `process_image()`, that takes an image as input and returns the final output image after all processing.  Here is an example of my result on a test image:

![alt text][output]

The complete list of final outputs on test images is available [here](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/tree/master/output_images/final_output)

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).



Here's a [link to my video result](https://github.com/dranzerashi/CarND-Advanced-Lane-Lines/blob/master/res_vid.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

When there are extreme variations in shadows and light areas as seen in the hardest challenge video the thresholding is not enough to filter out only the lane lines. 

The sliding window approach I have used does not take care of these scenarios where I fail to find a lane in the bottom half of the perspective transformed image. This can cause a crash. I can negate this by adding a try catch over the polyfit function and handle the exception by setting the curve detected to false so that I fall back to the average best fit of previous n values.

I can also reduce the amount by which the lanes can curve by taking an average of last n iterations to smoothen out the curve so that in such scenarios the car does not take a large turn.
