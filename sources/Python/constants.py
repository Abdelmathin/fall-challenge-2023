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
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

# [x, y, light]
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

'''
	[seed, fiches]:
		4 : [2551144270460652500]
		5 : [4652432536664612000]
		6 : [9061774830165723000, 2939674589624873500, 8129559243459837000, 2604157575199368700, 5434755661154524000]
'''
