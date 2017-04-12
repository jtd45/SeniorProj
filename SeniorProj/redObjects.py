class Rect(object):
	def __init__(self,x,y,x2,y2):
		self.x1=x
		self.x2=x2
		self.y1=y
		self.y2=y2
	def get_center(self):
		return int((self.x1+self.x2)/2),int((self.y1+self.y2)/2)
	def get_area(self):
		return abs(self.x1-self.x2)*abs(self.y1-self.y2)
	def get_width(self):
		return abs(self.x1-self.x2)
	def get_height(self):
		return abs(self.y1-self.y2)
	def merge(self,rect):
		self.x2=max(rect.x2,self.x2)
		self.y2=max(rect.y2,self.y2)
		self.x1=min(rect.x1,self.x1)
		self.y1=min(rect.y1,self.y1)
	def move(self,down,right):
		self.x2=self.x2+right
		self.x1=self.x1+right
		self.y1=self.y1+down
		self.y2=self.y2+down
	def grow(self,x,y):
		self.x2=self.x2+int(x/2)
		self.y2=self.y2+int(y/2)
		self.x1=self.x1-int(x/2)
		self.y1=self.y1-int(y/2)

class RedObj(object):
	def __init__(self,rect,id):
		self.rect=rect
		self.last=rect
		self.id=id
		self.frisbee=0
		self.motion=0
		self.track=list()
		self.trackAve=[0,0]
		self.lostCount=0
		self.found=False
		self.age=0
	def find_motion(self,ocenter,ncenter):
		ox,oy=ocenter
		nx,ny=ncenter
		trackBloc=[ox-nx,oy-ny]
		self.track.append(trackBloc)
		self.trackAve[0]=(self.trackAve[0]+ox-nx)/2
		self.trackAve[1]=(self.trackAve[1]+oy-ny)/2
		if len(self.track)>5:
			vars=list()
			dist=[0,0]
			for trc in self.track:
				vars.append([(trc[0]-self.trackAve[0])**2,(trc[1]-self.trackAve[1])**2])
				dist[0]=dist[0]+trc[0]
				dist[1]=dist[1]+trc[1]
			std=[0,0]
			for var in vars:
				std[0]=(std[0]+var[0])/2
				std[1]=(std[1]+var[1])/2
			print("std=",std," ave=",dist)
			if (abs(dist[0])>15 or abs(dist[1])>15) and (std[0]<30 and std[1]<30):
				print("there was motion detected for object ",self.id)
				self.motion=self.age
				self.trackAve=[0,0]
				self.track=list()
				return
	def continuity(self,rects): #find if object is still being detected by the camera
		ox,oy=self.rect.get_center()
		oarea=self.rect.get_area()
		self.increment_age()
		for rect in rects:
			if self.overlap(rect,40,40):
				x,y=rect.get_center()
				self.rect.move(y-oy,x-ox)
				self.last.merge(rect)
				self.rect=self.last
				self.last=rect
				rects.remove(rect)
				self.lostCount=0
				self.found=True
				self.find_motion((ox,oy),self.rect.get_center())
				return True
		self.lostCount+=1
		if self.frisbee==1:
			self.rect.grow(5,5)
		if self.lostCount>10:
			self.found=False
			return False
		else:
			return True
	def increment_age(self):
		self.age+=1
	def overlap(self,rect,cx,cy):
		x=rect.x1
		x2=rect.x2
		y=rect.y1
		y2=rect.y2
		if (((x>self.rect.x1-cx and x<self.rect.x2+cx) or (x2>self.rect.x1-cx and x2<self.rect.x2+cx)) and ((y>self.rect.y1-cy and y<self.rect.y2+cy) or (y2>self.rect.y1-cy and y2<self.rect.y2+cy)))or(((self.rect.x1>x-cx and self.rect.x1<x2+cx) or (self.rect.x2>x-cx and self.rect.x2<x2+cx)) and ((self.rect.y1>y-cy and self.rect.y1<y2+cy) or (self.rect.y2>y-cy and self.rect.y2<y2+cy))):
			return True
		else:
			return False