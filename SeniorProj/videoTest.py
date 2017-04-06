import numpy as np
import cv2
import imutils

class Rect(object):
	def __init__(self,x,y,x2,y2):
		self.x1=x
		self.x2=x2
		self.y1=y
		self.y2=y2

def colorFilter(image,lower,upper):
	lower=np.array(lower,dtype="uint8")
	upper=np.array(upper,dtype="uint8")
	mask=cv2.inRange(image,lower,upper)
	return cv2.bitwise_and(image,image,mask=mask)


def findObjects(contours):
	objects=list()
	rects=list()
	c=20
	for cnt in contours:
		x,y,w,h=cv2.boundingRect(cnt)
		found=0
		for object in objects:
			if (((x>object.x1-c and x<object.x2+c) or (x+w>object.x1-c and x+w<object.x2+c)) and ((y>object.y1-c and y<object.y2+c) or (y+h>object.y1-c and y+h<object.y2+c)))or(((object.x1>x-c and object.x1<x+w+c) or (object.x2>x-c and object.x2<x+w+c)) and ((object.y1>y-c and object.y1<object.y2+c) or (object.y2>y-c and object.y2<y+h+c))):
				print("overlap")
				#objects.remove(object)
				found=1
				object.x2=max(x+w,object.x2)
				object.y2=max(y+h,object.y2)
				object.x1=min(x,object.x1)
				object.y1=min(y,object.x1)
				rects.append(object)
			if found==1:
				break
		if found==0:
			objects.append(Rect(x,y,x+w,y+h))
	return objects

def diffFilter(f0,f1,f2):
	d1=cv2.absdiff(f2,f1)
	d2=cv2.absdiff(f1,f0)
	return cv2.bitwise_and(d1,d2)

if __name__=='__main__':
	try:
		#boundries=[((0,100,220), (5,120,255)),((150,230,230),(180,245,255)),((165,210,115),(180,225,130)),((0,241,227),(2,254,235)),((175,110,250),(178,137,254))]
		boundries=[((0,240,220),(5,255,235)),((175,110,250),(180,140,255)),((170,190,120),(180,235,170)),((0,240,110),(0,245,120)),((170,200,240),(175,240,255))]
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
			mask=cv2.dilate(mask,None,iterations=10)
			cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
			#print(len(cnts))
			cv2.drawContours(image, cnts, -1, (0,255,0), 1)
			
			nmask=cv2.bitwise_not(mask)
			mimg=cv2.bitwise_and(image,image,mask=mask)
			if len(cnts)>0:
				rects=findObjects(cnts)
				print(len(rects)," ",len(cnts))
				for rect in rects:
					cv2.rectangle(mimg,(rect.x1,rect.y1),(rect.x2,rect.y2),(0,255,0),2)
					center=(int((rect.x1+rect.x2)/2),int((rect.y1+rect.y2)/2))
					cv2.circle(mimg,center,10,(0,255,0),3)
				c=max(cnts,key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				#Identify center of frisbee
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"])-10, int(M["m01"] / M["m00"])+10)
				cv2.circle(image,center,10,(0,255,0),3)
				cv2.putText(mimg,"HI",center,cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0))
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
			
			cv2.imshow("title",mimg)
			k=cv2.waitKey(10)&0xFF
			if k==27:
				break
		cv2.destroyAllWindows()
	except:
		print("can't open")
		raise