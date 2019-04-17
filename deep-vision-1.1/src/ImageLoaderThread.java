import java.util.concurrent.BlockingQueue;

public class ImageLoaderThread implements Runnable {

	private final BlockingQueue<ImageData> processQueue;
	private static final String IMAGE_PATH = "D:\\Vision_Application\\hul_bad_230219\\Bad";
	private static final String EXT = ".BMP";

	public ImageLoaderThread(BlockingQueue processQueue) {
		this.processQueue = processQueue;
	}

	@Override
	public void run() {
		try {
			loadImage();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	private void loadImage() throws InterruptedException {
		for (int i = 11; i <= 60; i++) {
			ImageData image = new ImageData();
			image.setImgName("Image001" + i + EXT);
			image.setPath(IMAGE_PATH);
			
			Thread.sleep(100);
			this.processQueue.put(image);

		}
	}

}
