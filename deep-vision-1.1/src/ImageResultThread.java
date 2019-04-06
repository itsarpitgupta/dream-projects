import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.concurrent.BlockingQueue;

import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.SwingConstants;
import javax.swing.border.BevelBorder;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumnModel;

public class ImageResultThread implements Runnable {

	private final BlockingQueue<ImageData> resultQueue;
	private int count = 1;

	public ImageResultThread(BlockingQueue<ImageData> resultQueue) {
		this.resultQueue = resultQueue;
	}

	@Override
	public void run() {
		try {

			while (true) {

				ImageData image = resultQueue.take();
				MainFrame.loadResult(image, count);
				count++;
			}
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

}
