import java.io.File;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;

public class SoundEffect {

	private Clip clip;

	public SoundEffect(String soundType) {
		try {
			File file = null;
			if (soundType.equals(Constants.SOUND_TYPE_HIGH)) {
				file = new File(Constants.HIGH_LOAD_SOUND_FILE_PATH);
			}

			AudioInputStream ais = AudioSystem.getAudioInputStream(file);
			this.clip = AudioSystem.getClip();
			this.clip.open(ais);
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	public void play() {
		clip.setFramePosition(0);
		clip.start();
	}

}
