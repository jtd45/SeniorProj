import numpy as np
import cv2
import imutils

def colorFilter(image,lower,upper):
	lower=np.array(lower,dtype="uint8")
	upper=np.array(upper,dtype="uint8")
	mask=cv2.inRange(image,lower,upper)
	return cv2.bitwise_and(image,image,mask=mask)

def diffFilter(f0,f1,f2):
	d1=cv2.absdiff(f2,f1)
	d2=cv2.absdiff(f1,f0)
	return cv2.bitwise_and(d1,d2)

if __name__=='__main__':
	try:
		boundries=[((0,100,220), (5,120,255)),((150,230,230),(180,245,255)),((165,210,115),(180,225,130))]
		video=cv2.VideoCapture(0)
		if video.isOpened()==False:
			video.open();
		points=[]
		lostCount=0
		while(1):
			_,image=video.read()
			#image = imutils.resize(image, width=1300)
			hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
			mask=0
			for (lower,upper) in boundries:
				mask=cv2.bitwise_or(cv2.inRange(hsv,lower,upper),mask)
			mask=cv2.dilate(mask,None,iterations=1)
			cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
			print(len(cnts))
			cv2.drawContours(image, cnts, -1, (0,255,0), 1)
			
			if len(cnts)>0:
				c=max(cnts,key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				#Identify center of frisbee
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				cv2.circle(image,center,10,(0,255,0),3)
				points.append(center)
			else:
				if len(points)>0:
					cv2.circle(image,points[len(points)-1],10,(0,255,0),3)
				lostCount+=1
				#print("FRISBEE LOST #",lostCount)
			for i in range(1, len(points)):
				# if either of the tracked points are None, ignore
				# them
				if points[i - 1] is None or points[i] is None:
					continue
		 
				# otherwise, compute the thickness of the line and
				# draw the connecting lines
				thickness = 3
				#cv2.line(image, points[i - 1], points[i], (0, 255, 0), thickness)
			cv2.imshow("title",image)
			k=cv2.waitKey(10)&0xFF
			if k==27:
				break
		cv2.destroyAllWindows()
	except:
		print("can't open")
		raise