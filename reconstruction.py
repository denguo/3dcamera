import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from matplotlib.widgets import RectangleSelector
from mpl_toolkits.mplot3d import Axes3D

%matplotlib inline

""" Load Images """
filename = 'images/walsh_mod'
nimgs = 8
nchannels = 3
height = 720
width = 1080
b_offset = 155 # should be zero when cameras aligned properly

dj = height
dk = width

def show(img):
    plt.figure()
#     plt.title(title)
    plt.imshow(img, cmap='gray')
    plt.colorbar(shrink=0.8)
    plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    plt.show()
    
def show2(img1, img2, title1, title2):
    plt.subplot(1,2,1)
    plt.title(title1)
    plt.imshow(img1, cmap='gray')
    plt.colorbar(shrink=0.8)
    plt.subplot(1,2,2)
    plt.title(title2)
    plt.imshow(img2, cmap='gray')
    plt.colorbar(shrink=0.8)
    plt.show()

def rgbToGray(M):
    return np.dot(M, [0.299, 0.587, 0.114])

def H(a,x):
    b = a.astype(float)/255
    return b[jmin-x:jmax-x,kmin:kmax]

A_imgs = np.zeros(shape=(nimgs,dj,dk,nchannels))
B_imgs = np.zeros(shape=(nimgs,dj,dk,nchannels))

for k in range(nimgs):
    # normalize, rotate 180, crop
    A_imgs[k,:,:,:] = H(mpimg.imread(filename + '/A/' + str(k) + '.jpg'), 0)
    B_imgs[k,:,:,:] = H(mpimg.imread(filename + '/B/' + str(k) + '.jpg'), b_offset)
    show2(A_imgs[k], B_imgs[k], 'A', 'B')


""" Inner Product Codes """
from scipy.linalg import hadamard
test_n = 8
codes = hadamard(test_n)
print(codes)
print(len(codes))

A = rgbToGray(A_imgs)
B = rgbToGray(B_imgs)

A_codes = np.zeros(shape=(dj,dk), dtype='uint8')
B_codes = np.zeros(shape=(dj,dk), dtype='uint8')
for i in range(dj):
    for j in range(dk):
        A_weights = np.dot(codes, A[:test_n,i,j])
        B_weights = np.dot(codes, B[:test_n,i,j])
        
        A_codes[i,j] = np.argmax(A_weights[1:])
        B_codes[i,j] = np.argmax(B_weights[1:])

show(A_codes)
show(B_codes)


""" Disparity """
from depth import compute_disparity
mind = 30
maxd = 100
win = 10

disparity = compute_disparity(mind, maxd, win, A_codes, B_codes)
show(disparity)

""" Depth """
from depth import visualize_depthmap

dpi = 300
mmToInches = 25.4
focal_length = .34
baseline = 150
depth = focal_length * baseline / (disparity*mmToInches/dpi)
show(depth)

print('number of images = ', test_n-1)
visualize_depthmap(dj,dk,depth,2)
