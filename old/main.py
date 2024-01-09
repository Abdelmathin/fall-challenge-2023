import sys
import math

class Creature:

	def __init__(self, creature_id, color, _type):
		self.__id__	   = creature_id
		self.__color__ = color
		self.__type__  = _type

	def getPoints(self, game):
		if (game.isFirstScan()):
			

	def getId(self):
		return (self.__id__)

	def getColor(self):
		return (self.__color__)

	def getType(self):
		return (self.__type__)

	def __str__(self):
		return ('<creature id="' + str(self.getId()) + '" color="' + str(self.getColor()) + '" type="' + str(self.getType()) + '">')

	def __repr__(self):
		return (str(self))

class SeabedSecurity:

	def __init__(self):

		self.__creatures__ = {}
		self.__my_score__  = 0
		self.__foe_score__ = 0
		creature_count = int(input())
		for i in range(creature_count):
			creature_id, color, _type = [int(j) for j in input().split()]
			self.__creatures__[creature_id] = Creature(creature_id, color, _type)

	def log(self, *args):
		print (*args, file=sys.stderr, flush=True)

	def getCreatures(self):
		return (self.__creatures__)

	def getMyScore(self):
		return (self.__my_score__)

	def getFoeScore(self):
		return (self.__foe_score__)

	def getMyScanCount(self):
		return (self.__my_scan_count__)

	def getMyScannedCreatures(self):
		pass

	def loop(self):

		while True:
			my_score = int(input())
			foe_score = int(input())
			my_scan_count = int(input())
			for i in range(my_scan_count):
				creature_id = int(input())
			foe_scan_count = int(input())
			for i in range(foe_scan_count):
				creature_id = int(input())
			my_drone_count = int(input())
			for i in range(my_drone_count):
				drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
			foe_drone_count = int(input())
			for i in range(foe_drone_count):
				drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
			drone_scan_count = int(input())
			for i in range(drone_scan_count):
				drone_id, creature_id = [int(j) for j in input().split()]
			visible_creature_count = int(input())
			for i in range(visible_creature_count):
				creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
				
			radar_blip_count = int(input())
			for i in range(radar_blip_count):
				inputs = input().split()
				drone_id = int(inputs[0])
				creature_id = int(inputs[1])
				radar = inputs[2]
			for i in range(my_drone_count):
				self.log(self.getCreatures())
				print("MOVE {0} {1} 0".format(0, 0))


if (__name__ == "__main__"):
	game = SeabedSecurity()
	game.loop()
