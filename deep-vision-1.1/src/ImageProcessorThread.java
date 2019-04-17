import java.time.Duration;
import java.time.Instant;
import java.util.concurrent.BlockingQueue;

public class ImageProcessorThread implements Runnable {

	private final BlockingQueue<ImageData> processQueue;
	private final BlockingQueue<ImageData> resultQueue;
	private TemplateMatching templateMatching;

	public ImageProcessorThread(BlockingQueue processQueue, BlockingQueue resultQueue) {
		this.processQueue = processQueue;
		this.resultQueue = resultQueue;
	}

	@Override
	public void run() {
		try {
			templateMatching = new TemplateMatching();
			while (true) {
				Instant start = Instant.now();
				ImageData image = processQueue.take();
				if (processQueue.size() == 1) {
					failDueToHighLoad(image);
				} else {
					process(image);
				}

				loadImageIntoResultQueue(image);
				Instant finish = Instant.now();

			    long timeElapsed = Duration.between(start, finish).toMillis();  //in millis
				System.out.println(timeElapsed);

			}
		} catch (InterruptedException e) {
			Thread.currentThread().interrupt();
		}

	}

	private void process(ImageData image) {
		try {
			Thread.sleep(0);
			if (processQueue.size() == 1) {
				failDueToHighLoad(image);
				return;
			}

			templateMatching.startMatch(image);

			// isPass(image);
		} catch (InterruptedException e) {
			image.setPass(false);
			e.printStackTrace();
		}
	}

	private void loadImageIntoResultQueue(ImageData image) {
		try {
			resultQueue.put(image);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	private void isPass(ImageData image) {
		image.setPass(true);
		image.setHighLoad(false);
	}

	private void failDueToHighLoad(ImageData image) {
		image.setPass(false);
		image.setHighLoad(true);
	}

}
