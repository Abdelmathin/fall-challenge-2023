import sys
import math

class Creature:
	def __init__(self, creature_id, color, _type):
		self._creature_id  = creature_id
		self._color	       = color
		self._type		   = _type
		self._creature_x   = 0
		self._creature_y   = 0
		self._creature_vx  = 0
		self._creature_vy  = 0
		self._region	   = "BL"

	def getType(self):
		return self._type

	def setX(self, x):
		self._creature_x  = x

	def setY(self,y):
		self._creature_y  = y

	def setXVelocity(self, xv):
		self._creature_vx  = xv

	def setYVelocity(self, yv):
		self._creature_vy  = yv
	
	def setRegion(self, r):
		self._region = r

	def getX(self):
		return self._creature_x

	def getY(self):
		return self._creature_y

	def getXVelocity(self):
		return self._creature_vx

	def getYVelocity(self):
		return self._creature_vy
	
	def getRegion(self):
		return self._region
	
	def isMonster(self):
		return (self.getType() < 0)

class Drone:
	def __init__(self, drone_id, drone_x, drone_y, emergency, battery):
		self._drone_id  = drone_id
		self._drone_x   = drone_x
		self._drone_y   = drone_y
		self._emergency = emergency
		self._battery   = battery

	def getId(self):
		return self._drone_id

	def getBattery(self):
		return (self._battery)

	def getEmergency(self):
		return (self._emergency)

	def getX(self):
		return self._drone_x

	def getY(self):
		return self._drone_y

	def __str__(self):
		res = ("<drone pos=({}, {}) emergency={} battery={}/>".format(self.getX(), self.getY(), self.getEmergency(), self.getBattery()))
		print(res, file = sys.stderr, flush = True)
		return res

	def __repr__(self):
		return (str(self))

class SeabedSecurity:

	def __init__(self):
		self.creature_count = int(input())
		self.creatures = {}
		self.scanned = {}
		self.foe_scanned = {}
		self.drones = [None, None]
		self.foe_drones = {}
		for i in range(self.creature_count):
			creature_id, color, _type = [int(j) for j in input().split()]
			self.creatures[creature_id] = Creature(creature_id, color, _type)

	def getMyScore(self):
		return (self.my_score)

	def getFoeScore(self):
		return (self.foe_score)

	def loop(self):
		while True:
			self.setMyScore(int(input()))
			self.setFoeScore(int(input()))
			self.setMyScanCount(int(input()))

			self.foe_score = int(input())
			self.my_scan_count = int(input())
			for i in range(self.my_scan_count):
				creature_id = int(input())
				self.scanned[creature_id] = self.creatures[creature_id]

			self.foe_scan_count = int(input())
			for i in range(self.foe_scan_count):
				creature_id = int(input())
				self.foe_scanned[creature_id] = self.creatures[creature_id]

			self.my_drone_count = int(input())

			for i in range(self.my_drone_count):
				drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
				self.drones[i] = Drone(drone_id, drone_x, drone_y, emergency, battery)

			self.foe_drone_count = int(input())
			for i in range(self.foe_drone_count):
				drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
				self.foe_drones[drone_id] = Drone(drone_id, drone_x, drone_y, emergency, battery)

			self.drone_scan_count = int(input())
			for i in range(self.drone_scan_count):
				drone_id, creature_id = [int(j) for j in input().split()]

			visible_creature_count = int(input())
			for i in range(visible_creature_count):
				creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
				self.creatures[creature_id].setX(creature_x)
				self.creatures[creature_id].setY(creature_y)
				self.creatures[creature_id].setXVelocity(creature_vx)
				self.creatures[creature_id].setYVelocity(creature_vy)

			radar_blip_count = int(input())
			for i in range(radar_blip_count):
				inputs = input().split()
				drone_id = int(inputs[0])
				creature_id = int(inputs[1])
				radar = inputs[2]
				self.creatures[creature_id].setRegion(radar)

			for i in range(self.my_drone_count):
				x = self.drones[i].getX()
				if (i == 0):
					print("MOVE {} {} {} {}".format(2500, 3750, 0, visible_creature_count))
				else:
					print ("WAIT 0")
				# if (i == 0):
				#	move_lucy_drone()
				# else:
				#	print("WAIT 1")

class Algorithm:
	def __init__(self, game):
		self.game = game

	def distance(a, b):
		return math.sqrt((a.getX() - b.getX())**2 + (a.getY() - b.getY())**2)

	def lineIntersectsCircle(ahead, ahead2, obstacle):
		return distance(obstacle.center, ahead) <= obstacle.radius or distance(obstacle.center, ahead2) <= obstacle.radius;

	def collisionAvoidance():
		ahead  = position + normalize(velocity) * MAX_SEE_AHEAD
		ahead2 = position + normalize(velocity) * MAX_SEE_AHEAD * 0.5

	var mostThreatening :Obstacle = findMostThreateningObstacle();
	var avoidance :Vector3D = new Vector3D(0, 0, 0);
	if (mostThreatening != null) {
		avoidance.x = ahead.x - mostThreatening.center.x;
		avoidance.y = ahead.y - mostThreatening.center.y;
		avoidance.normalize();
		avoidance.scaleBy(MAX_AVOID_FORCE);
	} else {
		avoidance.scaleBy(0); // nullify the avoidance force 
	}
	return avoidance;

if (__name__ == "__main__"):
	game = SeabedSecurity()
	game.loop()
