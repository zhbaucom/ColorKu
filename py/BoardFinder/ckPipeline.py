from matplotlib import pyplot as plt
import numpy as np
import cv2
from tkinter import Tk    # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

coverSize = 3

### FUNCTIONS for finding board

def order_points(pts):
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    (tl, tr, br, bl) = pts
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def intersection(line1, line2):
    """Finds the intersection of two lines given in Hesse normal form.
    Returns closest integer pixel locations.
    See https://stackoverflow.com/a/383527/5087436
    """
    rho1, theta1 = line1
    rho2, theta2 = line2
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return [[x0, y0]]

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

def draw_lines(image, lines):
    for line in lines:
        rho, theta = line
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(image, (x1, y1), (x2, y2), (0,0,255), 2)


###Read and resize data

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# filename = askopenfilename()


img1 = cv2.imread(filename)

print('Original Dimensions : ',img1.shape)

scale_percent = 10 # percent of original size
width = int(img1.shape[1] * scale_percent / 100)
height = int(img1.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)

imgKeep = resized

### Calculate contours and keep the largest one
img = imgKeep.copy()
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 150, 255, 0)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


carea = [cv2.contourArea(x) for x in contours]
max_value = max(carea)
maxi = carea.index(max_value)

c1 = contours[maxi]
c = c1

im = cv2.drawContours(img, contours, maxi, (0, 230, 255), 2)
#cv2.imshow("contours",im)


### Create an optimal box around board

image = imgKeep.copy()
orig = image.copy()
draw = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (45, 45)) # Increased kernel size
gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, sqKernel)
ret, thresh = cv2.threshold(imgray, 150, 255, 0)

# Find the right most point of the content by finding contours.
# This is required as the content doesn't have extreme right edge line
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Short
cnts = c1

origH, origW = gray.shape[:2]
xMIN = origW
yMIN = origH
xwMAX = 0
yhMAX = 0

for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    if x > 5 and y > 5 and x + w < origW - 5 and y + h < origH - 5:
        if xMIN > x: xMIN = x
        if yMIN > y: yMIN = y
        if xwMAX < x + w: xwMAX = x + w
        if yhMAX < y + h: yhMAX = y + h

# Edge detection and houghlines transform for finding edge lines
edges = cv2.Canny(thresh, 50, 200)

lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

# Filter out irrelevant lines from houghlines transform
strong_lines = np.zeros([12, 1, 2]) # Increased number of considered strong_lines
n2 = 0
for n1 in range(0,len(lines)):
    for rho,theta in lines[n1]:
        theta_diff = np.abs(np.abs(theta) - np.abs(strong_lines[0, 0, 1])) * 180 / np.pi
        if theta_diff > 90:
            theta_diff -= 90
        if rho < 0:
           rho*=-1
           theta-=np.pi
        if n1 == 0:
            strong_lines[n2] = rho, theta
            n2 = n2 + 1
        elif n2 < 12 and not np.isclose(theta_diff, 45, atol=15):
            closeness_rho = np.isclose(rho,strong_lines[0:n2,0,0],atol = max(image.shape) / 10) # One-tenth of the image width/height
            closeness_theta = np.isclose(theta,strong_lines[0:n2,0,1],atol = np.pi/36)
            closeness = np.all([closeness_rho,closeness_theta],axis=0)
            if not any(closeness):
                strong_lines[n2] = rho, theta
                n2 = n2 + 1

# Removing the blank strong_lines entries
if n2 < strong_lines.shape[0]:
    strong_lines.resize(n2, 1, 2)

# Grouping the filtered lines in horizontal and vertical categories
vert_ind = np.abs(strong_lines[:, :, 1] - 1.5) > 0.5
vert_lines = strong_lines[vert_ind]
hori_lines = strong_lines[np.logical_not(vert_ind), :]

test = np.argsort(np.abs(vert_lines[:, 0]))
vert_lines = vert_lines[test]

test = np.argsort(np.abs(hori_lines[:, 0]))
hori_lines = hori_lines[test]

# Extra vert_line to cater the right side where no houghlines will be detected
# After checking if the right most line is already there
far_point1 = intersection(vert_lines[0], hori_lines[0])
far_point2 = intersection(vert_lines[-1], hori_lines[-1])
if not np.isclose(far_point1[0][0], xwMAX, atol=10) and not np.isclose(far_point2[0][0], xwMAX, atol=10):
    vert_lines = np.append(vert_lines, [[xwMAX, vert_lines[0][1]]], 0)

# Finding the intersection points of the lines
points = []
num_vert_lines = vert_lines.shape[0]
num_hori_lines = hori_lines.shape[0]
for i in range(num_vert_lines):
    for j in range(num_hori_lines):
        point = intersection(vert_lines[i], hori_lines[j])
        points.append(point)

# Drawing the lines and points
draw_lines(draw, vert_lines)
draw_lines(draw, hori_lines)
[cv2.circle(draw, (p[0][0], p[0][1]), 5, 255, 2) for p in points]

# Finding the four corner points and ordering them
pts = np.asarray(points)
four_vertices = order_points(pts.reshape(pts.shape[0], pts.shape[2]))

# Giving a 5 pixels margin for better readability
four_vertices[0] = four_vertices[0][0] - 5, four_vertices[0][1] - 5
four_vertices[1] = four_vertices[1][0] + 5, four_vertices[1][1] - 5
four_vertices[2] = four_vertices[2][0] + 5, four_vertices[2][1] + 5
four_vertices[3] = four_vertices[3][0] - 5, four_vertices[3][1] + 5

# Perspective transform to get the warped image
warped = four_point_transform(orig, four_vertices)


### show results

#cv2.imshow("squared drawing",draw)

warp2 = cv2.resize(warped, (1000,1000), interpolation = cv2.INTER_AREA)
img = warp2.copy()
### Add points where balls are
#inpt = [78, 120, 165, 210, 252, 296, 340, 383, 426]
inpt = [156, 242, 327, 421, 502, 590, 681, 769, 852]
#inpt = [30, 48, 65, 84, 100, 118, 137, 155, 171]
cv2.imwrite('C:/Users/zachb/Desktop/ck4out.png', warp2)


### OUTPUT EACH cell
coverSize = 38
# COUNT = 0
# for row in inpt:
#     for col in inpt:
#         cv2.imwrite("C:/Users/zachb/Desktop/ballgarb2/test"+str(COUNT)+".png", np.array(img[np.arange(col-coverSize, col+(coverSize + 1)), :, :][:, np.arange(row-coverSize, row+(coverSize + 1)), :]))
#         COUNT = COUNT + 1


#HSV Dictionary
color_dict_HSV = {
    'darkblue' : [
        [104, 177, 7],
        [118, 255, 255]
    ],
    'lightblue' : [
        [88, 66, 0],
        [109, 189, 255]
    ],
    'darkgreen' : [
        [23, 47, 26],
        [94, 241, 121]
    ],
    'lightgreen' : [
        [33, 109, 114],
        [68, 253, 250]
    ],
    'darkpurple' : [
        [102, 69, 31],
        [193, 161, 255]
    ],
    'lightpurple' : [
        [108, 29, 43],
        [172, 108, 255]
    ],
    'red' : [
        [0, 73, 0],
        [10, 255, 215]
    ],
    'orange' : [
        [0, 158, 132],
        [23, 246, 255]
    ],
    'yellow' : [
        [21, 80, 130],
        [43, 208, 255]
    ],
    'blank' : [
        [0, 3, 75],
        [43, 187, 187]
    ]
}

lower_range = np.array([106, 16, 35])
upper_range = np.array([135, 255, 255])

#Convert img to HSV
imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(imghsv, lower_range, upper_range)

cv2.imshow('image', img)
cv2.imshow('mask', mask)


percHolder = np.empty(shape = (9, 9, 9))
for z, ballCol in enumerate(["darkblue", "lightblue", "darkpurple", "lightpurple", "darkgreen", "lightgreen", "orange", "red", "yellow"]):

    colRang = color_dict_HSV[ballCol]
    lower_range = np.array(colRang[0])
    upper_range = np.array(colRang[1])

    mask = cv2.inRange(imghsv, lower_range, upper_range)

    for x, row in enumerate(inpt):
        for y, col in enumerate(inpt):
            cell = np.array(mask[np.arange(row-coverSize, row+(coverSize + 1)), :][:, np.arange(col-coverSize, col+(coverSize + 1))])
            # cv2.imshow(str(x)+","+ str(y), cell)
            percHolder[x, y, z] = cv2.countNonZero(cell)







#
# ppoints = [[col, row] for row in inpt for col in inpt]
#
# imgPoints = warp2.copy()
#
#
# # Radius of circle
# radius = 50
#
# # Blue color in BGR
# color = (255, 0, 0)
#
# # Line thickness of 2 px
# thickness = 1
#
# # Using cv2.circle() method
# # Draw a circle with blue line borders of thickness of 2 px
# for center_coordinates in ppoints:
#     imgPoints = cv2.circle(imgPoints, center_coordinates, radius, color, thickness)
#
# # Displaying the image
# cv2.imshow("Points Included", imgPoints)
#
#
# # Color finder
# class CKid:
#     def __init__ (self, img, row, col, coverSize):
#         self.coverSize = coverSize
#         self.colorz = np.array(["Red", "Or", "Yel", "DGr", "LGr", "DBlu", "LBlu", "DPur", "LPur"])
#         self.ballBGR = ballBGR = [[36, 39, 214],
#             [67, 148, 255],
#             [45, 226, 234],
#             [62, 118, 54],
#             [66, 202, 137],
#             [144, 69, 50],
#             [213, 204, 162],
#             [159, 47, 102],
#             [190, 169, 210]]
#         self.cell = img[np.arange(col-coverSize, col+(coverSize + 1)), :, :][:, np.arange(row-coverSize, row+(coverSize + 1)), :]
#         self.celldm = [np.square(np.array(self.cell - self.ballBGR[i])).sum(axis = 2) for i in np.arange(9)]
#         self.allmins = np.min(self.celldm, axis = 0)
#         self.ismin = self.celldm == self.allmins
#         self.cellcols = [[self.colorz[self.ismin[:,i, j]] for i in np.arange(2 * self.coverSize + 1)] for j in np.arange(2 * self.coverSize + 1)]
#         self.MLcols = np.array(self.cellcols).reshape((2 * self.coverSize + 1,2 * self.coverSize + 1))
#         self.ovmin = np.min(self.allmins)
#         self.wmin = self.allmins == self.ovmin
#         self.ec = self.MLcols[self.wmin]
#
#     def pixelCol(self):
#         return self.MLcols
#
#     def pixelDis(self):
#         return self.allmins
#
#     def predCol(self):
#         return self.ec
#
#
# ballBGR = [[36, 39, 214],
#     [67, 148, 255],
#     [45, 226, 234],
#     [62, 118, 54],
#     [66, 202, 137],
#     [144, 69, 50],
#     [213, 204, 162],
#     [159, 47, 102],
#     [190, 169, 210]]
#
#
#
# coverSize = 38
# img = warp2
# colorz = np.array(["Red", "Or", "Yel", "DGr", "LGr", "DBlu", "LBlu", "DPur", "LPur"])
# ballBGR = np.array([[36, 39, 214],
#     [67, 148, 255],
#     [45, 226, 234],
#     [62, 118, 54],
#     [66, 202, 137],
#     [144, 69, 50],
#     [213, 204, 162],
#     [159, 47, 102],
#     [190, 169, 210]])
#
# cell = np.array(img[np.arange(col-coverSize, col+(coverSize + 1)), :, :][:, np.arange(row-coverSize, row+(coverSize + 1)), :])
# COUNT = 0
# for row in inpt:
#     for col in inpt:
#         cv2.imwrite("C:/Users/zachb/Desktop/ballgarb2/test"+str(COUNT)+".png", np.array(img[np.arange(col-coverSize, col+(coverSize + 1)), :, :][:, np.arange(row-coverSize, row+(coverSize + 1)), :]))
#         COUNT = COUNT + 1
#
#
# Rcell = cell[:,:,2]
# Rball = ballBGR[:,2]
# R128 = np.array([np.array(Rcell + Rball[i])/2 > 128 for i in np.arange(9)])
#
# cellBGRD = np.array([np.square(np.array(cell - ballBGR[i])) for i in np.arange(9)])
#
#
# cv2.imshow("test",cv2.resize(cell, (1000,1000)))
#
# def coefCr(vec):
#     vec = np.array(vec).flatten()
#     if np.sum(vec) == len(vec):
#         return [2,4,3]
#     elif np.sum(vec) == 0:
#         return [3,4,2]
#     else:
#         np.array([[[2,4,3] * r + [3,4,2] * (1-r)] for r in vec]).reshape((2*coverSize + 1, 2*coverSize + 1, 3))
#
# celldm = [np.array(cellBGRD[i]*coefCr(R128[i])).sum(axis = 2) for i in np.arange(9)]
#
#
#
# allmins = np.min(celldm, axis = 0)
# ismin = celldm == allmins
# cellcols = [[colorz[ismin[:,i, j]] for i in np.arange(2 * coverSize + 1)] for j in np.arange(2 * coverSize + 1)]
# MLcols = np.array(cellcols).reshape((2 * coverSize + 1,2 * coverSize + 1))
# ovmin = np.min(allmins)
# wmin = allmins == ovmin
# ec = MLcols[wmin]
#
#
# #CKid(warp2, 30, 30, 3).pixelCol()
# #CKid(warp2, 30, 30, 3).predCol()
# #%run C:/Users/zachb/Desktop/ckPipeline.py
#
# predictedColors = [[CKid(warp2, i, j, 3).predCol() for i in np.arange(9)] for j in np.arange(9)]
#
# np.array(predictedColors).reshape((9,9))
