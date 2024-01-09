
package fr.tcordel.bridge;

public abstract class AbstractMultiplayerPlayer extends AbstractPlayer {

	private boolean active = true;

	public AbstractMultiplayerPlayer() {
	}

	public final boolean isActive() {
		return this.active;
	}

	public final int getIndex() {
		return super.getIndex();
	}

	public final int getScore() {
		return super.getScore();
	}

	public final void setScore(int score) {
		super.setScore(score);
	}

}
