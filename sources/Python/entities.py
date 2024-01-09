import math
import copy
from utils import *
from constants import *

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

	#################### getter's ####################

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

	#################### setter's ####################

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
	# # # # # # # # # # # # # # # # # # # # # # # # #
	def __str__(self):
		return ('<{} id={} x={} y={}, vx={}, vy={}/>'.format(self.name, self.getId(), self.getX(), self.getY(), self.getXVelocity(), self.getYVelocity()))

	def __repr__(self):
		return (str(self))
	# # # # # # # # # # # # # # # # # # # # # # # # #
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
		self.fleeingFromPlayer = 0
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
