package fr.tcordel.model;

public class AttackFish extends AbstractStrat {

	//seed=2740983747143833600
	public AttackFish(Game game) {super(game);}

	Vector process(Fish fish, Drone drone) {
		drone.strat = Strat.ATTACK;
		drone.target = fish;
		Vector target = null;
		Vector pos = null;
		resetCache(fish);
		boolean visible = fish.pos != null;
		if (visible) {
			pos = game.snapToFishZone(fish.pos.add(fish.speed), fish);
			int offset = ((pos.getX() < (Game.WIDTH / 2)) ? 1 : -1) * Game.DARK_SCAN_RANGE;
			double targetX = fish.pos.getX() + offset;
			double deltaTargetX = targetX - drone.getX();
			double deltaTargetY = pos.getY() - drone.getY();
			boolean correctingX = (drone.getX() < targetX && drone.getX() < fish.pos.getX())
				|| (drone.getX() > targetX && drone.getX() > fish.pos.getX());
			if (fish.pos.distance(drone.pos) >= Game.FISH_HEARING_RANGE) {

				target = new Vector((int)pos.getX() + offset - drone.getX(),
					deltaTargetY);
			} else if (correctingX && Math.abs(deltaTargetX) >= 450) {
				System.err.println("Correcting X for drone " + drone.id + "to attack " + fish.id);
				target = new Vector(deltaTargetX, 0);
			} else if (Math.abs(deltaTargetY) >= 450) {
				System.err.println("Correcting Y for drone " + drone.id + "to attack " + fish.id);
				target = new Vector(0,
					deltaTargetY);
			} else {
				target = new Vector((int)pos.getX() + offset - drone.getX(),
					deltaTargetY);
			}
		} else {
			target = drone.getRadar().get(fish.id)
				.getDirection();
		}
		System.err.printf("Drone %d attacking %d, f.p %s, f.v %s, t %s %b%n", drone.id, fish.id, pos, fish.speed, target, visible);
		return target;
	}

	private void resetCache(Fish fish) {
		if (Player.ROUND  - fish.lastSeenTurn >= 4) {
			System.err.println("Resetting position for fish " + fish.id);
			fish.pos = null;
			fish.speed = null;
		}
	}
}
