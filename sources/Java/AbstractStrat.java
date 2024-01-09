package fr.tcordel.model;

public abstract class AbstractStrat {

	protected final Game game;
	protected double _1DegToRadians = Math.toRadians(5);
	protected double _15DegToRadians = Math.toRadians(15);
	protected double _35DegToRadians = Math.toRadians(35);

	Vector UP = new Vector(0, -Game.DRONE_MOVE_SPEED);
	Vector DOWN = new Vector(0, Game.DRONE_MOVE_SPEED);
	Vector DOWN_LEFT = DOWN.rotate(_15DegToRadians).round();
	Vector DOWN_BIG_LEFT = DOWN.rotate(_35DegToRadians).round();
	Vector DOWN_RIGHT = DOWN.rotate(-_15DegToRadians).round();
	Vector DOWN_BIG_RIGHT = DOWN.rotate(-_35DegToRadians).round();

	protected AbstractStrat(Game game) {this.game = game;}


	boolean moveAndCheckNoCollision(Drone drone, Vector vector, int i, boolean moveDrone, double offset) {
		if (moveDrone) {
			drone.move = game.snapToDroneZone(drone.pos.add(vector.rotate(i * _1DegToRadians)).round());

			game.updateDrone(drone);
		}
		if (game.uglies
			.stream()
			.filter(ugly -> ugly.pos != null)
			.noneMatch(u -> game.getCollision(drone, u, offset))) {
			//			if (i == 0) {
			//					vector.normalize().mult(game.getMoveSpeed(drone));
			//			}
//			System.err.println("No Collision spotted : " + drone.id + "," + i + " original vector " + vector);
			return true;
		} else {
//			System.err.println("Collision spotted, new attemps processing for " + drone.id + "," + i);
		}
		return false;
	}

	protected Vector filterDirection(Drone drone, Vector vector, Vector direction, int xLimit, int yLimit) {
		double toXborder = Math.min(vector.getX(), Math.abs(vector.getX() - Game.WIDTH));
		double currentToXBorder = Math.min(drone.getX(), Math.abs(drone.getX() - Game.WIDTH));
		if ((toXborder < currentToXBorder) && (toXborder < xLimit)) {
			System.err.println("Reset X for drone " + drone.getId());
			direction =  new Vector(0, direction.getY());
		}

		vector = drone.pos.add(direction);
		double toYborder = Game.HEIGHT - vector.getY();
		double currentToYBorder = Game.HEIGHT - drone.getY();
		if ((toYborder < currentToYBorder) && (toYborder < yLimit)) {
			System.err.println("Reset Y for drone " + drone.getId() + " v" + vector+ ", " + yLimit);
			direction =  new Vector(direction.getX(), 0);
		}
		if (direction.getX() == 0 && direction.getY() == 0) {
			System.err.println("GoingUP for drone " + drone.getId());
			direction = UP;
		}
		return direction
			.normalize().mult(game.getMoveSpeed(drone)).round();
	}
}
