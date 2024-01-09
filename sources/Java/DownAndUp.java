package fr.tcordel.model;

import java.util.*;
import java.util.Map.Entry;
import java.util.function.Predicate;
import java.util.stream.Collectors;

public class DownAndUp extends AbstractStrat {

	private final AttackFish attackFish;


	public static final boolean FOE_WINNNING_COUNTER_ATTACK_STRAT = true;
	public static final boolean FOE_WINNNING_COMMIT_STRAT = true;
	public static final boolean ATTACK_RESSOURCE_ON_NO_ALLOCATION = true;

	public int leftIndex = 0;


	public DownAndUp(Game game) {
		super(game);
		attackFish = new AttackFish(game);
	}

	boolean[] batterieToogle = new boolean[2];
	boolean commitCalled = false;
	boolean hasCommitted = false;

//	Integer firstWinningIndex = null;

	boolean iWin = false;
	boolean foeWins = false;
//	Map<Integer, Set<Integer>> allocations = new HashMap<>();

	public void process(Map<Integer, Radar> radars, Set<Integer> scans) {
		checkWinningState();
		preAllocate(radars);
		resetCaches();
		Arrays.fill(targets, null);
		for (int i = 0; i < game.gamePlayers.get(GamePlayer.ME).drones.size(); i++) {
			Drone drone = game.gamePlayers.get(GamePlayer.ME).drones.get(i);
			if (drone.strat == Strat.UP && drone.getY() <= Game.DRONE_START_Y) {
				drone.strat = Strat.DOWN;
			}
			Vector vector = drone.strat == Strat.UP ? UP : getVector(radars, scans, i, drone);
//			boolean escaping = checkCollision(drone, vector);
			boolean escaping = checkCollisionDeeper(drone, vector);
			System.out.printf(
				"MOVE %d %d %d %s%s%n", (int)drone.move.getX(),
				(int)drone.move.getY(),
				switchOn(i, drone, radars.get(drone.id), targets[i], escaping),
				(drone.strat == Strat.UP ? "" : ""),
				escaping ? "" : ""
								);
		}
	}

	private void resetCaches() {
		for (Drone drone : game.gamePlayers.get(GamePlayer.ME)
			.drones) {
			if (drone.target != null && (
				!drone.getRadar().containsKey(drone.target.id)
				|| game.gamePlayers.get(GamePlayer.FOE).scans.contains(new Scan(drone.target))
				|| game.gamePlayers.get(GamePlayer.FOE).drones.stream().anyMatch(d -> d.scans.contains(new Scan(drone.target)))
			)) {
				drone.target = null;
			}
		}
	}

	private void checkWinningState() {
//		if (game.gamePlayers.get(GamePlayer.ME).getScore() > 0 ||
//			game.gamePlayers.get(GamePlayer.FOE).getScore() > 0 ) {
//			System.err.println("No winning state SCORE");
//			return;
//		}
//
//		if (game.gamePlayers.get(GamePlayer.ME).drones.stream().anyMatch(drone -> drone.strat == Strat.ATTACK)) {
//			System.err.println("No winning state ATTACK");
//			return;
//		}

		// Si je commit avant l'autre :
		// point bonus  moi
		// estimer la perte potentiel de point bonus (premier + combo) pour l'advesaire.

		// --> le reste ne permet pas de rattraper les données commit + bonus + le reste à récupérer.

		// mon score commit premier + reste potentiel second > reste potentiel premier pour l'autre.


		boolean foeCommitting = game.gamePlayers
			.get(GamePlayer.FOE)
			.drones
			.stream()
			.peek(drone -> System.err.println("Speed " + drone.id + " -> " + drone.isCommitting()))
			.allMatch(Drone::isCommitting);




		Set<Scan> scans = game.gamePlayers.get(GamePlayer.ME).drones.stream().flatMap(drone -> drone.scans.stream())
			.collect(Collectors.toSet());
		Set<Scan> scansFoe = game.gamePlayers.get(GamePlayer.FOE).drones.stream().flatMap(drone -> drone.scans.stream())
			.collect(Collectors.toSet());
		GameEstimator gameEstimator = Player.gameEstimator.clone();
		int myCommitPoint = gameEstimator.computeScanScore(scans, game.gamePlayers.get(GamePlayer.ME).getIndex());
//		gameEstimator.computeScanScore(scansFoe, game.gamePlayers.get(GamePlayer.FOE).getIndex());
		int oppMaxScore = gameEstimator.computeFullEndGameScore(game.gamePlayers.get(GamePlayer.FOE));
		int myScoreCommittingFirst = gameEstimator.computeFullEndGameScore(game.gamePlayers.get(GamePlayer.ME));

		gameEstimator = Player.gameEstimator.clone();
		int himCommintPoint = gameEstimator.computeScanScore(scansFoe, game.gamePlayers.get(GamePlayer.FOE).getIndex());
//		gameEstimator.computeScanScore(scans, game.gamePlayers.get(GamePlayer.ME).getIndex());
		int myScoreCommittingFirst2 = gameEstimator.computeFullEndGameScore(game.gamePlayers.get(GamePlayer.ME));
		int oppMaxScore2 = gameEstimator.computeFullEndGameScore(game.gamePlayers.get(GamePlayer.FOE));


		game.gamePlayers.get(GamePlayer.ME)
			.drones
			.forEach(d -> d.strat = Strat.DOWN);

		Map<Integer, List<Drone>> list = game.gamePlayers
			.stream()
			.flatMap(g -> g.drones.stream())
			.filter(d -> !d.scans.isEmpty())
			.collect(Collectors.toMap(a -> (int) Math.ceil((a.getY() - Game.DRONE_START_Y) / Game.DRONE_MOVE_SPEED), drone -> {
					List<Drone> arrayList = new ArrayList<>();
					arrayList.add(drone);
					return arrayList;
				}, (a, b) -> {
					a.addAll(b);
					return a;
				},
				TreeMap::new));



//		boolean iWillCommitFirst = !foeCommitting ||
//								   game.gamePlayers
//									   .get(GamePlayer.ME)
//									   .drones.stream()
//									   .map(d -> d.pos)
//									   .anyMatch(p -> p.getX() <= (Game.DRONE_MOVE_SPEED / 2) + game.gamePlayers
//										   .get(GamePlayer.FOE)
//										   .drones.stream()
//										   .map(d -> d.pos)
//										   .mapToDouble(Vector::getX)
//										   .min().orElse(Double.MAX_VALUE));
//		iWin = myCommitPoint >= oppMaxScore;
		foeWins = oppMaxScore2 >= myScoreCommittingFirst2;
//		if (firstWinningIndex == null) {
//			if (iWin) {
//				firstWinningIndex = GamePlayer.ME;
//			} else if (foeWins) {
//				firstWinningIndex = GamePlayer.FOE;
//			}
//		}

		GameEstimator gameEstimatorFinal = Player.gameEstimator.clone();
		list.forEach((key1, drones) -> {
			Set<Scan> myScans = drones.stream().filter(d -> d.getOwner().getIndex() == 0)
				.flatMap(drone -> drone.scans.stream())
				.collect(Collectors.toSet());
			Set<Scan> oppScans = drones.stream().filter(d -> d.getOwner().getIndex() == 1 && d.isCommitting())
				.flatMap(drone -> drone.scans.stream())
				.collect(Collectors.toSet());
			gameEstimatorFinal.commit(myScans, oppScans);
		});

		int myHitPointPondered = gameEstimatorFinal.getScore(GamePlayer.ME);
		int oppMaxScorePondered = gameEstimatorFinal.computeFullEndGameScore(game.gamePlayers.get(GamePlayer.FOE));
		int meMaxScorePondered = gameEstimatorFinal.computeFullEndGameScore(game.gamePlayers.get(GamePlayer.ME));
		iWin = myHitPointPondered >= oppMaxScorePondered;

		if (isWinning(GamePlayer.ME)) {
			game.gamePlayers.get(GamePlayer.ME)
				.drones
				.stream()
				.filter(d -> !d.scans.isEmpty())
				.forEach(d -> {
//					Drone opposite = game.getFoeFor(d.id);
//					boolean foeCom = opposite.isCommitting();
//					int myTurnToCommit = (int)Math.ceil((d.getY() - Game.DRONE_START_Y) / Game.DRONE_MOVE_SPEED);
//					int oppTurnToCommit = (int)Math.ceil((opposite.getY() - Game.DRONE_START_Y) / Game.DRONE_MOVE_SPEED);
//					System.err.printf("D %d Foe %d committing %b, turn %d vs %d %n", d.id, opposite.id, foeCom, myTurnToCommit, oppTurnToCommit);
//					if (!foeCom || myTurnToCommit <= oppTurnToCommit) {
						d.strat = Strat.UP;
//					}
				});
		}

//		if (FOE_WINNNING_COMMIT_STRAT && himCommintPoint > myScoreCommittingFirst2) {
//			System.err.println("OPP can win :("); // bug vs bot seed=7773864893213486000
//			GameEstimator gameEstimatorFinal2 = Player.gameEstimator.clone();
//			list.forEach((key1, drones) -> {
//				Set<Scan> myScans = drones.stream().filter(d -> d.getOwner().getIndex() == 0)
//					.flatMap(drone -> drone.scans.stream())
//					.collect(Collectors.toSet());
//				Set<Scan> oppScans = drones.stream().filter(d -> d.getOwner().getIndex() == 1)
//					.flatMap(drone -> drone.scans.stream())
//					.collect(Collectors.toSet());
//				gameEstimatorFinal2.commit(myScans, oppScans);
//			});
//			int myScore = gameEstimatorFinal2.computeFullEndGameScore(game.gamePlayers.get(GamePlayer.ME));
//			int foeScore = gameEstimatorFinal2.computeFullEndGameScore(game.gamePlayers.get(GamePlayer.FOE));
//
//			if (myScore >= foeScore) {
//				System.err.println("Rushing toward surface %d vs %d".formatted(myScore, foeScore));
//
//				int ennemyCount = 0;
//				for (Entry<Integer, List<Drone>> entry : list.entrySet()) {
//					if (ennemyCount == 2) {
//						System.err.println("Stopping counter cause all ennemy are before me");
//						break;
//					}
//					for (Drone drone : entry.getValue()) {
//						if (drone.getOwner().getIndex() == GamePlayer.FOE) {
//							ennemyCount ++;
//						} else {
//							System.err.println("Countering with drone " + drone.id);
//							drone.strat = Strat.UP;
//						}
//					}
//				}
//			} else {
//				System.err.println("OPP will win :( %d vs %d".formatted(myScore, foeScore));
//			}
//		}

//		if (FOE_WINNNING_COUNTER_ATTACK_STRAT && isWinning(GamePlayer.FOE)) {
//			System.err.println("Loosing, so attacking whatever i can");
//			game.gamePlayers.get(GamePlayer.ME).drones
//				.stream()
//				.filter(drone -> drone.strat != Strat.UP)
//				.forEach(drone -> drone.strat = Strat.ATTACK);
//		}



	}

	private boolean isWinning(int index) {
		return index == GamePlayer.ME ? iWin : foeWins;
	}

	private int switchOn(int i, Drone drone, Radar radar, FishType target, boolean escaping) {
		boolean lightOn = false;
		game.updateDrone(drone);
		boolean isUnknownUgly = game.uglies.stream().anyMatch(ugly -> ugly.pos == null);
		boolean needLight = isUnknownUgly
							|| drone.allocations.values().stream().anyMatch(fish -> fish.pos == null)
							|| drone.allocations.values().stream().anyMatch(fish -> {
			Scan scan = new Scan(fish);
			if (drone.scans.contains(scan) || game.gamePlayers.get(GamePlayer.ME).scans.contains(scan)) {
					return false;
				}
			double distance = drone.move.distance(fish.pos);
			return distance > (Game.DARK_SCAN_RANGE - Game.FISH_FLEE_SPEED)
				   && distance < (Game.LIGHT_SCAN_RANGE);
		});
		if (drone.strat == Strat.ATTACK) {
			lightOn = ((drone.target != null
					  && drone.target.pos == null
						&& isInRange(drone, Set.of(drone.target.type))) || isUnknownUgly)
					  && !batterieToogle[i];
		} else {
			if (
				//			!escaping&&
				drone.move.getY() >= FishType.JELLY.getUpperLimit()
				&& (!batterieToogle[i] || (drone.getY() > 6500))
				&& (isInRange(drone, radar.getTypes(drone.allocations)) || isUnknownUgly || (target == FishType.CRAB && (drone.getY() > 6500)))
				&& needLight
			) {
				lightOn = true;
			}
		}
		batterieToogle[i] = lightOn;
		return lightOn ? 1 : 0;
	}

	private boolean isInRange(Drone drone, Set<FishType> target) {
		FishType zoneType = FishType.forY(drone.move.getY(), game.getMoveSpeed(drone) / 2);
		if (zoneType == null) {
			return false;
		}
		return target.stream().anyMatch(fishType -> fishType.equals(zoneType));
//		return drone.getY() >= 3000;
	}

	private void preAllocate(Map<Integer, Radar> radars) {

//		game.gamePlayers.get(GamePlayer.ME).drones
//			.forEach(d -> allocations.put(d.id, new HashSet<>()));
//
//		Drone drone0 = game.gamePlayers.get(GamePlayer.ME).drones.get(0);
//		Drone drone1 = game.gamePlayers.get(GamePlayer.ME).drones.get(1);
//
//		boolean splitHoriz = Math.abs(drone1.getX() - drone0.getX()) >= 1000;
//		boolean splitVert = Math.abs(drone1.getY() - drone0.getY()) >= 1000;
//		boolean drone0isLeft = drone1.getX() > drone0.getX();
//		boolean drone0isUp = drone1.getY() > drone0.getY();
//
//
//		Radar drone0radar = radars.get(drone0.id);
//		Radar drone1radar = radars.get(drone1.id);
//		if (splitHoriz) {
//			allocations.get(drone0.id).addAll(drone0isLeft ? drone0radar.topLeft : drone0radar.topRight);
//			allocations.get(drone0.id).addAll(drone0isLeft ? drone0radar.bottomLeft : drone0radar.bottomRight);
//			allocations.get(drone1.id).addAll(!drone0isLeft ? drone1radar.topLeft : drone1radar.topRight);
//			allocations.get(drone1.id).addAll(!drone0isLeft ? drone1radar.bottomLeft : drone1radar.bottomRight);
//		}
//
//		if (splitVert) {
//			allocations.get(drone0.id).addAll(drone0isUp ? drone0radar.topLeft : drone0radar.bottomLeft);
//			allocations.get(drone0.id).addAll(drone0isUp ? drone0radar.topRight : drone0radar.bottomRight);
//			allocations.get(drone1.id).addAll(!drone0isUp ? drone1radar.topLeft : drone1radar.bottomLeft);
//			allocations.get(drone1.id).addAll(!drone0isUp ? drone1radar.topRight : drone1radar.bottomRight);
//		}

	}

	/**
	 * seed=5865112135755987000 vs boss
	 * @param drone
	 * @param vector
	 * @return
	 */
	public boolean checkCollision(Drone drone, Vector vector) {
//
//		for (int i = 0; i < 360; i++) {
//			int offset = (i % 2 > 0 ? 1 : -1) * (i / 2);
//			if (moveAndCheckNoCollision(drone, vector, offset, true, 80))
//				return i > 0;
//		}

		for (int i = 0; i < 360; i++) {
			int offset = (i % 2 > 0 ? 1 : -1) * (i / 2);
			if (moveAndCheckNoCollision(drone, vector, offset, true, 0))
				return i > 0;
		}
		Optional<Ugly> min = game.uglies
			.stream()
			.filter(ugly -> ugly.pos != null)
			.min(Comparator.comparingDouble(u -> u.pos.manhattanTo(drone.pos)));
		if (min.isPresent()) {
			Ugly ugly = min.get();
			Vector normalize = ugly.speed.normalize().mult(Game.DRONE_MOVE_SPEED).round();
			drone.move = drone.pos.add(normalize);
		} else {
			drone.move = drone.pos.add(vector);
		}
		return true;
	}

	public boolean checkCollisionDeeper(Drone drone, Vector vector) {
		List<Ugly> conflicting = game.uglies
			.stream()
			.filter(u -> u.pos != null)
			.filter(u -> u.pos.inRange(drone.pos, 2 * (Game.DRONE_MOVE_SPEED + Game.UGLY_ATTACK_SPEED)))
			.toList();

		Vector dronePosition = drone.pos;
		Vector droneMove = game.snapToDroneZone(dronePosition.add(vector));

		if (conflicting.isEmpty()) {
			drone.move = droneMove;
			return false;
		}


		int i = 0;
		main:
		for (; i < 360; i++) {
			int offset = (i % 2 > 0 ? 1 : -1) * (i / 2);

			Vector rotate = vector.rotate(offset * _1DegToRadians);
			Vector rotateNormalized = rotate.normalize().mult(Game.DRONE_MOVE_SPEED).round();
			droneMove = game.snapToDroneZone(dronePosition.add(rotate).round());
			Vector droneSpeed = game.getDroneSpeed(dronePosition, droneMove);

			for (Ugly ugly : conflicting) {
				if (game.getCollision2(dronePosition, droneSpeed, ugly.pos, ugly.speed)) {
					continue main;
				}
			}

			int j = 0;
			inner:
			for (; j < 25; j++) {
				int offset2 = (j % 2 > 0 ? 1 : -1) * (j / 2);
				Vector secondMove = game.snapToDroneZone(droneMove.add(rotateNormalized.rotate(offset2 * _15DegToRadians)).round());
				Vector secondSpeed = game.getDroneSpeed(droneMove, secondMove);

				for (Ugly ugly : conflicting) {
					if (ugly.speed.length() > 0) {
//						continue;
					}
					Vector newPosition = game.snapToUglyZone(ugly.pos.add(ugly.speed));
					Vector attackVec = new Vector(newPosition, droneMove);
					if (attackVec.length() > Game.LIGHT_SCAN_RANGE) {
						continue;
					}
					if (attackVec.length() > Game.UGLY_ATTACK_SPEED) {
						attackVec = attackVec.normalize().mult(Game.UGLY_ATTACK_SPEED);
					}
					attackVec = attackVec.round();
//					System.err.println("AttackVec " + ugly.id + " " + newPosition +" - "+ attackVec + " with drone at " + droneMove );

					if (game.getCollision2(droneMove, secondSpeed, newPosition, attackVec)) {
						continue inner;
					}
				}
				break;
			}

			if (j == 25) {
				System.err.println("Second step collision detected");
				continue;
			}
			//			if (game.uglies
//				.stream()
//				.filter(ugly -> ugly.pos != null)
//				.noneMatch(u -> game.getCollision(drone, u, offset))) {
			break;
		}
		drone.move = droneMove;
		return i > 0;
	}

	FishType[] targets = new FishType[2];

	private Vector getVector(Map<Integer, Radar> radars, Set<Integer> scans, int i, Drone drone) {
		Radar radarForDrone = radars.get(drone.id);
		boolean isLeft = leftIndex == i;

		Vector direction = null;

		if (drone.strat == Strat.ATTACK) {
			direction = applyAttackStrat(drone, isLeft);
		}
		if (direction != null) {
			return direction;
		}

		RadarDirection rd = null;
		Radar radarForType;
		FishType target = null;

//
//		if (fishToAttack.isPresent()) {
//			direction = applyAttackStrat(drone, isLeft);
//			if (direction != null) {
//				return direction;
//			}
//		}


		for (FishType fishType : FishType.FISH_ORDERED) {
			radarForType = radarForDrone.forType(game.fishesMap, fishType);
			target = fishType;
			RadarDirection radarDirection = isLeft ? RadarDirection.BL : RadarDirection.BR;
			rd = checkForType(drone.allocations, isLeft ? radarForType.bottomLeft : radarForType.bottomRight, radarDirection);
			if (rd != null) {
				System.err.println(radarDirection + " for " + drone.id + " aiming for " + fishType);
				break;
			}
			radarDirection = !isLeft ? RadarDirection.BL : RadarDirection.BR;
			rd = checkForType(drone.allocations, !isLeft ? radarForType.bottomLeft : radarForType.bottomRight, radarDirection);
			if (rd != null) {
				System.err.println(radarDirection + " for " + drone.id + " aiming for " + fishType);
				break;
			}
			radarDirection = isLeft ? RadarDirection.TL : RadarDirection.TR;
			rd = checkForType(drone.allocations, isLeft ? radarForType.topLeft : radarForType.topRight, radarDirection);
			if (rd != null) {
				System.err.println(radarDirection + " for " + drone.id + " aiming for " + fishType);
				break;
			}
			radarDirection = !isLeft ? RadarDirection.TL : RadarDirection.TR;
			rd = checkForType(drone.allocations, !isLeft ? radarForType.topLeft : radarForType.topRight, radarDirection);
			if (rd != null) {
				System.err.println(radarDirection + " for " + drone.id + " aiming for " + fishType);
				break;
			}
		}

		if (rd == null) {
			if ( (ATTACK_RESSOURCE_ON_NO_ALLOCATION)
				|| (FOE_WINNNING_COUNTER_ATTACK_STRAT && isWinning(GamePlayer.FOE))) {
				direction = applyAttackStrat(drone, isLeft);
				if (direction != null) {
					return direction;
				}
			}
			return UP;
		}

		targets[i] = target;

		RadarDirection finalRd = rd;
		Predicate<Fish> sameDirection = f -> isWinning(GamePlayer.FOE) || switch (finalRd) {
			case BL, BR ->f.pos.getY() >= drone.pos.getY();
			case TL, TR ->f.pos.getY() <= drone.pos.getY();
		};
		Optional<Fish> fishToAttack = drone.scans.stream()
			.filter(scan ->  game.gamePlayers.get(GamePlayer.FOE).drones.stream().noneMatch(opp -> opp.scans.contains(scan)))
			.map(scan -> game.fishesMap.get(scan.fishId))
			.filter(f -> !f.escaped && f.pos != null)
			.filter(fish -> isLeft ? (fish.getX() < Game.FISH_FLEE_SPEED * 2) : (fish.getX() > (Game.WIDTH - Game.FISH_FLEE_SPEED * 2)))
			.filter(fish -> fish.pos.euclideanTo(drone.pos) < (Game.FISH_HEARING_RANGE + Game.DRONE_MOVE_SPEED))
			.filter(fish -> game.gamePlayers.get(GamePlayer.FOE).drones.stream()
				.allMatch(opp -> fish.pos.euclideanTo(opp.pos) > (Game.LIGHT_SCAN_RANGE + Game.DRONE_MOVE_SPEED - Game.FISH_FLEE_SPEED)))
			.filter(sameDirection)
			.findFirst();

		if (fishToAttack.isPresent()) {
			System.err.printf("Drone %d may attack %d", drone.id, fishToAttack.get().id);
			return attackFish.process(fishToAttack.get(), drone);
		}
		int threshold = game.getMoveSpeed(drone);
		if ((drone.getY() - threshold) >= target.getDeeperLimit() || (drone.getY() + threshold) <= target.getUpperLimit()) {
			FishType fishType = FishType.forY(drone.getY(), 0);
			System.err.println(drone.getId() + " depth too far from target type " + target + "... " + drone.getY() + "at zone" + fishType);
//			FishType nextZone = switch (rd) {
//			 case BL, BR ->FishType.deeper(fishType);
//			 case TL, TR ->FishType.upper(fishType);
//			};
//
//			if (nextZone != null
//				&& nextZone != target
//				&& (rd == RadarDirection.BR || rd == RadarDirection.BL)
//				&& drone.allocations.values().stream().anyMatch(f -> f.getType() == nextZone
//																	 && !drone.scans.contains(new Scan(f))
//																	 && f.radarZone == RadarZone.EXTERNAL)) {
//
//				if (isLeft) {
//					if (drone.getX() >= 2100) {
//						System.err.println("Spotted External Fish in next zone, aim for it" + drone.id);
//						return DOWN_BIG_LEFT;
//					}
//				} else {
//					if (drone.getX() < 7900) {
//						System.err.println("Spotted External Fish in next zone, aim for it" + drone.id);
//						return DOWN_BIG_RIGHT;
//					}
//				}
//			}
			return switch (rd) {
				case BL -> drone.getX() > Game.FISH_HEARING_RANGE ? DOWN_LEFT : DOWN;
				case BR -> drone.getX() < (Game.WIDTH - Game.FISH_HEARING_RANGE) ? DOWN_RIGHT : DOWN;
//				case BL, BR -> DOWN;
				case TL, TR -> UP;
			};
		}


//		boolean goToCenter = isLeft;
		//		List<Integer> integers = isLeft ? radar.bottomLeft : radar.bottomRight;
		//		for (Integer integer : integers) {
		//			if (game.fishesMap.containsKey(integer)) {
		//				goToCenter = !goToCenter;
		//				break;
		//			}
		//		}
		//		RadarDirection rd = goToCenter ? RadarDirection.BR : RadarDirection.BL;
		direction = getFilteredVector(drone, rd.getDirection(), 400, 400);

		return direction;
	}

	private Vector applyAttackStrat(Drone drone, boolean isLeft) {
		Vector direction = null;
		if (drone.target == null) {
			drone.target = game.fishes.stream()
				.filter(f -> !f.escaped)
				.filter(f -> drone.getRadar().containsKey(f.id))
				.filter(f -> game.gamePlayers.get(GamePlayer.ME).drones.stream().allMatch(d -> d.target != f))
				.filter(f -> !game.gamePlayers.get(GamePlayer.FOE).scans.contains(new Scan(f)))
				.filter(f -> game.gamePlayers.get(GamePlayer.FOE).drones.stream().noneMatch(d -> d.scans.contains(new Scan(f))))
				.sorted(Comparator.comparingDouble((Fish f) -> f.getPos() == null ? Double.MAX_VALUE : f.getPos().manhattanTo(drone.getPos()))
					.thenComparing(f -> -f.getType().ordinal()))
				.findFirst().orElse(null);
		}
		if (drone.target != null) {
			direction = attackFish.process(drone.target, drone);
		}
		if (direction != null) {
			boolean collision = !moveAndCheckNoCollision(drone, direction, 0, true, 0);
			System.err.println("Attacking collision check for drone " + drone.id + ": " + collision);
			if (collision) {
				Vector direction2 = filterDirection(drone, drone.pos.add(direction), direction, 0, Game.HEIGHT);
				System.err.println("Collision ! " + direction + "->" + direction2);
				direction = direction2;
			}
		}
		return direction;
	}

	private Vector getFilteredVector(Drone drone, Vector direction, int xLimit, int yLimit) {
		if (direction == null) {
			return direction;
		}
		Vector vector = drone.pos.add(direction);
		drone.move = game.snapToDroneZone(vector);
		game.updateDrone(drone);
		boolean processFilter = game.uglies
									.stream()
									.filter(ugly -> ugly.pos != null)
									.noneMatch(u -> game.getCollision(drone, u));

		if (!processFilter) {
			System.err.println("Filter border target only for " + drone.id + " due to collision");
			xLimit = 0;
			yLimit = Game.HEIGHT;
		}

		return filterDirection(drone, vector, direction, xLimit, yLimit);
	}

	private RadarDirection checkForType(Map<Integer, Fish> allocations, List<Integer> integers, RadarDirection radarDirection) {
		if (integers.stream()
			.anyMatch(allocations::containsKey)) {
			return radarDirection;
		}
		return null;
	}
}
