package fr.tcordel.bridge;

import java.util.ArrayList;
import java.util.List;

public abstract class AbstractPlayer {

	protected int index;
	private List<String> inputs = new ArrayList();
	private boolean timeout;
	private int score;
	private boolean hasBeenExecuted;
	private boolean hasNeverBeenExecuted = true;

	public AbstractPlayer() {
	}

	public final String getNicknameToken() {
		return "$" + this.index;
	}

	public final String getAvatarToken() {
		return "$" + this.index;
	}

	int getIndex() {
		return this.index;
	}

	int getScore() {
		return this.score;
	}

	void setScore(int score) {
		this.score = score;
	}
}
