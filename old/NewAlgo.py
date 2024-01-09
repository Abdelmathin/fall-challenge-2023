import sys
import math

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
        self.clearRdar()

    def clearRdar(self):
        self.__radar = {}

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
        self.creature_count = int(self.readline())
        self.creatures      = {}
        self.my_drones      = [None, None]
        self.foe_drones     = [None, None]
        for i in range(self.creature_count):
            creature_id, color, _type = [int(j) for j in self.readline().split()]
            self.creatures[creature_id] = Creature(creature_id, color, _type)

    def readline(self):
        return (input())

    def loop(self):
        while True:
            # # # # # # # # # # # # # # # # # # # #
            #
            # # # # # # # # # # # # # # # # # # # #
            self.setMyScore(int(self.readline()))
            self.setFoeScore(int(self.readline()))
            self.setMyScanCount(int(self.readline()))
            for i in range(self.getMyScanCount()):
                self.creatures[int(self.readline())].setScanned(True)
            self.setFoeScanCount(int(self.readline()))
            for i in range(self.getFoeScanCount()):
                self.creatures[int(self.readline())].setFoeScanned(True)
            self.setMyDroneCount(int(self.readline()))
            for i in range(self.getMyDroneCount()):
                drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in self.readline().split()]
                if self.my_drones[i] == None:
                    self.my_drones[i] = Drone(drone_id, drone_x, drone_y, emergency, battery)
                else:
                    self.my_drones[i](drone_id, drone_x, drone_y, emergency, battery)
            self.setFoeDroneCount(int(self.readline()))
            for i in range(self.getFoeDroneCount()):
                if self.foe_drones[i] == None:
                    self.foe_drones[i] = Drone(drone_id, drone_x, drone_y, emergency, battery)
                else:
                    self.foe_drones[i](drone_id, drone_x, drone_y, emergency, battery)
            self.setDroneScanCount(int(self.readline()))

            for i in range(drone_scan_count):
                drone_id, creature_id = [int(j) for j in self.readline().split()]
                self.creatures[creature_id].setScannerId(drone_id)
            self.visible_creatures = []
            self.setVisibleCreatureCount(int(self.readline()))
            for i in range(self.getVisibleCreatureCount()):
                creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in self.readline().split()]
                self.visible_creatures[creature_id] = self.creatures[creature_id]
                self.visible_creatures[creature_id].setX(creature_x)
                self.visible_creatures[creature_id].setY(creature_y)
                self.visible_creatures[creature_id].setXVelocity(creature_vx)
                self.visible_creatures[creature_id].setYVelocity(creature_vy)
            self.setRadarBlipCount(int(self.readline()))

            for i in range(len(self.my_drones)):
                self.my_drones[i].clearRdar()

            for i in range(self.getRadarBlipCount()):
                inputs      = self.readline().split()
                drone_id    = int(inputs[0])
                creature_id = int(inputs[1])
                radar       = inputs[2]
                for p in range(len(self.my_drones)):
                    if (self.my_drones[i].getId() == drone_id):
                        self.my_drones[i].addRdarTeget()

                    self.my_drones[i].clearRdar()
                    self.creatures[creature_id].setRadarInfo(drone_id, radar)

    for i in range(my_drone_count):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # MOVE <x> <y> <light (1|0)> | WAIT <light (1|0)>
        print("WAIT 1")
