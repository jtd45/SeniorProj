import numpy as np
import cv2
import sys
import serial
import time
from arduinoSerial import arduinoSerial
from redObjects import Rect
from redObjects import RedObj
	
def diffFilter4(f0,f1):
	b1=cv2.cvtColor(f1,cv2.COLOR_BGR2GRAY)
	hsv0=cv2.cvtColor(f0,cv2.COLOR_BGR2GRAY)
	d=cv2.absdiff(hsv0,b1)
	d=cv2.GaussianBlur(d, (21, 21), 0)
	thresh = cv2.threshold(d, 25, 255, cv2.THRESH_BINARY)[1]
	cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	cv2.drawContours(d,cnts,-1,(0,255,255),10)
	#d = cv2.fastNlMeansDenoisingColored(d,None,10,10,7,21)
	return d,thresh
	
def image_filter(image):
	boundries=[((0,240,220),(5,255,235)),((175,110,250),(180,140,255)),((170,190,120),(180,235,170)),((0,240,110),(0,245,120)),((170,200,240),(175,240,255)),((0,210,170),(5,220,180)),((175,200,90),(180,225,110))]#,((0,90,220),(10,110,235))]
	#image=cv2.resize(image,(832,624))
	#image filtering
	image=cv2.bilateralFilter(image,9,75,75)
	hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	mask=0
	for (lower,upper) in boundries:
		mask=cv2.bitwise_or(cv2.inRange(hsv,lower,upper),mask)
	mask=cv2.dilate(mask,None,iterations=20)
	cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	nmask=cv2.bitwise_not(mask)
	mimg=cv2.bitwise_and(image,image,mask=mask)
	return cnts,image

def findObjects(contours):
	objects=list()
	c=10
	for cnt in contours:
		x,y,w,h=cv2.boundingRect(cnt)
		found=0
		for object in objects:
			if (((x>object.x1-c and x<object.x2+c) or (x+w>object.x1-c and x+w<object.x2+c)) and ((y>object.y1-c and y<object.y2+c) or (y+h>object.y1-c and y+h<object.y2+c)))or(((object.x1>x-c and object.x1<x+w+c) or (object.x2>x-c and object.x2<x+w+c)) and ((object.y1>y-c and object.y1<y+h+c) or (object.y2>y-c and object.y2<y+h+c))):
				#objects.remove(object)
				found=1
				object.merge(Rect(x,y,x+w,y+h))
			if found==1:
				break
		if found==0:
			objects.append(Rect(x,y,x+w,y+h))
	return objects
	
def check_position(center,image):
	x,y=center
	height,width = image.shape[:2]
	cv2.rectangle(image,(int(width/2-140),int(height/2-100)),(int(width/2+130),int(height/2+100)),(0,255,0),2)
	print(width," ",height," ",width/2-140," ",height/2-100," ",x," ",y)
	if x>0 and y>0:
		dir="0"
		back="0"
		if y>height/2+100:
			dir="B"
		elif y<height/2-100:
			dir="3"
		if x>width/2+130:
			dir="F"+dir#move right
			back="70"
		elif x<width/2-140:
			dir="7"+dir#move left
			back="F0"
		return dir,back
	else:
		return "",""

if __name__=='__main__':
	try:
		video=cv2.VideoCapture(0)
		if video.isOpened()==False:
			video.open()
		
		port=arduinoSerial()
		#image=diffFilter(image0,image1,image2)
		print("hi34342")
		images=list()
		i=0
		port.write_Serial("0")
		time.sleep(2)
		_,image=video.read()
		
		newFrameCount=0
		count=0
		frisbee=Rect(-1,-1,-1,-1)
		foundCount=0
		dir=""
		back=""
		time.sleep(3)
		while(video.isOpened()):
			if newFrameCount<7:
				dir=""
				_,oldImage=video.read()
				newFrameCount+=1
			elif newFrameCount<7:
				newFrameCount+=1
			else:
				dir,back=check_position(frisbee.get_center(),image)
			_,image=video.read()
			filt,t=diffFilter4(image,oldImage)
			cv2.imshow("thresh",t)
			cv2.imshow("filtered",filt)
			filtered_img=cv2.bitwise_and(image,image,mask=t)
			cnts,filtered_img=image_filter(filtered_img)
			rects=findObjects(cnts)
			
			area=0
			for rect in rects:
				cv2.rectangle(image,(rect.x1,rect.y1),(rect.x2,rect.y2),(0,255,0),2)
				if rect.get_area()>area:
					frisbee=rect
			if len(rects)==0:
				foundCount+=1
				if foundCount>10:
					frisbee=Rect(-1,-1,-1,-1)
			else:
				foundCount=0
			
			if port.port!=None and dir!="" and newFrameCount>=7 and dir!="0":
				print(dir)
				port.write_Serial(dir)
				newFrameCount=0
			cv2.drawContours(filtered_img,cnts,-1,(0,255,255),10)
			cv2.imshow("title",filtered_img)
			cv2.imshow("image",image)
			k=cv2.waitKey(10)&0xFF
			if k==27:
				print("27")
				break
			if cv2.getWindowProperty("title",0)==-1:
				print("-1")
				break
		print("end?")
		
		cv2.destroyAllWindows()
		video.release()
		port.write_Serial("0")
	except:
		print("can't open")
		raise