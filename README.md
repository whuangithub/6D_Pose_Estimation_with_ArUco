# Usage

The image for testing is saved in the `ComputerVision/test_images` folder.

To get the 6DoF pose of a marker in an image, in a terminal of a Linux system, get to the `ComputerVision` directory, and input

```
./PoseEstimation.py <image_path>
```

the result of the `rvec` and `tvec` will show in the terminal window and one image with the axis will show as well. It's also possible to add more paths to images, like

```
./PoseEstimation.py <image_path1> <image_path2> <image_path3> ...
```

The `rvec`, `tvec`, and images with axis will show separately.

For example, please try

```
./PoseEstimation.py test_images/test_image02.jpg test_images/test_image03.jpg
```

**Press any key to show the result for the next image or end the program.**

# About the program

## Marker

I use No.10 aruco marker in the 4X4_50 dictionary. It's saved in the `No10Aruco_4X4_50.pdf`. The size of it is 12.5cm so that the `mark_size` is set to 0.125 in the code.<br>
You can print it out and reset the `marker_size`.<br>
****Please note that the size of the marker is the width and height without the black border.****<br>
The reason for me to use this marker is because there is a robust and accurate algorithm for the aruco markers. It's found to be the best one after comparing several types of markers and algorithms.

## Camera calibration

The calibration is the first part of the code.<br>
I calibrate my webcam with chessboard images, which are in the `calibration_images` folder.

**The images are necessary for the program, please make sure the `calibration_images` folder is included in `ComputerVision` folder.**

## Pose Estimation

The program uses the functions from OpenCv to calculate the 6DoF pose.
