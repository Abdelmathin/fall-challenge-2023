import sys
import math
from constants import *
from utils import get_next_line, distance
from entities import Fish, Ugly, GamePlayer

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
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
			# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
			for i in range(radar_blip_count):
				inputs      = get_next_line().split()
				drone_id    = int(inputs[0])
				fish_id     = int(inputs[1])
				radar       = inputs[2]
				self.elements[fish_id].setRadarBlip(self.elements[drone_id], radar, self.player.visibles)
				self.elements[drone_id].setEntityRadar(self.elements[fish_id], radar)
			# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
			if (self.turn == 0):
				for fish_id, fish in self.getFishes().items():
					if (fish.getX() <= WIDTH / 2):
						opp_fish_id = self.getOppositeIdById(fish_id)
						self.player.drones[0].targets[fish_id]     = fish_id
						self.player.drones[1].targets[opp_fish_id] = opp_fish_id
				for fish_id in [8, 9, 14, 15]:
					for drone in self.player.drones:
						drone.targets[fish_id] = fish_id
			# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
			for drone in self.player.drones:
				self.updateDroneTargets(drone)
				self.updateDroneTarget(drone)
				light = self.getLight(drone)
				drone.moveTo(drone.target, light, [drone.battery, self.player.expectedPoints()])
			self.finiTrun()
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
	# # # # # # # # # # # # # # START:simulation # # # # # # # # # # # # #
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
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
			if ((fish.fleeingFromPlayer != None) and (fish.fleeingFromPlayer != -1)):
				self.chasedFishCount[fish.fleeingFromPlayer] += 1
			self.getFishes()[fish.getId()].pos = Vector(0, 0)
		
		for fish in self.getFishes().values():
			fish.fleeingFromPlayer = None

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
				# print (">>> a 1", ugly.speed, file = sys.stderr)
				attackVec = Vector(ugly.pos, target)
				if (attackVec.length() > UGLY_ATTACK_SPEED):
					attackVec = attackVec.normalize().mult(UGLY_ATTACK_SPEED)
				ugly.speed = attackVec.round()
				# print (">>> b 1", ugly.speed, file = sys.stderr)
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
				# print (">>> 2", ugly.speed, file = sys.stderr)

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

	# # # # # # # # # # # # # # # END:simulation # # # # # # # # # # # # # #

	def getLight(self, drone):
		[x, y] = [drone.lastLightPos.getX(), drone.lastLightPos.getY()]
		if 800 <= distance([x, y], [drone.getX(), drone.getY()]):
			return (1)
		# minDist = None
		# for fish_id, fish in self.getElements().items():
		# 	if (self.isScanned(fish_id)):
		# 		continue
		# 	d = fish.pos.distance(drone.pos)
		# 	if (minDist == None) or (d < minDist):
		# 		minDist = d
		# if (minDist != None) and (minDist < 1200):
		# 	return (1)
		return (0)

	def updateDroneTarget(self, drone):
		if not (drone.currentLevelTargets) or len(self.player.scans) - len(self.player.saved) > 9:
			drone.target = Vector(drone.getX(), 0)
			return (drone.target)
		# targets_list = []
		# for fish_id in drone.currentLevelTargets:
		# 	targets_list.append(self.getFishes()[fish_id])
		# drone.target = Closest(targets_list, 0.0).getMeanPos()
		# return (drone.target)
		#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
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
		if (self.bothPlayersHaveScannedAllRemainingFish()):
			return (True)
		return ((self.turn >= 200) or self.computeMaxPlayerScore(self.player) < self.enemy.points or self.computeMaxPlayerScore(self.enemy) < self.player.points)
