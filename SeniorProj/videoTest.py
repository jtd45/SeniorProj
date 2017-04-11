import numpy as np
import cv2
import sys
import serial
from arduinoSerial import arduinoSerial
from redObjects import Rect
from redObjects import RedObj


def findObjects(contours):
	objects=list()
	c=50
	for cnt in contours:
		x,y,w,h=cv2.boundingRect(cnt)
		found=0
		for object in objects:
			if (((x>object.x1-c and x<object.x2+c) or (x+w>object.x1-c and x+w<object.x2+c)) and ((y>object.y1-c and y<object.y2+c) or (y+h>object.y1-c and y+h<object.y2+c)))or(((object.x1>x-c and object.x1<x+w+c) or (object.x2>x-c and object.x2<x+w+c)) and ((object.y1>y-c and object.y1<y+h+c) or (object.y2>y-c and object.y2<y+h+c))):
				objects.remove(object)
				found=1
				object.merge(Rect(x,y,x+w,y+h))
			if found==1:
				break
		if found==0:
			objects.append(Rect(x,y,x+w,y+h))
	return objects

def image_filter(image):
	boundries=[((0,240,220),(5,255,235)),((175,110,250),(180,140,255)),((170,190,120),(180,235,170)),((0,240,110),(0,245,120)),((170,200,240),(175,240,255)),((0,210,170),(5,220,180)),((175,200,90),(180,225,110))]#,((10,15,250),(15,25,255))]
	image=cv2.resize(image,(832,624))
	hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	mask=0
	for (lower,upper) in boundries:
		mask=cv2.bitwise_or(cv2.inRange(hsv,lower,upper),mask)
	mask=cv2.dilate(mask,None,iterations=20)
	cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	nmask=cv2.bitwise_not(mask)
	mimg=cv2.bitwise_and(image,image,mask=mask)
	cv2.drawContours(image, cnts, -1, (0,255,0), 1)
	return cnts,image

def disp_objects(image,robject):
	cv2.rectangle(image,(robject.rect.x1,robject.rect.y1),(robject.rect.x2,robject.rect.y2),(0,255,0),2)
	x,y=robject.rect.get_center()
	center=(x-10,y+10)
	cv2.putText(image,str(robject.id)+" "+str(robject.frisbee),center,cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255))
	cv2.circle(image,(x,y),int(robject.rect.get_width()/2),(0,255,0),3)

def get_frisbee(image,redobjects,rects):
	area=0
	frisbee=RedObj(Rect(-1,-1,-1,-1),-1)
	for robject in redobjects:
		if robject.continuity(rects)==False:
			redobjects.remove(robject)
		if robject.frisbee==True:
			disp_objects(image,robject)
		if robject.rect.get_area()>area:
			area=robject.rect.get_area()
			frisbee=robject
	return frisbee

def sendto_serial(x,y,image):
	dir="0"
	if x>0 and y>0:
		if x>516:
			dir="1"#dir|0x01 #move right
		elif x<316:
			dir="9"#dir|0x09 #move left
		if y>412:
			dir="1"+dir#|0x10 #move right
		elif y<312:
			dir="9"+dir#|0x90 #move left
	if port.port!=None: #and f<20:
		port.write_Serial(dir)
	cv2.putText(image,dir,(0,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255))

if __name__=='__main__':
	try:
		video=cv2.VideoCapture(0)
		if video.isOpened()==False:
			video.open()
		count=0
		redobjects=list()
		port=arduinoSerial()
		
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		out = cv2.VideoWriter('output.avi',fourcc, 20.0, (832,624))
		
		_,image=video.read()
		cv2.imshow("title",image)
		
		f=0
		while(video.isOpened()):
			_,image=video.read()
			cnts,image=image_filter(image)
			area=0
			if len(cnts)>0:
				rects=findObjects(cnts)
				frisbee=get_frisbee(image,redobjects,rects)
				for rect in rects:
					redobjects.append(RedObj(rect,count))
					cv2.rectangle(image,(rect.x1,rect.y1),(rect.x2,rect.y2),(0,255,0),2)
					count+=1
			else:
				frisbee=get_frisbee(image,redobjects,list())

			print(frisbee.age)
			if frisbee.age>3:
				for robject in redobjects:
					robject.frisbee=False
				frisbee.frisbee=True
			x,y=frisbee.rect.get_center()
			sendto_serial(x,y,image)

			k=cv2.waitKey(10)&0xFF
			if k==27:
				break
			if cv2.getWindowProperty("title",0)==-1:
				break
			cv2.imshow("title",image)
			out.write(image)
			
		cv2.destroyAllWindows()
		video.release()
		out.release()
	except:
		print("can't open")
		raise