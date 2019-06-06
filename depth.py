""" computes disparity given a min/max range and two sets of walsh code images """
def compute disparity(mind, maxd, win, A_codes, B_codes):
	disparity = np.zeros(shape=(dj,dk))

	for i in range(dj):
	    b_code = -1
	    for j in range(dk):
	        if j+win > dk-1:
	            j_win = dk-1
	        else:
	            j_win = j+win
	        
	        b_loc = np.where(B_codes[i,j:j_win] == b_code)[0]
	        if len(b_loc) != 0:
	            disparity[i,j] = disparity[i,j-1]
	            continue
	        
	        b_code = B_codes[i,j]
	        
	        if j+maxd > dk-1:
	            jmax = dk-1
	        else:
	            jmax = j+maxd
	        
	        a_loc = np.where(A_codes[i,j+mind:jmax] == b_code)[0]
	        if len(a_loc) != 0:
	            disparity[i,j] = a_loc[0] + mind
	        else:
	            disparity[i,j] = disparity[i,j-1]

	        if disparity[i,j] == 0:
	            disparity[i,j] = mind
    return disparity

# def levels(depth, scale):
#     (row, col) = depth.shape
#     for i in range(row):
#         for j in range(col):
#             if not math.isnan(depth[i,j]) and not math.isinf(depth[i,j]):
#                 depth[i,j] = int(depth[i,j] / scale)
#     return depth

""" plot 3D point cloud of scene """
def visualize_depthmap(height, width, depth, scale):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # depth = levels(depth, scale)
    # depth[depth>16] = np.nan
    
    depth_max = depth.max()
#     print(depth_max)
    for i in range(height):
        x = np.arange(0,width,1)
        y = depth[-i,:]
        z = i*np.ones(shape=(width))
        ax.scatter(x, y, c='b', s=1, zs=z)
    ax.set_xlabel('R axis', color='r')
    ax.set_ylabel('G axis', color='g')
    ax.set_zlabel('B axis', color='b')
    plt.show()
    plt.figure()
    plt.imshow(depth, cmap='gray')
    plt.colorbar(shrink=0.8)
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(height):
        x = np.arange(0,width,1)
        y = depth[-i,:]
        z = i*np.ones(shape=(width))
        ax.scatter(x, z, c='b', s=1, zs=y)
    ax.set_xlabel('R axis', color='r')
    ax.set_ylabel('G axis', color='g')
    ax.set_zlabel('B axis', color='b')
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(height):
        x = np.arange(0,width,1)
        y = depth[-i,:]
        z = i*np.ones(shape=(width))
        ax.scatter(y, z, c='b', s=1, zs=x)
    ax.set_xlabel('R axis', color='r')
    ax.set_ylabel('G axis', color='g')
    ax.set_zlabel('B axis', color='b')
    plt.show()

# depth = np.zeros(shape=(100,100))
# depth[25:75,25:50] = 5
# depth[25:50,50:75] = 3
# visualize_depthmap(100, 100, depth, 1)
