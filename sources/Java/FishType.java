package fr.tcordel.model;

import java.util.List;

public enum FishType {
    JELLY(1 * Game.HEIGHT / 4, 2 * Game.HEIGHT / 4), FISH(2 * Game.HEIGHT / 4, 3 * Game.HEIGHT / 4), CRAB(3 * Game.HEIGHT / 4, Game.HEIGHT);


    private final int upperLimit;
    private final int deeperLimit;

    public static FishType[] FISH_TYPE_VALUES = FishType.values();

    public static List<FishType> FISH_ORDERED = List.of(CRAB, FISH, JELLY);

	FishType(int upperLimit, int deeperLimit) {
		this.upperLimit = upperLimit;
		this.deeperLimit = deeperLimit;
	}

	public int getUpperLimit() {
        return upperLimit;
    }

    public int getDeeperLimit() {
        return deeperLimit;
    }

	public static FishType forY(double y, int threshold) {
		if ((y - threshold) >= FishType.JELLY.getUpperLimit() && (y) <= FishType.JELLY.getDeeperLimit()) {
			return FishType.JELLY;
		}
		if ((y - threshold) >= FishType.FISH.getUpperLimit() && (y) <= FishType.FISH.getDeeperLimit()) {
			return FishType.FISH;
		}
		if ((y - threshold) >= FishType.CRAB.getUpperLimit() && (y) <= FishType.CRAB.getDeeperLimit()) {
			return FishType.CRAB;
		}

		return null;
	}

	public static FishType deeper(FishType type) {
		if (type == null) {
			return JELLY;
		} else if (type==JELLY) {
			return FISH;
		} else  {
			return CRAB;
		}
	}

	public static FishType upper(FishType type) {
		if (type == null) {
			return null;
		} else if (type==JELLY) {
			return null;
		} else if (type==FISH) {
			return JELLY;
		} else  {
			return FISH;
		}
	}
}
