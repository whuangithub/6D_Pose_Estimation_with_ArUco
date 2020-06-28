
import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import sys

if len(sys.argv) < 2:
    print("Usage: ./PoseEsimation <image_path> ... <image_path>")
    print("There are images for testing in test_images folder")
    sys.exit()

image_paths_test = sys.argv[1:]

####---------------------- CALIBRATION ---------------------------
#### Calibrate the camera with images in calibration_images folder

# max_iteration = 100
# epsilon = 0.0001
# because we want more accuracy
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)

# size of the chessboard (number of the inner conrners) and the board length of a single square
chessboard_size = [8,5,0.03]
# size of the marker, to get the tvec
marker_size = 0.125

# provide the coordinate of the corner in 3d space
object_points = np.zeros((chessboard_size[0]*chessboard_size[1],3), np.float32)
object_points[:,:2] = np.mgrid[0:chessboard_size[0],0:chessboard_size[1]].T.reshape(-1,2)*chessboard_size[2]

# arrays to store object points and image points from all the images.
points_3d = [] # 3d point in real world space
points_2d = [] # 2d points in image plane.

# iterating through all calibration imagesin the folder
image_paths = glob.glob('calibration_images/*.jpg')
if len(image_paths)==0:
    print("Cannot find calibration files.")
    print("Please make sure 'calibration_images' folder is in the same directory.")
    sys.exit()

for fname in image_paths:

    image = cv2.imread(fname)
    # convert into gray image
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # look for corners
    is_pattern_found, corners = cv2.findChessboardCorners(image_gray, (chessboard_size[0],chessboard_size[1]),None)

    if is_pattern_found == True:
        # add 3d coordinate
        points_3d.append(object_points)

        # Refine the corners of the detected corners
        # cv2.cornerSubPix(image,corners_initial,search_window_size,zero_zone,criteria)
        corners2 = cv2.cornerSubPix(image_gray,corners,(11,11),(-1,-1),criteria)
        points_2d.append(corners2)


        # draw and show the corners
        #image = cv2.drawChessboardCorners(image, (chessboard_size[0],chessboard_size[1]), corners2,is_pattern_found)
        # cv2.imshow('fname',image)
        # cv2.waitKey(0)
    else:
        print("Cannot find a chessboard in calibration.")

# calibrate the camera
_, camera_matrix, distortion, rvecs, tvecs = cv2.calibrateCamera(points_3d, points_2d, image_gray.shape[::-1],None,None)
# print(camera_matrix)
# print(tvecs)
# print(retval)
# sys.exit()

####--------------------------------Pose Estimation---------------------------------------------------
# paths to the images (test all the images)
# image_paths_test = glob.glob('test_images/*.jpg')

for fname in image_paths_test:
    image = cv2.imread(fname)
    if image is None:
        print("Cannot find image "+fname)
        print("Press any button to continue")
        cv2.waitKey(0)
        continue
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # Size: 6X6
    # depends on which dictionary the marker belongs to
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

    # parameters for the detector
    parameters = aruco.DetectorParameters_create()

    #detect the marker
    corners, ids, _ = aruco.detectMarkers(image_gray, aruco_dict, parameters=parameters)

    # font of text
    font = cv2.FONT_HERSHEY_SIMPLEX

    if np.all(ids != None):
        # aruco.estimatePoseSingleMarkers(corners,markerLength camera_matrix,distCoeffs)
        rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, distortion)

        # print result for each image
        print('for image',fname)
        print("rvec is", rvec[0])
        print("tvec is", tvec[0]) # because there will be only one marker in the image (task)

        # draw axis
        aruco.drawAxis(image, camera_matrix, distortion, rvec[0], tvec[0], 0.05)
        # draw a square around the markers
        aruco.drawDetectedMarkers(image, corners)

    else:
        print("The marker is not found in the image.",fname)

    # display the resulting image
    cv2.imshow('Result',image)
    cv2.waitKey(0)

# Reference
# https://docs.opencv.org/master/d9/d6d/tutorial_table_of_content_aruco.html
