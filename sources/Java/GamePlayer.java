package fr.tcordel.model;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

import fr.tcordel.bridge.AbstractMultiplayerPlayer;

public class GamePlayer extends AbstractMultiplayerPlayer {

	public static final int ME = 0;
	public static final int FOE = 1;


	String message;
	List<Drone> drones;
	Set<Scan> scans;
//	Set<Fish> visibleFishes;

	List<Integer> countFishSaved;
	int points = 0;

	public GamePlayer() {
		drones = new ArrayList<>();
//		visibleFishes = new LinkedHashSet<>();
		scans = new LinkedHashSet<>();
		countFishSaved = new ArrayList<Integer>();
	}

	public GamePlayer(int index) {
		this();
		setIIndex(index);
	}

	public String getMessage() {
		return message;
	}

	public void reset() {
		message = null;
		drones.forEach(d -> {
			d.move = null;
//			d.fishesScannedThisTurn.clear();
			d.didReport = false;
			d.message = "";
		});
	}

	void setIIndex(int index) {
		this.index = index;
	}

}
