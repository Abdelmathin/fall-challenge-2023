package fr.tcordel.model;

public class Fish implements Entity {
    FishType type;
    Vector pos;
    int color;
    double startY;
    Vector speed;
    int id;
    int lowY, highY;
    boolean isFleeing;
    /* stats */
    Integer fleeingFromPlayer;

    boolean escaped = false;

    public RadarZone radarZone;

    public int lastSeenTurn = 0;

    public Fish(int id, int color, FishType type) {
        this.type = type;
        this.color = color;
        this.id = id;
        switch (type) {
            case JELLY -> {
                lowY = 1 * Game.HEIGHT / 4;
                highY = 2 * Game.HEIGHT / 4;
			}
            case FISH -> {
                lowY = 2 * Game.HEIGHT / 4;
                highY = 3 * Game.HEIGHT / 4;
            }
            case CRAB -> {
                lowY = 3 * Game.HEIGHT / 4;
                highY = 4 * Game.HEIGHT / 4;
            }
        }
    }

    public Fish(double x, double y, FishType type, int color, int id, int lowY, int highY) {
        this.id = id;
        this.pos = new Vector(x, y);
        this.type = type;
        this.color = color;
        this.lowY = lowY;
        this.highY = highY;
        this.speed = Vector.ZERO;
    }

    @Override
    public Vector getPos() {
        return pos;
    }

    @Override
    public Vector getSpeed() {
        return speed;
    }

    public double getX() {
        return pos.getX();
    }

    public double getY() {
        return pos.getY();
    }


    @Override
    public int getId() {
        return id;
    }

    public FishType getType() {
        return type;
    }
}
