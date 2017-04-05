import numpy as np
import cv2

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
		#boundries=[(
		lower=[100,90,180]
		upper=[160,150,230]
		video=cv2.VideoCapture(0)
		_,temp=video.read()
		f_minus=temp#colorFilter(temp,lower,upper)
		f=temp#colorFilter(temp,lower,upper)
		f_plus=temp#colorFilter(temp,lower,upper)
		while(1):
			filteredImage=diffFilter(f_minus,f,f_plus)
			cv2.imshow("DiffVid",filteredImage)
			k=cv2.waitKey(10)&0xFF
			if k==27:
				break
			f_minus=f
			f=f_plus
			_,temp=video.read()
			f_plus=temp#colorFilter(temp,lower,upper)
		cv2.destroyAllWindows()
	except:
		print("can't open")
		raise