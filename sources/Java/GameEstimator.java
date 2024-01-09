package fr.tcordel.model;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

public class GameEstimator {

	public static int MAX_POINT = 96;

	Set<Scan> allOfMyScans = new HashSet<>();
	Set<Scan> allOfFoeScans = new HashSet<>();
	Map<Scan, Integer> firstToScan = new HashMap<>();
	Map<Integer, Integer> firstToScanAllFishOfColor = new HashMap<>();
	Map<FishType, Integer> firstToScanAllFishOfType = new HashMap<>();

	public int computeScanScore(Set<Scan> scans, int playerIndex) {
		int total = 0;
		for (Scan scan : scans) {
			total += scan.type.ordinal() + 1;
			if (firstToScan.get(scan) == null || firstToScan.get(scan).equals(playerIndex)) {
				firstToScan.put(scan, playerIndex);
				total += scan.type.ordinal() + 1;
			}
		}

		for (FishType type : FishType.values()) {
			if (playerScannedAllFishOfType(scans, type)) {
				total += Game.COLORS_PER_FISH;
				if (Objects.isNull(firstToScanAllFishOfType.get(type))
					|| Objects.equals(firstToScanAllFishOfType.get(type), playerIndex)) {
					firstToScanAllFishOfType.put(type, playerIndex);
					total += Game.COLORS_PER_FISH;
				}
			}
		}

		for (int color = 0; color < Game.COLORS_PER_FISH; ++color) {
			if (playerScannedAllFishOfColor(scans, color)) {
				total += FishType.values().length;
				if (Objects.isNull(firstToScanAllFishOfColor.get(color))
					|| Objects.equals(firstToScanAllFishOfColor.get(color), playerIndex)) {
					firstToScanAllFishOfColor.put(color, playerIndex);
					total += FishType.values().length;
				}
			}
		}
		return total;
	}

	public void commit(Set<Scan> myScans, Set<Scan> foeScans) {
		allOfMyScans.addAll(myScans);
		allOfFoeScans.addAll(foeScans);
		for (Scan scan : Player.ALL_SCANS) {
			if (firstToScan.containsKey(scan)) {
				continue;
			}
			if (myScans.contains(scan) && !foeScans.contains(scan)) {
				firstToScan.put(scan, GamePlayer.ME);
			} else if (foeScans.contains(scan) && !myScans.contains(scan)) {
				firstToScan.put(scan, GamePlayer.FOE);
			}
		}

		for (FishType type : FishType.values()) {
			if (firstToScanAllFishOfType.containsKey(type)) {
				continue;
			}
			boolean iCompleted = playerScannedAllFishOfType(allOfMyScans, type);
			boolean foeCompleted = playerScannedAllFishOfType(allOfFoeScans, type);
			if (iCompleted && !foeCompleted) {
				firstToScanAllFishOfType.put(type, GamePlayer.ME);
			} else if (foeCompleted && !iCompleted) {
				firstToScanAllFishOfType.put(type, GamePlayer.FOE);
			}
		}


		for (int color = 0; color < Game.COLORS_PER_FISH; ++color) {
			if (firstToScanAllFishOfColor.containsKey(color)) {
				continue;
			}
			boolean iCompleted = playerScannedAllFishOfColor(allOfMyScans, color);
			boolean foeCompleted = playerScannedAllFishOfColor(allOfFoeScans, color);
			if (iCompleted && !foeCompleted) {
				firstToScanAllFishOfColor.put(color, GamePlayer.ME);
			} else if (foeCompleted && !iCompleted) {
				firstToScanAllFishOfColor.put(color, GamePlayer.FOE);
			}
		}
	}

	public int getScore(int playerIndex) {
		return switch (playerIndex) {
			case GamePlayer.ME -> computeGameScore(GamePlayer.ME, allOfMyScans);
			case GamePlayer.FOE -> computeGameScore(GamePlayer.FOE, allOfFoeScans);
			default -> throw new IllegalArgumentException("Unexpecrted player id %d".formatted(playerIndex));
		};
	}

	private int computeGameScore(int playerIndex, Set<Scan> scans) {
		int total = 0;
		for (Scan scan : scans) {
			total += scan.type.ordinal() + 1;
			if (firstToScan.get(scan) == null || firstToScan.get(scan).equals(playerIndex)) {
				firstToScan.put(scan, playerIndex);
				total += scan.type.ordinal() + 1;
			}
		}

		for (FishType type : FishType.values()) {
			if (!playerScannedAllFishOfType(scans, type)) {
				continue;
			}
			total += Game.COLORS_PER_FISH;
			if (Objects.isNull(firstToScanAllFishOfType.get(type))
					|| Objects.equals(firstToScanAllFishOfType.get(type), playerIndex)) {
				firstToScanAllFishOfType.put(type, playerIndex);
				total += Game.COLORS_PER_FISH;
			}
		}

		for (int color = 0; color < Game.COLORS_PER_FISH; ++color) {
			if (!playerScannedAllFishOfColor(scans, color)) {
				continue;
			}
			total += FishType.values().length;
			if (Objects.isNull(firstToScanAllFishOfColor.get(color))
				|| Objects.equals(firstToScanAllFishOfColor.get(color), playerIndex)) {
				firstToScanAllFishOfColor.put(color, playerIndex);
				total += FishType.values().length;
			}
		}
		return total;
	}

	public int computeFullEndGameScore(GamePlayer gamePlayer) {
		HashSet<Scan> scans = new HashSet<>(Player.ALL_AVAILABLE_SCANS);
		gamePlayer.drones.forEach(d -> scans.addAll(d.scans));
		scans.addAll(gamePlayer.scans);
		return computeGameScore(gamePlayer.getIndex(), scans);
	}

	private boolean playerScannedAllFishOfType(Set<Scan> scans, FishType type) {
		for (int color = 0; color < Game.COLORS_PER_FISH; ++color) {
			if (!scans.contains(new Scan(type, color))) {
				return false;
			}
		}
		return true;
	}

	private boolean playerScannedAllFishOfColor(Set<Scan> scans, int color) {

		for (int i = 0; i < FishType.FISH_TYPE_VALUES.length; i++) {
			if (!scans.contains(new Scan(FishType.FISH_TYPE_VALUES[i], color))) {
				return false;
			}
		}
		return true;
	}

	//	public void reset() {
	//		firstToScan.clear();
	//		firstToScanAllFishOfColor.clear();
	//		firstToScanAllFishOfType.clear();
	//		allOfMyScans.clear();
	//		allOfFoeScans.clear();
	//	}

	public GameEstimator clone() {
		GameEstimator clone = new GameEstimator();
		clone.allOfMyScans = new HashSet<>(allOfMyScans);
		clone.allOfFoeScans = new HashSet<>(allOfFoeScans);
		clone.firstToScan = new HashMap<>(firstToScan);
		clone.firstToScanAllFishOfColor = new HashMap<>(firstToScanAllFishOfColor);
		clone.firstToScanAllFishOfType = new HashMap<>(firstToScanAllFishOfType);
		return clone;
	}
}
