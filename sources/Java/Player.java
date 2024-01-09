package fr.tcordel.model;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class Player {

	static GameEstimator gameEstimator = new GameEstimator();
	static Game game = new Game();
	static DownAndUp downAndUp = new DownAndUp(game);

	public static Set<Scan> ALL_SCANS = Arrays.stream(FishType.values())
		.flatMap(fishType -> IntStream.range(0, Game.COLORS_PER_FISH).mapToObj(i -> new Scan(fishType, i)))
		.collect(Collectors.toSet());

	public static Set<Scan> ALL_AVAILABLE_SCANS = Arrays.stream(FishType.values())
		.flatMap(fishType -> IntStream.range(0, Game.COLORS_PER_FISH).mapToObj(i -> new Scan(fishType, i)))
		.collect(Collectors.toSet());
	public static boolean FIRST_ROUND = true;
	public static int ROUND = 0;

	public static void main(String args[]) {
		Scanner in = new Scanner(System.in);
		int creatureCount = in.nextInt();
		game.fishes = new ArrayList<>(creatureCount);
		game.uglies = new ArrayList<>(creatureCount);
		Set<Integer> scans = new HashSet<>();
		game.visibleFishes = new ArrayList<>();
		game.visibleUglies = new ArrayList<>();
		Set<Integer> myDonesId = new HashSet<>();


		Map<Integer, Integer> droneIdToIndex = new HashMap<>();

		for (int i = 0; i < creatureCount; i++) {
			int creatureId = in.nextInt();
			int color = in.nextInt();
			int type = in.nextInt();
			if (type >= 0) {
				Fish fish = new Fish(creatureId, color, FishType.values()[type]);
				game.fishesMap.put(creatureId, fish);
				game.fishes.add(fish);
			} else {
				Ugly ugly = new Ugly(creatureId);
				game.uglies.add(ugly);
				game.ugliesMap.put(creatureId, ugly);
			}
		}
		Map<Integer, Radar> radars = new HashMap<>();
		List<Vector>[] targets = new List[] {
			List.of(
				new Vector(2500, 9000),
				new Vector(2500, 0)
			), List.of(
				new Vector(7500, 9000),
				new Vector(7500, 0)
			)};
		int[] targetIndex = new int[] {0, 0};
		GamePlayer me = new GamePlayer();
		me.setIIndex(GamePlayer.ME);
		GamePlayer foe = new GamePlayer();
		foe.setIIndex(GamePlayer.FOE);
		game.gamePlayers = List.of(me, foe);
		Set<Integer> allIds = new HashSet<>();

		Set<Scan> myCommit = new HashSet<>();
		Set<Scan> foeCommit = new HashSet<>();
		// game loop
		while (true) {
			int myScore = in.nextInt();
			game.gamePlayers.get(0).setScore(myScore);
			int foeScore = in.nextInt();
			game.gamePlayers.get(1).setScore(foeScore);

			myCommit.clear();
			foeCommit.clear();
			int myScanCount = in.nextInt();
			scans.clear();
			game.visibleFishes.clear();
			game.visibleUglies.clear();

			game.gamePlayers.get(0).scans.clear();

			for (int i = 0; i < myScanCount; i++) {
				int creatureId = in.nextInt();
				Scan e = new Scan(game.fishesMap.get(creatureId));
				if (game.gamePlayers.get(0).scans.add(e)) {
					myCommit.add(e);
				}
				scans.add(creatureId);
			}
			int foeScanCount = in.nextInt();
			game.gamePlayers.get(1).scans.clear();
			for (int i = 0; i < foeScanCount; i++) {
				int creatureId = in.nextInt();
				Scan e = new Scan(game.fishesMap.get(creatureId));
				if (game.gamePlayers.get(1).scans.add(e)) {
					foeCommit.add(e);
				}
			}

			gameEstimator.commit(myCommit, foeCommit);
			int myDroneCount = in.nextInt();
			game.dronesMap.values().forEach(Drone::resetRadars);
			int lastDroneX = 0;
			for (int i = 0; i < myDroneCount; i++) {
				int droneId = in.nextInt();
				int droneX = in.nextInt();
				int droneY = in.nextInt();
				int emergency = in.nextInt();
				int battery = in.nextInt();
				if (i == 1) {
					if (downAndUp.leftIndex == 0) {
						if (droneX < (lastDroneX + 100)) {
							downAndUp.leftIndex = 1;
						}
					} else {
						if (lastDroneX < (droneX + 100)) {
							downAndUp.leftIndex = 0;
						}
					}
				}
				if (FIRST_ROUND) {
					radars.put(droneId, new Radar());
					myDonesId.add(droneId);
					if (i == 0 && droneX > (Game.WIDTH / 2)) {
						System.err.println("switching targets " + droneId + ", " + droneX);
						List<Vector> tmp = targets[0];
						targets[0] = targets[1];
						targets[1] = tmp;
					}
					Drone drone = new Drone(droneX, droneY, droneId, game.gamePlayers.get(0));
					game.gamePlayers.get(0).drones.add(drone);
					game.dronesMap.put(droneId, drone);
					droneIdToIndex.put(droneId, i);
				}

				Drone drone = game.gamePlayers.get(0).drones.get(i);
				refreshDrone(drone, droneX, droneY, emergency, battery);
				lastDroneX = droneX;
			}
			radars.values().forEach(Radar::reset);

			int foeDroneCount = in.nextInt();
			for (int i = 0; i < foeDroneCount; i++) {
				int droneId = in.nextInt();
				int droneX = in.nextInt();
				int droneY = in.nextInt();
				int emergency = in.nextInt();
				int battery = in.nextInt();
				if (FIRST_ROUND) {
					Drone drone = new Drone(droneX, droneY, droneId, game.gamePlayers.get(1));
					game.gamePlayers.get(1).drones.add(drone);
					game.dronesMap.put(droneId, drone);
				}
				Drone drone = game.gamePlayers.get(1).drones.get(i);
				refreshDrone(drone, droneX, droneY, emergency, battery);
			}

			if (!FIRST_ROUND) {
				game.performGameUpdate(ROUND);
			}

			game.dronesMap.values()
				.forEach(drone -> {
					drone.pos = drone.move;
					drone.move = null;
				});


			int droneScanCount = in.nextInt();
			game.dronesMap.values().forEach(drone -> drone.scans.clear());
			for (int i = 0; i < droneScanCount; i++) {
				int droneId = in.nextInt();
				int creatureId = in.nextInt();
//				System.err.println("Scanned " + droneId + "-" + creatureId);
				Scan e = new Scan(game.fishesMap.get(creatureId));
				game.dronesMap.get(droneId).scans.add(e);
				if (myDonesId.contains(droneId)) {
					scans.add(creatureId);
				}
			}
			int visibleCreatureCount = in.nextInt();
			for (int i = 0; i < visibleCreatureCount; i++) {
				int creatureId = in.nextInt();
				int creatureX = in.nextInt();
				int creatureY = in.nextInt();
				int creatureVx = in.nextInt();
				int creatureVy = in.nextInt();
				Vector pos = new Vector(creatureX, creatureY);
				Vector speed = new Vector(creatureVx, creatureVy);
				if (game.fishesMap.containsKey(creatureId)) {
					Fish fish = game.fishesMap.get(creatureId);

					fish.pos = pos;
					fish.speed = speed;
					fish.lastSeenTurn = ROUND;
					game.visibleFishes.add(fish);
				} else if (game.ugliesMap.containsKey(creatureId)) {
					Ugly ugly = game.ugliesMap.get(creatureId);
					System.err.println("Ugly " + creatureId + "@" + pos + "," + speed);
					if (ROUND < 200 && creatureVx == 0 && creatureVy == 0) { // todo : revert processing position retrieval
						int oppCreatureId = creatureId + (creatureId % 2 == 0 ? 1 : -1);
						Ugly ugly1 = game.ugliesMap.get(oppCreatureId);
						if (ugly1 != null && ugly1.pos == null) {
							ugly1.pos = pos.hsymmetric(Game.CENTER.getX());
							System.err.println("Estimated oppUgly " + oppCreatureId + " location " + ugly1.pos);
						}
					}
					ugly.pos = pos;
					ugly.speed = speed;
					game.visibleUglies.add(ugly);
				}
			}
			int radarBlipCount = in.nextInt();

			ALL_AVAILABLE_SCANS.clear();
			allIds.clear();
			for (int i = 0; i < radarBlipCount; i++) {
				int droneId = in.nextInt();
				int creatureId = in.nextInt();
				String radar = in.next();
//				System.err.println(droneId + " -> " + creatureId + " @ " + radar);
				RadarDirection radarDirection = RadarDirection.valueOf(radar);
				allIds.add(creatureId);
				if (game.fishesMap.containsKey(creatureId)) {
					ALL_AVAILABLE_SCANS.add(new Scan(game.fishesMap.get(creatureId)));
				}
				if (!scans.contains(creatureId)) {
					radars.get(droneId).populate(creatureId, radarDirection);
				}
				game.dronesMap.get(droneId).getRadar().put(creatureId, radarDirection);
			}

			if (Player.FIRST_ROUND) {
				Drone drone0 = game.gamePlayers.get(GamePlayer.ME).drones.get(0);
				Drone drone1 = game.gamePlayers.get(GamePlayer.ME).drones.get(1);
				boolean drone0isLeft = drone1.getX() > drone0.getX();

				Drone droneLeft = drone0isLeft ? drone0 : drone1;
				Drone droneRight = !drone0isLeft ? drone0 : drone1;
				boolean droneLeftExternal = droneLeft.pos.getX() < 3000;
				droneLeft.initialPosition = droneLeftExternal ? DroneInitialPosition.EXTERNAL : DroneInitialPosition.INNER;
				droneRight.initialPosition = !droneLeftExternal ? DroneInitialPosition.EXTERNAL : DroneInitialPosition.INNER;

				Radar radarDroneLeft = radars.get(droneLeft.id);
				Radar radarDroneRight = radars.get(droneRight.id);

//				System.err.println("Analyzing map");
				for (int i = 4; i <= 14; i = i+2) {
					int currId = i;
					int oppId = i + 1;
					Fish fish = game.fishesMap.get(i);
					Fish oppfish = game.fishesMap.get(oppId);
//					System.err.printf("%nDuo %d - %d, c %d, t %s%n", i, oppId,fish.color, fish.getType());

					RadarDirection leftToCurDir = radarDroneLeft.forFish(currId);
					RadarDirection rightToOppDir = radarDroneRight.forFish(oppId);
					RadarDirection leftToOppDir = radarDroneLeft.forFish(oppId);
					RadarDirection rightToCurDir = radarDroneRight.forFish(currId);

//					System.err.printf("Trying to estimate %d zone%n", currId);

					RadarDirection leftFoeToCurDir = rightToOppDir.hsymettric();
					RadarDirection rightFoeToCurDir = leftToOppDir.hsymettric();

					List<RadarDirection> directions = List.of(leftToCurDir, leftFoeToCurDir, rightToCurDir, rightFoeToCurDir);
					RadarZone rz;
					if (directions.stream().distinct().count() == 1) {
						rz = RadarZone.EXTERNAL;

						if (leftToCurDir == RadarDirection.BR) {
							droneRight.allocations.put(currId, fish);
							droneLeft.allocations.put(oppId, oppfish);
						} else {
							droneLeft.allocations.put(currId, fish);
							droneRight.allocations.put(oppId, oppfish);
						}
					} else if ((directions.stream().filter(d -> d == RadarDirection.BR).count() %2) == 1) {
						rz = RadarZone.CENTRAL;
						if (droneLeft.initialPosition == DroneInitialPosition.EXTERNAL) {
							boolean alone = Stream.of(leftFoeToCurDir, rightToCurDir, rightFoeToCurDir).noneMatch(a -> a == leftToCurDir);
//							System.err.println("DroneLeft seet it at " + leftToCurDir + "alone ? " + alone);
							if (alone) {
								droneLeft.allocations.put(currId, fish);
								droneRight.allocations.put(oppId, oppfish);
							} else {
								droneRight.allocations.put(currId, fish);
								droneLeft.allocations.put(oppId, oppfish);
							}
						} else {
							boolean alone = Stream.of(leftFoeToCurDir, leftToCurDir, rightFoeToCurDir).noneMatch(a -> a == rightToCurDir);
//							System.err.println("DroneRight seet it at " + rightToCurDir + "alone ? " + alone);
							if (alone) {
								droneRight.allocations.put(currId, fish);
								droneLeft.allocations.put(oppId, oppfish);
							} else {
								droneLeft.allocations.put(currId, fish);
								droneRight.allocations.put(oppId, oppfish);
							}
						}

					} else {
						rz = RadarZone.INNER;
						// Arbitrary allocation
						droneLeft.allocations.put(currId, fish);
						droneRight.allocations.put(oppId, oppfish);
					}
					fish.radarZone = rz;
					oppfish.radarZone = rz;
				}

//				System.err.println("Drone left " + droneLeft.id + " has fish " + droneLeft.allocations.stream().map(Fish::getId).map(String::valueOf).collect(Collectors.joining(",")));
//				System.err.println("Drone left " + droneRight.id + " has fish " + droneRight.allocations.stream().map(Fish::getId).map(String::valueOf).collect(Collectors.joining(",")));
			}

			game.fishesMap.values().forEach(f -> f.escaped = !allIds.contains(f.id));

			downAndUp.process(radars, scans);
			FIRST_ROUND = false;
			ROUND ++;
		}
	}

	private static void refreshDrone(Drone drone, int droneX, int droneY, int emergency, int battery) {
		drone.move = new Vector(droneX, droneY);
		Vector lastPos = drone.pos;
		drone.pos = new Vector(droneX, droneY);
		if (!FIRST_ROUND) {
			drone.lastSpeed = drone.speed;
			drone.speed = new Vector(lastPos, drone.pos);
		}
		drone.dead = emergency == 1;
		drone.lightOn = battery < drone.battery;
		drone.battery = battery;
		if (drone.id == 0) {
			System.err.println("Drone " + drone.pos + ", " + drone.move + "-" + drone.dead);
		}
	}

}