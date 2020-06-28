The image for testing is saved in the `test_images` folder.  

** Run in Linux **  

```
./PoseEstimation.py <image_path>
```

It's also possible to add more paths to images, like

```
./PoseEstimation.py <image_path1> <image_path2> <image_path3> ...
```

Press any key to show the result for the next image or end the program.

## Marker

No.10 aruco marker in the 4X4_50 dictionary.  `No10Aruco_4X4_50.pdf` The size of it is 12.5cm so that the `mark_size` is set to 0.125 in the code.<br>
You can print it out and reset the `marker_size`.<br>

## Camera calibration

Calibrating with chessboard images, in the `calibration_images` folder.

The program uses the functions from OpenCV to calculate the 6DoF pose.
