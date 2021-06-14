import math
import random
class Vector:
	def __init__(self,x = 0, y = 0):
		self.x = x
		self.y = y
	def normalize(self):
		a = self.x
		b = self.y
		if not (a == 0 and b == 0):	
			self.x = a/math.sqrt(a**2 + b**2)
			self.y = b/math.sqrt(a**2 + b**2)
		else:
			pass
			#print("Vector is zero")
	def setMag(self,mag):
		self.normalize()
		self.x *= mag
		self.y *= mag
	def getMag(self):
		return math.sqrt(self.x**2 + self.y**2)
	def setDir(self,angle):
		mag = self.getMag()
		self.x = mag*math.cos(angle)
		self.y = mag*math.sin(angle)
	def getDir(self):
		return math.atan2(self.y , self.x)
	def get(self):
		return [self.x,self.y]
	def __add__(self,vec):
		return Vector(self.x + vec.x, self.y + vec.y)
	def __iadd__(self,vec):
		self.x += vec.x
		self.y += vec.y
		return self
	def __sub__(self,vec):
		return Vector(self.x - vec.x, self.y - vec.y)
	def __isub__(self,vec):
		self.x -= vec.x
		self.y -= vec.y
		return self
	def __mul__(self,mag):
		return Vector(self.x*mag,self.y*mag)
	def __imul__(self,mag):
		self.x *= mag
		self.y *= mag
		return self
	def __truediv__(self,mag):
		return Vector(self.x/mag,self.y/mag)
	# def __eq__(self,vec):
		# self.x = vec.x
		# self.y = vec.y
	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"
	def __repr__(self):
		return str(self)
	def repeTile(self,win_width,win_height):
		if self.x > win_width/2:
			self.x -= win_width
		elif self.x < -win_width/2:
			self.x += win_width
		if self.y > win_height/2:
			self.y -= win_height
		elif self.y < -win_height/2:
			self.y += win_height
	def collideTile(self,vel,win_width,win_height):
		if self.x > win_width/2 or self.x < -win_width/2:
			vel.x = -vel.x
		if self.y > win_height/2 or self.y < -win_height/2:
			vel.y = -vel.y
	def zero(self):
		self.x = 0
		self.y = 0
	def one(self):
		self.x = 1
		self.y = 0
	def dot(self,vec):
		return self.x * vec.x + self.y * vec.y
	def limit(self,mag):
		if self.getMag() > mag:
			self.setMag(mag)
	def vec2tup(self):
		return (self.x, self.y)
	def vec2tupint(self):
		return (int(self.x),int(self.y))

def vectorUnitRandom():
	x = random.randint(-10000,10000)
	y = random.randint(-10000,10000)
	return Vector( x/math.sqrt(x**2+y**2) , y/math.sqrt(x**2+y**2) )
	
def dist(vec1,vec2):
	return math.sqrt( (vec2.x - vec1.x)**2 + (vec2.y - vec1.y)**2 )

def getAngleByTwoVectors(vec_org,vec_taget):
	return math.atan2(vec_taget.y - vec_org.y, vec_taget.x - vec_org.x)
	
def vectorCopy(vec):
	return Vector(vec.x,vec.y)