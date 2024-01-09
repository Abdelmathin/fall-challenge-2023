import sys
import math
import socket

class Creature:
    def __init__(self, creature_id, color, _type):
        self._creature_id  = creature_id
        self._color        = color
        self._type         = _type
        self._creature_x   = 0
        self._creature_y   = 0
        self._creature_vx  = 0
        self._creature_vy  = 0
        self._region       = "BL"

    def getTyoe(self):
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
        return (self.getTyoe() < 0)

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

def move(self.drones[i], self.visible_creatures, x, y, light):
    print("MOVE {} {} {}".format(x, y, light))

class Snapshot:
    pass


class SeabedSecurity:

    def __init__(self):
        self.creature_count = int(input())
        self.creatures = {}
        self.scanned = {}
        self.foe_scanned = {}
        self.drones = [None, None]
        self.foe_drones = [None, None]
        for i in range(self.creature_count):
            creature_id, color, _type = [int(j) for j in input().split()]
            self.creatures[creature_id] = Creature(creature_id, color, _type)

    def loop(self):
        while True:
            snapshot = Snapshot()
            self.my_score = int(input())
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
                self.foe_drones[i] = Drone(drone_id, drone_x, drone_y, emergency, battery)

            self.drone_scan_count = int(input())
            for i in range(self.drone_scan_count):
                drone_id, creature_id = [int(j) for j in input().split()]

            self.visible_creatures = []
            visible_creature_count = int(input())
            for i in range(visible_creature_count):
                creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
                self.creatures[creature_id].setX(creature_x)
                self.creatures[creature_id].setY(creature_y)
                self.creatures[creature_id].setXVelocity(creature_vx)
                self.creatures[creature_id].setYVelocity(creature_vy)
                self.visible_creatures.append(self.creatures[creature_id])

            radar_blip_count = int(input())
            for i in range(radar_blip_count):
                inputs = input().split()
                drone_id = int(inputs[0])
                creature_id = int(inputs[1])
                radar = inputs[2]
                self.creatures[creature_id].setRegion(radar)

            for i in range(self.my_drone_count):
                if (i == 1):
                    print("MOVE 0 0 0")
                    continue
                move(self.drones[i], self.visible_creatures, 8000, 9000, 0)

if (__name__ == "__main__"):
    game = SeabedSecurity()
    game.loop()
