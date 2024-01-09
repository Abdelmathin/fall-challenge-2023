package fr.tcordel.model;

public enum RadarDirection {

	//la créature est en haut à gauche du drone.
	TL(new Vector(-424, -424)),
	//la créature est en haut à droite du drone.
	TR(new Vector(+424, -424)),
	//la créature est en bas à droite du drone.
	BR(new Vector(+424, +424)),
	//la créature est en bas à gauche du drone.
	BL(new Vector(-424, +424));

	private final Vector direction;

	RadarDirection(Vector direction) {this.direction = direction;}

	public Vector getDirection() {
		return direction;
	}

	public RadarDirection hsymettric() {
		return switch (this) {
			case BL -> BR;
			case BR -> BL;
			case TL -> TR;
			case TR -> TL;
		};
	}
}