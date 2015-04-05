#!/usr/bin/python

import cv2
import numpy as np

# # read an image---------------
# img = cv2.imread("/home/jason/projects/python/test.png")
# cv2.imshow("Image", img)
# key = cv2.waitKey(0) & 0xFF
# # press ESC to close window
# if key == 27:
# 	cv2.destroyAllWindows()
# # wait for 's' key to save and exit
# elif key == ord('s'):
# 	# write an image
# 	cv2.imwrite('testcopy.png', img)
# 	cv2.destroyAllWindows()


# video-------------------------
# cap = cv2.VideoCapture(0)

# while (True):
# 	# Capture frame-by-frame
# 	ret, frame = cap.read()
# 	# Our operations on the frame come here
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	# Display the resulting frame
# 	cv2.imshow('frame', gray)
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		break

# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()



# drawing--------------------
# Create a black image
# img = np.zeros((512,512,3), np.uint8)
# # Draw a diagonal blue line with thickness of 5 px
# cv2.line(img,(0,0),(511,511),(255,0,0),5)
# cv2.rectangle(img,(384,0),(500,128),(0,255,0),3)
# cv2.circle(img,(447,63), 63, (0,0,255), -1)
# cv2.ellipse(img,(256,256),(100,50),0,0,180,255,-1)
# # ploygon
# pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
# pts = pts.reshape((-1,1,2))
# cv2.polylines(img,[pts],True,(0,255,255))
# # text
# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(img,'Hello World',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)

# cv2.imshow("Image", img)
# key = cv2.waitKey(0) & 0xFF
# if key == 27:
# 	cv2.destroyAllWindows()



# Mouse as a Paint-Brush-------------------------
# [i for i in dir(cv2) if 'EVENT' in i]
# ['EVENT_FLAG_ALTKEY', 'EVENT_FLAG_CTRLKEY', 'EVENT_FLAG_LBUTTON', 
# 'EVENT_FLAG_MBUTTON', 'EVENT_FLAG_RBUTTON', 'EVENT_FLAG_SHIFTKEY', 
# 'EVENT_LBUTTONDBLCLK', 'EVENT_LBUTTONDOWN', 'EVENT_LBUTTONUP', 
# 'EVENT_MBUTTONDBLCLK', 'EVENT_MBUTTONDOWN', 'EVENT_MBUTTONUP', 
# 'EVENT_MOUSEHWHEEL', 'EVENT_MOUSEMOVE', 'EVENT_MOUSEWHEEL', 
# 'EVENT_RBUTTONDBLCLK', 'EVENT_RBUTTONDOWN', 'EVENT_RBUTTONUP']

# drawing = False # true if mouse is pressed
# mode = True # if True, draw rectangle. Press 'm' to toggle to curve
# ix,iy = -1,-1

# def draw_circle(event,x,y,flags,param):
# 	global ix,iy,drawing,mode

# 	if event == cv2.EVENT_LBUTTONDOWN:
# 		drawing = True
# 		ix,iy = x,y
# 	elif event == cv2.EVENT_MOUSEMOVE:
# 		if drawing == True:
# 			if mode == True:
# 				cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
# 			else:
# 				cv2.circle(img,(x,y),5,(0,0,255),-1)
# 	elif event == cv2.EVENT_LBUTTONUP:
# 		drawing = False
# 		if mode == True:
# 			cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
# 		else:
# 			cv2.circle(img,(x,y),5,(0,0,255),-1)


# # Create a black image, a window and bind the function to window
# img = np.zeros((512,512,3), np.uint8)
# cv2.namedWindow('image')
# cv2.setMouseCallback('image',draw_circle)

# while(1):
# 	cv2.imshow('image',img)
# 	k = cv2.waitKey(1) & 0xFF
# 	if k == ord('m'):
# 		mode = not mode
# 	elif k == 27:
# 		break
# cv2.destroyAllWindows()




#Trackbar as the Color Palette-----------
def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
	cv2.imshow('image',img)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

	# get current positions of four trackbars
	r = cv2.getTrackbarPos('R','image')
	g = cv2.getTrackbarPos('G','image')
	b = cv2.getTrackbarPos('B','image')
	s = cv2.getTrackbarPos(switch,'image')

	if s == 0:
		img[:] = 0
	else:
		img[:] = [b,g,r]

cv2.destroyAllWindows()