import numpy as np
import cv2
import glob
import sys
from scipy.linalg import hadamard
from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration
from stereovision.point_cloud import PointCloud

indir = 'output'
calibration = StereoCalibration(input_folder=indir)

print('get camera projection matrix')
R1 = np.zeros(shape=(3,3))
R2 = np.zeros(shape=(3,3))
P1 = np.zeros(shape=(3,4))
P2 = np.zeros(shape=(3,4))
Q = np.zeros(shape=(4,4))

mtx1 = calibration.cam_mats['left']
mtx2 = calibration.cam_mats['right']
dst1 = calibration.dist_coefs['left']
dst2 = calibration.dist_coefs['right']
R = calibration.rot_mat
T = calibration.trans_vec
imageSize = (640,480)
height = 480
width = 640

cv2.stereoRectify(mtx1, dst1, mtx2, dst2, imageSize, R, T, R1, R2, P1, P2, Q)

workingFolder   = "test/walsh/wood_dark/"
dist = '100'
imageType       = 'jpg'

filename_L    = workingFolder + dist + "/L/*." + imageType
images_L      = glob.glob(filename_L)
filename_R    = workingFolder + dist + "/R/*." + imageType
images_R      = glob.glob(filename_R)

images_L.sort()
images_R.sort()

n = len(images_L)
rectified_left = np.zeros(shape=(n, height, width))
rectified_right = np.zeros(shape=(n, height, width))

for i in range(n):
	fnameL = images_L[i]
	fnameR = images_R[i]
   
	imgL = cv2.imread(fnameL, 0)
	imgR = cv2.imread(fnameR, 0)
	
	# rectify image pair
	rectified_pair = calibration.rectify((imgL, imgR))
	rectified_left[i,:,:] = rectified_pair[0]
	rectified_right[i,:,:] = rectified_pair[1]

""" Inner Product Codes """
codes = hadamard(n+1)[1:,1:]

codes_left = np.zeros(shape=(height, width), dtype='uint8')
codes_right = np.zeros(shape=(height, width), dtype='uint8')
for i in range(height):
    for j in range(width):
        weights_left = np.dot(codes, rectified_left[:,i,j])
        weights_right = np.dot(codes, rectified_right[:,i,j])
        
        codes_left[i,j] = np.argmax(weights_left)
        codes_right[i,j] = np.argmax(weights_right)

# compute disparity
disparity = np.zeros(shape=(height,width), dtype='int16')
mind = 30
maxd = 100
win = 10

for i in range(height):
	code_r = -1
	for j in range(width):
		j_win = min(j+win, width-1)
		
		loc_r = np.where(codes_right[i,j:j_win] == code_r)[0]
		if len(loc_r) != 0:
			disparity[i,j] = disparity[i,j-1]
			continue
		
		code_r = codes_right[i,j]
		
		jmax = min(j+maxd, width-1)
		loc_l = np.where(codes_left[i, j+mind:jmax] == code_r)[0]
		if len(loc_l) != 0:
			disparity[i,j] = loc_l[0] + mind
		else:
			disparity[i,j] = disparity[i,j-1]

# project to 3D
points = cv2.reprojectImageTo3D(disparity, Q)

imgL_color = cv2.imread(workingFolder + dist + '/left.jpg', 1)
imgR_color = cv2.imread(workingFolder + dist + '/right.jpg', 1)
color_pair = calibration.rectify((imgL_color, imgR_color))
c = cv2.flip(cv2.flip(color_pair[0], 1),0)
colors = cv2.cvtColor(c, cv2.COLOR_BGR2RGB)

cloud = PointCloud(points, colors)
cloud = cloud.filter_infinity()

# export and save
cloud.write_ply(workingFolder + 'results/clouds/cloud_' + dist + '.PLY')
np.save(workingFolder + 'results/images/codes_L_' + dist + '.npy', codes_left)
np.save(workingFolder + 'results/images/codes_R_' + dist + '.npy', codes_right)

np.save(workingFolder + 'results/maps/depth_' + dist + '.npy', points[:,:,2])
np.save(workingFolder  + 'results/maps/disparity_' + dist + '.npy', disparity)

np.save(workingFolder + 'results/images/image_L_' + dist + '.npy', rectified_pair[0])
np.save(workingFolder  + 'results/images/image_R_' + dist + '.npy', rectified_pair[1])	
