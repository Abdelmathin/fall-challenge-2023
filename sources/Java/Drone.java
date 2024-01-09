package fr.tcordel.model;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Drone implements Entity {

    Vector pos;
    Vector move;
    Vector speed;
    Vector lastSpeed;

    int light;
    int battery;
    List<Scan> scans;
//    List<Integer> fishesScannedThisTurn;
    boolean lightSwitch;
    boolean lightOn;
    boolean dying;
    boolean dead;
    boolean didReport;
    int id;
    double dieAt;
    String message;
    GamePlayer owner;

    public Fish target;

    public DroneInitialPosition initialPosition = null;


    public Map<Integer, Fish> allocations = new HashMap<>();

    Map<Integer, RadarDirection> radar = new HashMap<>();

    Strat strat = Strat.DOWN;
    
    /* stats */
    int maxTurnsSpentWithScan;
    int turnsSpentWithScan;
    int maxY;

    public Drone(double x, int y, int id, GamePlayer owner) {
        this.id = id;
        this.owner = owner;
        pos = new Vector(x, y);
        battery = Game.DRONE_MAX_BATTERY;
        light = 0;
        scans = new ArrayList<>();
        lightSwitch = false;
        speed = Vector.ZERO;
        dying = false;
        dead = false;
        didReport = false;
        lightOn = false;
//        fishesScannedThisTurn = new ArrayList<>();
        message = "";
    }

    @Override
    public Vector getPos() {
        return pos;
    }

    @Override
    public Vector getSpeed() {
        return speed;
    }

    public boolean isEngineOn() {
        return move != null;
    }

    public boolean isLightOn() {
        return lightOn;
    }


    public void drainBattery() {
        battery -= Game.LIGHT_BATTERY_COST;
    }

    public void rechargeBattery() {
        if (battery < Game.DRONE_MAX_BATTERY) {
            battery += Game.DRONE_BATTERY_REGEN;
            if (battery >= Game.DRONE_MAX_BATTERY) {
                battery = Game.DRONE_MAX_BATTERY;
            }
        }

    }

    public boolean isDeadOrDying() {
        return dying || dead;
    }

    public double getX() {
        return pos.getX();
    }

    public double getY() {
        return pos.getY();
    }

    public String scanSlotToString(int i) {
        if (scans.size() > i) {
            Scan scan = scans.get(i);
            return scan.toInputString();
        }
        return "-1 -1";
    }

    public void setMessage(String message) {
        this.message = message;
        if (message != null && message.length() > 48) {
            this.message = message.substring(0, 46) + "...";
        }

    }

    public void resetRadars() {
        radar.clear();
    }


    @Override
    public int getId() {
        return id;
    }

    public GamePlayer getOwner() {
        return owner;
    }

    public Map<Integer, RadarDirection> getRadar() {
        return radar;
    }

    public List<Scan> getScans() {
        return scans;
    }

    public boolean isCommitting() {
        if (lastSpeed == null || speed == null) {
            return false;
        }
        int threshold = -(Game.DRONE_MOVE_SPEED - 50);
        return /*lastSpeed.getY() <= threshold &&*/
               speed.getY() <= threshold;
    }
}
