package fr.tcordel.model;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Radar {

	public Map<Integer, RadarDirection> bearings = new HashMap<>();
	public List<Integer> topLeft = new ArrayList<>();
	public List<Integer> topRight = new ArrayList<>();
	public List<Integer> bottomRight = new ArrayList<>();
	public List<Integer> bottomLeft = new ArrayList<>();

	public Radar() {
	}

	public Radar(List<Integer> topLeft, List<Integer> topRight, List<Integer> bottomRight, List<Integer> bottomLeft) {
		this.topLeft = topLeft;
		this.topRight = topRight;
		this.bottomRight = bottomRight;
		this.bottomLeft = bottomLeft;
	}

	public void reset() {
		bearings.clear();
		topLeft.clear();
		topRight.clear();
		bottomRight.clear();
		bottomLeft.clear();
	}

	public void populate(int creatureId, RadarDirection radar) {
		bearings.put(creatureId, radar);
		switch (radar) {
			case TL -> topLeft.add(creatureId);
			case TR -> topRight.add(creatureId);
			case BR -> bottomRight.add(creatureId);
			case BL -> bottomLeft.add(creatureId);
		}
	}

	public RadarDirection forFish(int creatureId) {
		return bearings.get(creatureId);
	}

	public Radar forType(Map<Integer, Fish> fishes, FishType type) {
		return new Radar(
			topLeft.stream().filter(i -> fishes.containsKey(i) && fishes.get(i).type == type).toList(),
			topRight.stream().filter(i -> fishes.containsKey(i) && fishes.get(i).type == type).toList(),
			bottomRight.stream().filter(i -> fishes.containsKey(i) && fishes.get(i).type == type).toList(),
			bottomLeft.stream().filter(i -> fishes.containsKey(i) && fishes.get(i).type == type).toList()
		);
	}

	public Set<FishType> getTypes(Map<Integer, Fish> fishes) {
		return Stream.of(topLeft, topRight, bottomLeft, bottomRight)
			.flatMap(Collection::stream)
			.map(fishes::get)
			.filter(Objects::nonNull)
			.map(Fish::getType)
			.collect(Collectors.toSet());
	}
}
