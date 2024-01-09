import math
import copy
import sys
import math
import builtins
import sys
import math
from math import cos, sin, tan
import sys
import math
import sys
import math
TYPE_DRONE                     = 1000000
TYPE_UGLY                      = -1
UNKNOWN_COLOR                  = -1
WIDTH                          = 10000
HEIGHT                         = 10000
DRONES_PER_PLAYER              = 2
UGLY_UPPER_Y_LIMIT             = 2500
DRONE_UPPER_Y_LIMIT            = 0
DRONE_START_Y                  = 500
COLORS_PER_FISH                = 4
DRONE_MAX_BATTERY              = 30
LIGHT_BATTERY_COST             = 5
DRONE_BATTERY_REGEN            = 1
DARK_SCAN_RANGE                = 800
LIGHT_SCAN_RANGE               = 2000
UGLY_EAT_RANGE                 = 300
DRONE_HIT_RANGE                = 200
FISH_HEARING_RANGE             = (DARK_SCAN_RANGE + LIGHT_SCAN_RANGE) / 2
DRONE_MOVE_SPEED               = 600
DRONE_SINK_SPEED               = 300
DRONE_EMERGENCY_SPEED          = 300
DRONE_MOVE_SPEED_LOSS_PER_SCAN = 0
FISH_SWIM_SPEED                = 200
FISH_AVOID_RANGE               = 600
FISH_FLEE_SPEED                = 400
UGLY_ATTACK_SPEED              = int(DRONE_MOVE_SPEED * 0.9)
UGLY_SEARCH_SPEED              = int(UGLY_ATTACK_SPEED / 2)
FISH_X_SPAWN_LIMIT             = 1000
FISH_SPAWN_MIN_SEP             = 1000
MAX_TURNS                      = 201
ENABLE_UGLIES                  = True
FISH_WILL_FLEE                 = True
FISH_WILL_MOVE                 = True
SIMPLE_SCANS                   = False
INFINITY                       = 1000000000
MAX_ANALYSIS_TURN              = 4
DOWN                           = 0
UP                             = 1
OPPOSITES = {
	10  : 11,
	11  : 10,
	4   : 5 ,
	5   : 4 ,
	6   : 7 ,
	7   : 6 ,
	12  : 13,
	13  : 12,
	14  : 15,
	15  : 14,
	8   : 9 ,
	9   : 8 ,
	16  : 17,
	17  : 16,
	18  : 19,
	19  : 18,
	20  : 21,
	21  : 20,
	22  : 23,
	23  : 22,
}
FISH_LOW_Y = {
	0  : 0,
	1  : 0,
	2  : 0,
	3  : 0,
	5  : 2500,
	10 : 2500,
	11 : 2500,
	4  : 2500,
	6  : 5000,
	7  : 5000,
	12 : 5000,
	13 : 5000,
	8  : 7500,
	15 : 7500,
	14 : 7500,
	9  : 7500,
	16 : 2500,
	17 : 2500,
	18 : 2500,
	19 : 2500,
	20 : 2500,
	21 : 2500,
	22 : 2500,
	23 : 2500,
}
FISH_HIGH_Y = {
	0  : HEIGHT - 1,
	1  : HEIGHT - 1,
	2  : HEIGHT - 1,
	3  : HEIGHT - 1,
	5  : 5000,
	10 : 5000,
	11 : 5000,
	4  : 5000,
	6  : 7500,
	7  : 7500,
	12 : 7500,
	13 : 7500,
	8  : 10000,
	15 : 10000,
	14 : 10000,
	9  : 10000,
	16 : 10000,
	17 : 10000,
	18 : 10000,
	19 : 10000,
	20 : 10000,
	21 : 10000,
	22 : 10000,
	23 : 10000,
}
patterns = [
	[
		[2500, 5000],
		[1000, 8500],
		[300, 0],
	],
	[
		[7500, 4500],
		[6000, 8000],
		[9000, 6000],
		[8500, 450],
	]
]
destinations = [
	patterns[0][0],
	patterns[1][0]
]
MIN_RANGE_RADIUS = 800
class Entity:
	def __init__(self, _id = -1, _color = -1, _type = -1):		
		self.lowY       = FISH_LOW_Y[_id]
		self.highY      = FISH_HIGH_Y[_id]
		self.lowX       = 0
		self.highX      = WIDTH
		self.pos        = Vector((self.lowX + self.highX) / 2, (self.lowY + self.highY) / 2)
		self.speed      = Vector(0, 0)
		self.id         = _id
		self.color      = _color
		self.type       = _type
		self.detected   = False
		self.approached = False
		self.name       = "unknown"
		self.radars     = {}
		self.game       = None
		self.minX       = self.lowX
		self.maxX       = self.highX
		self.minY       = self.lowY
		self.maxY       = self.highY
		self.visible    = False
	def __call__(self, _x, _y, _vx, _vy):
		opp = self.getGame().getElements()[OPPOSITES[self.getId()]]
		if not opp.isDetected():
			opp.setDetected(True)
			opp.setVisibility(True)
			opp.setMinX(WIDTH - 1 - _x)
			opp.setMaxX(WIDTH - 1 - _x)
			opp.setMinY(_y)
			opp.setMaxY(_y)
		self.setVisibility(True)
		self.setDetected(True)
		self.setMinX(_x)
		self.setMaxX(_x)
		self.setMinY(_y)
		self.setMaxY(_y)
		self.setXVelocity(_vx)
		self.setYVelocity(_vy)
	def deepcopy(self):
		return (copy.deepcopy(self))
	def isDetected(self):
		return (self.detected)
	def getGame(self):
		return (self.game)
	def getX(self):
		return (self.getPos().getX())
	def getY(self):
		return (self.getPos().getY())
	def getMinX(self):
		return (self.minX)
	def getMaxX(self):
		return (self.maxX)
	def getMinY(self):
		return (self.minY)
	def getMaxY(self):
		return (self.maxY)
	def getXVelocity(self):
		return (self.getSpeed().getX())
	def getYVelocity(self):
		return (self.getSpeed().getY())
	def getVelocity(self):
		return (math.sqrt(self.getXVelocity()**2 + self.getYVelocity()**2))
	def getPos(self):
		return (self.pos)
	def getSpeed(self):
		return (self.speed)
	def getId(self):
		return (self.id)
	def getType(self):
		return (self.type)
	def getColor(self):
		return (self.color)
	def setGame(self, _game):
			self.game = _game
	def setId(self, _id):
		self.id = _id
	def setX(self, _x):
		self.pos.setX(_x)
	def setY(self, _y):
		self.pos.setY(_y)
	def setMinX(self, minX):
		self.minX = minX
		self.setX((self.minX + self.maxX) / 2)
	def setMaxX(self, maxX):
		self.maxX = maxX
		self.setX((self.minX + self.maxX) / 2)
	def setMinY(self, minY):
		self.minY = minY
		self.setY((self.minY + self.maxY) / 2)
	def setMaxY(self, maxY):
		self.maxY = maxY
		self.setY((self.minY + self.maxY) / 2)
	def setPosition(self, _x, _y):
		self.setX(_x)
		self.setY(_y)
	def setXVelocity(self, _vx):
		self.speed.setX(_vx)
	def setYVelocity(self, _vy):
		self.speed.setY(_vy)
	def setDetected(self, value):
		self.detected = value
	def setVisibility(self, _visible):
		self.visible = _visible
	def __str__(self):
		return ('<{} id={} x={} y={}, vx={}, vy={}/>'.format(self.name, self.getId(), self.getX(), self.getY(), self.getXVelocity(), self.getYVelocity()))
	def __repr__(self):
		return (str(self))
	def isOut(self):
		return (False)
	def isUgly(self):
		return (False)
	def setRadarBlip(self, drone, radar, visibles):
		if (self.getId() in visibles):
			return
		if (radar in ["BL", "TL"]):
			if (self.getMaxX() > drone.getX()):
				self.setMaxX(drone.getX())
		elif (radar in ["TR", "BR"]):
			if (self.getMinX() < drone.getX()):
				self.setMinX(drone.getX())
		if (radar in ["TL", "TR"]):
			if (self.getMaxY() > self.getY()):
				self.setMaxY(drone.getY())
		elif (radar in ["BL", "BR"]):
			if (self.getMinY() < self.getY()):
				self.setMinY(drone.getY())
		opp = self.getGame().getElements()[OPPOSITES[self.getId()]]
		if not opp.isDetected():
			if (abs(opp.getMaxX() - opp.getMinX()) > abs(self.getMaxX() - self.getMinX())):
				opp.setMinX(WIDTH - 1 - self.getMaxX())
				opp.setMaxX(WIDTH - 1 - self.getMinX())
			if (abs(opp.getMaxY() - opp.getMinY()) > abs(self.getMaxY() - self.getMinY())):
				opp.setMinY(self.getMinY())
				opp.setMaxY(self.getMaxY())
class Fish(Entity):
	def __init__(self, _id, _color, _type):
		super(Fish, self).__init__(_id = _id, _color = _color, _type = _type)
		self.fleeingFromGamePlayer = 0
		self.name              = "fish"
	def getLowY(self):
		return (self.lowY)
	def getHighY(self):
		return (self.highY)
class Ugly(Entity):
	def __init__(self, _id):
		super(Ugly, self).__init__(_id = _id, _type = TYPE_UGLY, _color = UNKNOWN_COLOR)
		self.foundTarget = False
		self.target      = None
		self.name        = "ugly"
	def isUgly(self):
		return (True)
class GamePlayer:
	def __init__(self, game):
		self.game     = game
		self.drones   = []
		self.score    = 0
		self.saved    = {}
		self.scans    = {}
		self.droneIds = {}
	def loadDrones(self):
		dronesNumber = int(get_next_line())
		for droneIndex in range(dronesNumber):
			[drone_id, drone_x, drone_y, emergency, battery] = [int(j) for j in get_next_line().split()]
			self.droneIds[drone_id] = drone_id
			if (droneIndex >= len(self.drones)):
				self.drones.append(Drone(droneIndex, self.game, drone_id, drone_x, drone_y, emergency, battery))
			self.drones[droneIndex](drone_id, drone_x, drone_y, emergency, battery)
			self.drones[droneIndex].clearRadarInfo()
			self.game.getElements()[drone_id] = self.drones[droneIndex]
		self.drones[0].friend = self.drones[1]
		self.drones[1].friend = self.drones[0]
	def expectedPoints(self):
		self.has4Types  = False
		self.has3Colors = False
		points  = 0
		colors  = {}
		types   = {}
		visited = {}
		for drone in self.drones:
			for fish_id in drone.scans:
				if fish_id in visited:
					continue
				visited[fish_id] = True
				fish = self.game.getFishes()[fish_id]
				points += 2 * (fish.getType() + 1)
				colors[fish.color] = colors.get(fish.color, 0)
				colors[fish.color] = colors[fish.color] + 1
				types[fish.type]   = types.get(fish.type, 0)
				types[fish.type]   = types[fish.type] + 1
				if (colors[fish.color] == 3):
					self.has3Colors = True
					points += 6
					colors[fish.color] = -1000000
				if (types[fish.type] == 4):
					self.has4Types = True
					points += 8
					types[fish.type] = -1000000
		return (points)
def get_next_line():
	line = input()
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
class Drone(Entity):
	def __init__(self, _index, _game, _id, _x, _y, _emergency, _battery):
		super(Drone, self).__init__(_id = _id)
		self.name                  = "drone"
		self.index                 = _index
		self.game                  = _game
		self.old_battery           = _battery
		self.battery               = _battery
		self.emergency             = _emergency
		self.light                 = 0
		self.scans                 = {}
		self.lightSwitch           = False
		self.dying                 = False
		self.dead                  = False
		self.didReport             = False
		self.lightOn               = None
		self.fishesScannedThisTurn = []
		self.message               = ""
		self.dieAt                 = None
		self.maxTurnsSpentWithScan = None
		self.turnsSpentWithScan    = None
		self.maxY                  = None
		self.move                  = None
		self.lastLightPos          = Vector(_x, _y)
		self.isLastTimeLightOn     = False
		self.lastPosX              = None
		self.lastPosY              = None
		self.target                = None
		self.targets               = {} # {id : id}
		self.currentLevelTargets   = {} # {id : id}
		self.spin                  = DOWN
		self.mode                  = None
		self.player                = None
		self.visibles              = {}
		self.pathIndex             = 0
		self.path                  = []
		self.__call__(_id, _x, _y, _emergency, _battery)
		self.clearRadarInfo()
	def clearRadarInfo(self):
		self.radar_info = {
			"uglies" : {
				"TL" : {},
				"TR" : {},
				"BL" : {},
				"BR" : {},
			},
			"fishs" : {
				"TL" : {},
				"TR" : {},
				"BL" : {},
				"BR" : {},
			}
		}
	def getTLUglies(self):
		return (list(self.radar_info["uglies"]["TL"].keys()))
	def getTRUglies(self):
		return (list(self.radar_info["uglies"]["TR"].keys()))
	def getBLUglies(self):
		return (list(self.radar_info["uglies"]["BL"].keys()))
	def getBRUglies(self):
		return (list(self.radar_info["uglies"]["BR"].keys()))
	def getTLFishs(self):
		return (list(self.radar_info["fishs"]["TL"].keys()))
	def getTRFishs(self):
		return (list(self.radar_info["fishs"]["TR"].keys()))
	def getBLFishs(self):
		return (list(self.radar_info["fishs"]["BL"].keys()))
	def getBRFishs(self):
		return (list(self.radar_info["fishs"]["BR"].keys()))
	def setEntityRadar(self, entity, radar):
		if (entity.isUgly()):
			self.radar_info["uglies"][radar][entity] = 1
		else:
			self.radar_info["fishs"][radar][entity] = 1
	def __call__(self, _id, _x, _y, emergency, battery):
		self.lastPosX    = self.getX()
		self.lastPosY    = self.getY()
		self.setId(_id)
		self.setX(_x)
		self.setY(_y)
		self.old_battery = self.battery
		self.emergency   = emergency
		self.battery     = battery
		self.lightOn     = None
		if _y < 600:
			self.dying = False
			self.dead  = False
	def getIndex(self):
		return (self.index)
	def isEngineOn(self):
		return (self.move != None)
	def isLightOn(self):
		if ((self.getId() % 2) == 0):
			return (self.lightOn)
		return (abs(self.old_battery - self.battery) > 2)
	def drainBattery(self):
		self.battery -= LIGHT_BATTERY_COST
	def rechargeBattery(self):
		if (self.battery < DRONE_MAX_BATTERY):
			self.battery += DRONE_BATTERY_REGEN
			if (self.battery >= DRONE_MAX_BATTERY):
				self.battery = Game.DRONE_MAX_BATTERY
	def isDeadOrDying(self):
		return (self.dying or self.dead)
	def getSafePath(self, target):
		self.speed       = Vector(self.pos, target)
		currentDroneX    = self.getX()
		currentDroneY    = self.getY()
		targetDroneAngle = self.speed.getAngle()
		moveVectorLength = self.speed.length()
		if (moveVectorLength > DRONE_MOVE_SPEED):
			moveVectorLength = DRONE_MOVE_SPEED
		alpha = 0.0
		while (alpha < 3.5):
			_moveVectorLength = moveVectorLength
			while (_moveVectorLength > 0):
				for angle in [targetDroneAngle + alpha, targetDroneAngle - alpha]:
					nextDroneXSpeed   = _moveVectorLength * math.cos(angle)
					nextDroneYSpeed   = _moveVectorLength * math.sin(angle)
					nextDroneX        = int(currentDroneX + nextDroneXSpeed)
					nextDroneY        = int(currentDroneY + nextDroneYSpeed)
					if (nextDroneX < 0):
						nextDroneX = 0
					if (nextDroneX > WIDTH - 1):
						nextDroneX = WIDTH - 1
					if (nextDroneY < 0):
						nextDroneY = 0
					if (nextDroneY > HEIGHT - 1):
						nextDroneY = HEIGHT - 1
					self.speed        = Vector(nextDroneXSpeed, nextDroneYSpeed)
					is_safe_path      = True
					for ugly in self.getGame().getUglies().values():
						uglyStartX = ugly.getX()
						uglyStartY = ugly.getY()
						uglyEndX   = uglyStartX + ugly.getXVelocity()
						uglyEndY   = uglyStartY + ugly.getYVelocity()
						if (playerCollidesWithEnemy(currentDroneX, currentDroneY, nextDroneX, nextDroneY, uglyStartX, uglyStartY, uglyEndX, uglyEndY, DRONE_HIT_RANGE + UGLY_EAT_RANGE)):
							is_safe_path = False
							break
					if is_safe_path:
						return ([nextDroneX, nextDroneY])
				_moveVectorLength -= 71
			alpha += 0.1
		return ([0, 0])
	def moveTo(self, target, lightSwitch, message):
		if (lightSwitch and (self.battery >= LIGHT_BATTERY_COST)):
			self.lightOn = 1
		else:
			self.lightOn = 0
		[target_x, target_y] = self.getSafePath(target)
		self.speed = Vector(target_x - self.getX(), target_y - self.getY())
		if (self.speed.length() > DRONE_MOVE_SPEED):
			self.speed = self.speed.normalize().mult(DRONE_MOVE_SPEED)
		if (self.lightOn):
			self.lastLightPos = Vector(self.getX(), self.getY())
		print("MOVE {} {} {} {}".format(int(target_x), int(target_y), 1 if self.lightOn else 0, message))
class SeabedSecurity:
	def __init__(self):
		self.player           = GamePlayer(self)
		self.enemy            = GamePlayer(self)
		self.turn             = 0
		self.uglies           = {}
		self.fishes           = {}
		self.elements         = {}
		self.chasedFishCount  = [0, 0]
		fish_count            = int(get_next_line())
		for i in range(fish_count):
			_id, _color, _type = [int(j) for j in get_next_line().split()]
			if (_type == -1):
				self.uglies[_id] = Ugly(_id)
				self.uglies[_id].setGame(self)
				self.elements[_id] = self.uglies[_id]
			else:
				self.fishes[_id] = Fish(_id, _color, _type)
				self.fishes[_id].setGame(self)
				self.elements[_id] = self.fishes[_id]
		self.setAnalysisMode(True)
	def loop(self):
		while True:
			self.initTrun()
			self.player.score = int(get_next_line())
			self.enemy.score  = int(get_next_line())
			mySaveNumber      = int(get_next_line())
			for i in range(mySaveNumber):
				fish_id = int(get_next_line())
				self.player.saved[fish_id] = fish_id
			foeSaveNumber = int(get_next_line())
			for i in range(foeSaveNumber):
				fish_id = int(get_next_line())
				self.enemy.saved[fish_id] = fish_id
			self.player.loadDrones()
			self.enemy.loadDrones()
			drone_scan_count = int(get_next_line())
			for i in range(drone_scan_count):
				drone_id, fish_id = [int(j) for j in get_next_line().split()]
				if (drone_id in self.player.droneIds):
					self.elements[drone_id].player = self.player
					self.player.scans[fish_id] = fish_id
				else:
					self.elements[drone_id].player = self.enemy
					self.enemy.scans[fish_id] = fish_id
				self.elements[drone_id].scans[fish_id] = fish_id
			self.player.visibles = {}
			visible_fish_count   = int(get_next_line())
			for i in range(visible_fish_count):
				fish_id, fish_x, fish_y, fish_vx, fish_vy = [int(j) for j in get_next_line().split()]
				self.player.visibles[fish_id] = fish_id
				self.elements[fish_id](fish_x, fish_y, fish_vx, fish_vy)
			radar_blip_count = int(get_next_line())
			for i in range(radar_blip_count):
				inputs      = get_next_line().split()
				drone_id    = int(inputs[0])
				fish_id     = int(inputs[1])
				radar       = inputs[2]
				self.elements[fish_id].setRadarBlip(self.elements[drone_id], radar, self.player.visibles)
				self.elements[drone_id].setEntityRadar(self.elements[fish_id], radar)
			if (self.turn == 0):
				for fish_id, fish in self.getFishes().items():
					if (fish.getX() <= WIDTH / 2):
						opp_fish_id = self.getOppositeIdById(fish_id)
						self.player.drones[0].targets[fish_id]     = fish_id
						self.player.drones[1].targets[opp_fish_id] = opp_fish_id
				for fish_id in [8, 9, 14, 15]:
					for drone in self.player.drones:
						drone.targets[fish_id] = fish_id
			for drone in self.player.drones:
				self.updateDroneTargets(drone)
				self.updateDroneTarget(drone)
				light = self.getLight(drone)
				drone.moveTo(drone.target, light, [drone.battery, self.player.expectedPoints()])
			self.finiTrun()
	def isAnalysisMode(self):
		return (self._is_analysis_mode)
	def setAnalysisMode(self, mode):
		self._is_analysis_mode = mode
	def initTrun(self):
		pass
	def finiTrun(self):
		self.turn += 1
		self.updateDrones()
		self.moveEntities()
		self.updateUglyTargets()
		self.updateUglySpeeds()
	def getCollision(self, drone, ugly):
		if (ugly.getPos().isZero()):
			return NONE_COLLISION
		if (ugly.getPos().inRange(drone.pos, DRONE_HIT_RANGE + UGLY_EAT_RANGE)):
			return Collision(0.0, ugly, drone)
		if (drone.speed.isZero() and ugly.speed.isZero()):
			return NONE_COLLISION
		x  = ugly.pos.getX()
		y  = ugly.pos.getY()
		ux = drone.pos.getX()
		uy = drone.pos.getY()
		x2  = x - ux
		y2  = y - uy
		r2  = DRONE_HIT_RANGE + UGLY_EAT_RANGE
		vx2 = ugly.speed.getX() - drone.speed.getX()
		vy2 = ugly.speed.getY() - drone.speed.getY()
		a = vx2 * vx2 + vy2 * vy2
		if (a <= 0.0):
			return NONE_COLLISION
		b     = 2.0 * (x2 * vx2 + y2 * vy2)
		c     = x2 * x2 + y2 * y2 - r2 * r2
		delta = b * b - 4.0 * a * c
		if (delta < 0.0):
			return NONE_COLLISION
		t = (-b - math.sqrt(delta)) / (2.0 * a)
		if (t <= 0.0):
			return NONE_COLLISION
		if (t > 1.0):
			return NONE_COLLISION
		return Collision(t, ugly, drone)
	def updateDrones(self):
		for drone in self.getDrones():
			moveSpeed = int(DRONE_MOVE_SPEED - DRONE_MOVE_SPEED * DRONE_MOVE_SPEED_LOSS_PER_SCAN * len(drone.scans))
			if (drone.dead):
				floatVec = Vector(0, -1).mult(DRONE_EMERGENCY_SPEED)
				drone.speed = floatVec
			elif (drone.move != None):
				moveVec = Vector(drone.pos, drone.move)
				if (moveVec.length() > moveSpeed):
					moveVec = moveVec.normalize().mult(moveSpeed)
				drone.speed = moveVec.round()
			elif (drone.pos.getY() < HEIGHT - 1):
				sinkVec = Vector(0, 1).mult(DRONE_SINK_SPEED)
				drone.speed = sinkVec
	def moveEntities(self):
		for drone in self.getDrones():
			for ugly in self.getUglies().values():
				col = self.getCollision(drone, ugly)
				if (col.happened()):
					drone.dying = True
					drone.scans.clear()
					drone.dieAt = col.t
					print (">>>> drone {} is hit by monster {}!".format(drone.id, ugly.id), file = sys.stderr)
					break
		for drone in self.getDrones():
			drone.pos = drone.pos.add(drone.speed)
			self.snapToDroneZone(drone)
		for fish in self.getFishes().values():
			fish.pos = fish.pos.add(fish.speed)
			self.snapToFishZone(fish)
			fish.setVisibility(False)
		for ugly in self.getUglies().values():
			ugly.pos = ugly.pos.add(ugly.speed)
			self.snapToUglyZone(ugly)
			ugly.setVisibility(False)
		fishToRemove = []
		for fish in self.getFishes().values():
			if ((fish.getPos().getX() > WIDTH - 1) or (fish.getPos().getX() < 0)):
				fishToRemove.append(fish)
		for fish in fishToRemove:
			if ((fish.fleeingFromGamePlayer != None) and (fish.fleeingFromGamePlayer != -1)):
				self.chasedFishCount[fish.fleeingFromGamePlayer] += 1
			self.getFishes()[fish.getId()].pos = Vector(0, 0)
		for fish in self.getFishes().values():
			fish.fleeingFromGamePlayer = None
	def snapToFishZone(self, fish):
		fish_id = fish.getId()
		if (fish.getY() > HEIGHT - 1):
			self.getFishes()[fish_id].setPosition(fish.getX(), HEIGHT - 1)
		elif (fish.getY() > fish.getHighY()):
			self.getFishes()[fish_id].setPosition(fish.getX(), fish.getHighY())
		elif (fish.getY() < fish.getLowY()):
			self.getFishes()[fish_id].setPosition(fish.getX(), fish.getLowY())
	def snapToUglyZone(self, ugly):
		ugly_id = ugly.getId()
		if (ugly.getY() > HEIGHT - 1):
			self.getUglies()[ugly_id].setPosition(ugly.getX(), HEIGHT - 1)
		elif (ugly.getY() < UGLY_UPPER_Y_LIMIT):
			self.getUglies()[ugly_id].setPosition(ugly.getX(), UGLY_UPPER_Y_LIMIT)
	def snapToDroneZone(self, drone):
		if (drone.pos.getY() > HEIGHT - 1):
			drone.pos = Vector(drone.pos.getX(), HEIGHT - 1)
		elif (drone.pos.getY() < DRONE_UPPER_Y_LIMIT):
			drone.pos = Vector(drone.pos.getX(), DRONE_UPPER_Y_LIMIT)
		if (drone.pos.getX() < 0):
			drone.pos = Vector(0, drone.pos.getY())
		elif (drone.pos.getX() >= WIDTH):
			drone.pos = Vector(WIDTH - 1, drone.pos.getY())
	def updateUglyTargets(self):
		for ugly in self.getUglies().values():
			foundTarget = self.updateUglyTarget(ugly)
			ugly.foundTarget = foundTarget
	def updateUglyTarget(self, ugly):
		targetableDrones = []
		for drone in self.getDrones():
			lightOn = drone.isLightOn()
			if (drone.pos.inRange(ugly.pos, LIGHT_SCAN_RANGE if lightOn else DARK_SCAN_RANGE)):
				if not drone.isDeadOrDying():
					targetableDrones.append(drone)
		if (targetableDrones):
			closestTargets = self.getClosestTo(ugly.getPos(), targetableDrones)
			ugly.target = closestTargets.getMeanPos()
			return True
		ugly.target = None
		return (False)
	def isScanned(self, fish_id):
		fish = self.getFishes().get(fish_id, None)
		if not fish:
			return (False)
		if (fish_id in self.player.scans):
			return (True)
		if (fish_id in self.player.saved):
			return (True)
		if (fish.isOut()):
			return (True)
		return (False)
	def updateUglySpeeds(self):
		for ugly in self.getUglies().values():
			target = ugly.target
			if (target != None):
				attackVec = Vector(ugly.pos, target)
				if (attackVec.length() > UGLY_ATTACK_SPEED):
					attackVec = attackVec.normalize().mult(UGLY_ATTACK_SPEED)
				ugly.speed = attackVec.round()
			else:
				if (ugly.speed.length() > UGLY_SEARCH_SPEED):
					ugly.speed = ugly.speed.normalize().mult(UGLY_SEARCH_SPEED).round()
				if (not ugly.speed.isZero()):
					closestUglies = self.getClosestTo(ugly.pos, [u for u in self.getUglies().values() if u.getId() != ugly.getId()])
					if (closestUglies.list and closestUglies.distance <= FISH_AVOID_RANGE):
						avoid = closestUglies.getMeanPos()
						avoidDir = Vector(avoid, ugly.pos).normalize()
						if (not avoidDir.isZero()):
							ugly.speed = avoidDir.mult(FISH_SWIM_SPEED).round()
				nextPos = ugly.pos.add(ugly.speed)
				if (((nextPos.getX() < 0) and (nextPos.getX() < ugly.pos.getX())) or ((nextPos.getX() > WIDTH - 1) and (nextPos.getX() > ugly.pos.getX()))):
					ugly.speed = ugly.speed.hsymmetric()
				if (((nextPos.getY() < UGLY_UPPER_Y_LIMIT) and (nextPos.getY() < ugly.pos.getY())) or ((nextPos.getY() > HEIGHT - 1) and (nextPos.getY() > ugly.pos.getY()))):
					ugly.speed = ugly.speed.vsymmetric()
	def getClosestTo(self, vfrom, ltargets):
		minDist  = 0
		closests = []
		for target in ltargets:
			dist = distance([target.getX(), target.getY()], [vfrom.getX(), vfrom.getY()])
			if (closests == []) or (dist < minDist):
				closests = [target]
				minDist = dist
			elif (dist == minDist):
				closests.append(target)
		return Closest(closests, math.sqrt(minDist))
	def getLight(self, drone):
		[x, y] = [drone.lastLightPos.getX(), drone.lastLightPos.getY()]
		if 800 <= distance([x, y], [drone.getX(), drone.getY()]):
			return (1)
		return (0)
	def updateDroneTarget(self, drone):
		if not (drone.currentLevelTargets) or len(self.player.scans) - len(self.player.saved) > 9:
			drone.target = Vector(drone.getX(), 0)
			return (drone.target)
		i = drone.getIndex()
		[target_x, target_y] = destinations[i]
		if (distance([drone.getX(), drone.getY()], [target_x, target_y]) <= MIN_RANGE_RADIUS):
			[target_x, target_y] = destinations[i]
			for pattern_index in range(len(patterns[i])):
				if (patterns[i][pattern_index] == destinations[i]):
					destinations[i] = patterns[i][(pattern_index + 1) % len(patterns[i])]
					break
		drone.target = Vector(target_x, target_y)
		return (drone.target)
	def updateDroneTargets(self, drone):
		drone.currentLevelTargets = {}
		levels = [[4, 5, 10, 11], [6, 7, 12, 13], [8, 9, 14, 15]]
		if (drone.spin == UP):
			levels = [[8, 9, 14, 15], [6, 7, 12, 13], [4, 5, 10, 11]]
		for level in levels:
			for id in level:
				if (not self.isScanned(id)) and (id in drone.targets):
					drone.currentLevelTargets[id] = id
			if (level == levels[-1]):
				drone.spin = 1 - drone.spin
			if len(drone.currentLevelTargets) > 0:
				return (drone)
		return (drone)
	def getOppositeIdById(self, element_id):
		return (OPPOSITES[element_id])
	def getElements(self):
		return (self.elements)
	def getUglies(self):
		return (self.uglies)
	def getDrones(self):
		return (self.player.drones + self.enemy.drones)
	def getFishes(self):
		return (self.fishes)
	def isOver(self):
		if (self.bothGamePlayersHaveScannedAllRemainingFish()):
			return (True)
		return ((self.turn >= 200) or self.computeMaxGamePlayerScore(self.player) < self.enemy.points or self.computeMaxGamePlayerScore(self.enemy) < self.player.points)
game = SeabedSecurity()
game.loop()