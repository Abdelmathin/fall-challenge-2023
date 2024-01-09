import sys
import math
import builtins

def get_next_line():
	line = input()
	# print ("LINE:" + str(line), file = sys.stderr)
	return (line)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def inRange(p1, p2, r):
	return (p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]) <= r * r

def absoluteValue(x):
	if (x < 0):
		return (-x)
	return (x)

def squareRoot(x):
	return math.sqrt(x)

def distanceBetweenTwoPoints(startX, startY, endX, endY):
	d2 = (endX - startX) * (endX - startX) + (endY - startY) * (endY - startY)
	return (squareRoot(d2))



def playerCollidesWithEnemy(playerStartX, playerStartY, playerEndX, playerEndY, enemyStartX, enemyStartY, enemyEndX, enemyEndY, dangerZoneRadius):
	playerSpeed2 = (playerEndX - playerStartX) * (playerEndX - playerStartX) + (playerEndY - playerStartY) * (playerEndY - playerStartY)
	enemySpeed2  = (enemyEndX - enemyStartX) * (enemyEndX - enemyStartX) + (enemyEndY - enemyStartY) * (enemyEndY - enemyStartY)

	if (enemyStartY < 2000):
		return (False)
	d = distanceBetweenTwoPoints(playerStartX, playerStartY, playerEndX, playerEndY)
	if (d <= dangerZoneRadius):
		return (True)
	if (enemySpeed2 < 1 and playerSpeed2 < 1):
		return (False)
	x  = enemyStartX
	y  = enemyStartY
	ux = playerStartX
	uy = playerStartY

	x2  = x - ux
	y2  = y - uy
	r2  = dangerZoneRadius
	vx2 = (enemyEndX - enemyStartX) - (playerEndX - playerStartX)
	vy2 = (enemyEndY - enemyStartY) - (playerEndY - playerStartY)

	a = vx2 * vx2 + vy2 * vy2

	if (a <= 0.0):
		return (False)

	b     = 2.0 * (x2 * vx2 + y2 * vy2)
	c     = x2 * x2 + y2 * y2 - r2 * r2
	delta = b * b - 4.0 * a * c

	if (delta < 0.0):
		return (False)

	t = (-b - math.sqrt(delta)) / (2.0 * a)

	if (t <= 0.0):
		return (False)

	if (t > 1.0):
		return (False)

	return (True)


# def isDangerousPath(enemyStartX, enemyStartY, enemyEndX, enemyEndY, playerStartX, playerStartY, playerEndX, playerEndY, dangerZoneRadius):
# 	if (distanceBetweenTwoPoints(enemyStartX, enemyStartY, playerStartX, playerStartY) <= dangerZoneRadius):
# 		return (True)
# 	if (distanceBetweenTwoPoints(enemyEndX, enemyEndY, playerEndX, playerEndY) <= dangerZoneRadius):
# 		return (True)
# 	if (((enemyEndX - enemyStartX) * (enemyEndX - enemyStartX) + (enemyEndY - enemyStartY) * (enemyEndY - enemyStartY)) < 1):
# 		if (((playerEndX - playerStartX) * (playerEndX - playerStartX) + (playerEndY - playerStartY) * (playerEndY - playerStartY)) < 1):
# 			return (False)
# 	x2  = enemyStartX - playerStartX;
# 	y2  = enemyStartY - playerStartY;
# 	vx2 = enemyEndX - playerEndX - x2;
# 	vy2 = enemyEndY - playerEndY - y2;
# 	a   = vx2 * vx2 + vy2 * vy2;
# 	if (a <= 0.0):
# 		return (False)
# 	b     = 2.0 * (x2 * vx2 + y2 * vy2);
# 	c     = x2 * x2 + y2 * y2 - dangerZoneRadius * dangerZoneRadius;
# 	delta = b * b - 4.0 * a * c;
# 	if (delta < 0.0):
# 		return (False)
# 	t = (-b - squareRoot(delta)) / (2.0 * a);
# 	if (t <= 0.0):
# 		return (False)
# 	if (t > 1.0):
# 		return (False)
# 	return (True)


def isIntersected(self, start, end, center, radius):
	a = (end.getY() - start.getY()) * 1.0 / ((end.getX() - start.getX()) + 0.000000001)
	b = end.getY() - a * end.getX()
	alpha = b - center.getX()
	beta = radius * radius - center.getX() * center.getX() - alpha * alpha
	delta4 = (center.getX() - a * alpha) ** 2 + (1 + a * a) * beta
	return (delta4 >= 0)

def isDangerousPath(enemyStartX, enemyStartY, enemyEndX, enemyEndY, playerStartX, playerStartY, playerEndX, playerEndY, dangerZoneRadius):
	enemySpeedX  = (enemyEndX  - enemyStartX )
	enemySpeedY  = (enemyEndY  - enemyStartY )
	playerSpeedX = (playerEndX - playerStartX)
	playerSpeedY = (playerEndY - playerStartY)
	enemyFactor  = 0.0
	df           = 0.1
	iterations   = 0
	while (enemyFactor <= 1.0):
		enemyX = enemyStartX + enemyFactor * enemySpeedX
		enemyY = enemyStartY + enemyFactor * enemySpeedY
		playerFactor  = 0.0
		while (playerFactor <= 1.0):
			playerX = playerStartX + playerFactor * playerSpeedX
			playerY = playerStartY + playerFactor * playerSpeedY
			iterations = iterations + 1
			if (distanceBetweenTwoPoints(playerX, playerY, enemyX, enemyY) <= dangerZoneRadius):
				return (True)
			playerFactor += df
		enemyFactor += df
	return (False)

class Collision:
	def __init__(self, t, a = None, b = None):
		self.t = t
		self.a = a
		self.b = b

	def happened(self):
		return self.t >= 0

NONE_COLLISION = Collision(-1)

class Closest:
	def __init__(self, _list, _distance):
		self.list      = _list
		self.distance  = _distance

	def hasOne(self):
		return (len(self.getList()) == 1)

	def getPos(self):
		if not self.hasOne():
			return (None)
		return (self.getList()[0].getPos())

	def getDistance(self):
		return (self.distance)

	def getList(self):
		return (self.list)

	def getMeanPos(self):
		if (self.hasOne()):
			return self.getPos()
		x = 0
		y = 0
		for entity in self.getList():
			x += entity.getPos().getX()
			y += entity.getPos().getY()
		return Vector(x / len(self.getList()), y / len(self.getList()))

class Vector:

	def __str__(self):
		return ('<vector x="{}" y="{}">'.format(self.getX(), self.getY()))

	def __repr__(self):
		return (str(self))

	def __init__(self, a, b = None):
		if (type(a) in [type(self)]):
			self.setX(b.getX() - a.getX())
			self.setY(b.getY() - a.getY())
		elif (b != None):
			self.setX(a)
			self.setY(b)			
		else:
			raise

	def vsymmetric(self, center = None):
		if (center == None):
			return Vector(self.getX(), -self.getY())
		return Vector(self.getX(), 2 * center - self.getY())



	def hsymmetric(self, center = None):
		if (center == None):
			return Vector(-self.getX(), self.getY())
		return Vector(2 * center - self.getX(), self.getY())

	def add(self, a, b = None):
		if b != None:
			raise
		return Vector(self.getX() + a.getX(), self.getY() + a.getY())

	def getX(self):
		return (self._x)
	def getY(self):
		return (self._y)
	def setX(self, _x):
		self._x = _x
	def setY(self, _y):
		self._y = _y

	def length(self):
		return math.sqrt(self.getX() * self.getX() + self.getY() * self.getY())

	def normalize(self):
		length = self.length()
		if (length == 0):
			return (Vector(0, 0))
		return Vector(self.getX() / length, self.getY() / length)

	def mult(self, factor):
		return Vector(self.getX() * factor, self.getY() * factor)

	def round(self):
		return Vector(int(builtins.round(self.getX())), int(builtins.round(self.getY())))

	def isZero(self):
		return (self.getX() == 0) and (self.getY() == 0)

	def inRange(self, v, r):
		return (v.getX() - self.getX())**2 + (v.getY() - self.getY())**2 <= r * r

	def distance(self, v):
		return math.sqrt((v.getX() - self.getX())**2 + (v.getY() - self.getY())**2);

	def rotate(self, angle):
		nx = (self.getX() * math.cos(angle)) - (self.getY() * math.sin(angle))
		ny = (self.getX() * math.sin(angle)) + (self.getY() * math.cos(angle))
		return Vector(nx, ny)

	def getAngle(self):
		return math.atan2(self.getY(), self.getX())
