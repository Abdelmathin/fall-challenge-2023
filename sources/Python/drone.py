import sys
import math
from math import cos, sin, tan
from utils import distance
from constants import *
from entities import Entity

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
						# if (self.getGame().getCollision(self, ugly).happened()):
						# 	is_safe_path = False
						# 	break
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
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
		[target_x, target_y] = self.getSafePath(target)
		self.speed = Vector(target_x - self.getX(), target_y - self.getY())
		if (self.speed.length() > DRONE_MOVE_SPEED):
			self.speed = self.speed.normalize().mult(DRONE_MOVE_SPEED)
		if (self.lightOn):
			self.lastLightPos = Vector(self.getX(), self.getY())
		print("MOVE {} {} {} {}".format(int(target_x), int(target_y), 1 if self.lightOn else 0, message))
