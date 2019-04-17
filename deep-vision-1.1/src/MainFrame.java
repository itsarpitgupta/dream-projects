import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.EventQueue;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.Robot;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import javax.imageio.ImageIO;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.SwingConstants;
import javax.swing.border.BevelBorder;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.JTableHeader;
import javax.swing.table.TableColumnModel;

public class MainFrame extends JFrame implements MouseListener, MouseMotionListener {

	int drag_status = 0, c1, c2, c3, c4;
	private static ResultDisplayPanel resultDisplayPanel = null;
	private BlockingQueue<ImageData> processQueue = null;
	private BlockingQueue<ImageData> resultQueue = null;
	private boolean tempMatch;
	private boolean searchMatch;
	private static MainFrame mainFrame = null;
	private static JTable jt = null;
	private static DefaultTableModel model = null;
	private static JPanel statusPanel = null;
	private static Rectangle searchArea = null;
	private static Rectangle tempArea = null;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					mainFrame = new MainFrame();
					mainFrame.setVisible(true);

					mainFrame.loadStartupUi();

				} catch (Exception e) {
					e.printStackTrace();
				}
			}

		});
	}

	public static void loadResult(ImageData image, int count) throws InterruptedException {
		jt.setVisible(true);
		SoundEffect sound = new SoundEffect(Constants.SOUND_TYPE_HIGH);
		if (image.isHighLoad() && sound != null) {
			sound.play();
		}

		mainFrame.setTitle(image.getImgName());

		resultDisplayPanel.loadImage(image);
		resultDisplayPanel.updateUI();

		model.setValueAt(image.getImgName(), 0, 1);
		model.setValueAt(count, 1, 1);
		model.setValueAt(image.isPass() ? "PASS" : "FAIL", 2, 1);
		model.setValueAt(image.isHighLoad() ? "HIGH" : "LOW", 3, 1);
		model.setValueAt(image.getMatchPercentage()+"%", 4, 1);
		
//		Thread.sleep(1000);

	}

	private void loadStartupUi() {
		ImageData ig = new ImageData();
		ig.setPath("D:\\Vision_Application\\hul_bad_230219\\Bad");
		ig.setImgName("Image00127.BMP");
		resultDisplayPanel.loadImage(ig);
		resultDisplayPanel.updateUI();
		addMouseListener(this);
		addMouseMotionListener(this);

	}

	/**
	 * Create the frame.
	 */
	public MainFrame() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(0, 0, 820, 700);
		resultDisplayPanel = new ResultDisplayPanel();
		resultDisplayPanel.setBorder(new BevelBorder(BevelBorder.RAISED));
		resultDisplayPanel.setPreferredSize(new Dimension(getWidth(), 40));
		resultDisplayPanel.setLayout(new BoxLayout(resultDisplayPanel, BoxLayout.X_AXIS));

		add(resultDisplayPanel, BorderLayout.CENTER);

		loadPatternTool();

		// create the status bar panel and shove it down the bottom of the frame
		loadStatusBar();

		loadResultTable();

	}

	private void loadResultTable() {
		String column[] = { "ID", "NAME" };
		model = new DefaultTableModel(column, 0);
		jt = new JTable(model);

		jt.setLayout(new BoxLayout(jt, BoxLayout.X_AXIS));

		model.addRow(new String[] { "Image Name", });
		model.addRow(new String[] { "Count", });
		model.addRow(new String[] { "Status", });
		model.addRow(new String[] { "Load", });
		model.addRow(new String[] { "MatchPercentage", });

		
		jt.setAutoResizeMode(JTable.AUTO_RESIZE_NEXT_COLUMN);
		TableColumnModel colModel = jt.getColumnModel();
		colModel.getColumn(1).setPreferredWidth(120);

		jt.disable();
		jt.setTableHeader(new JTableHeader());
		jt.setBackground(Color.YELLOW);

		jt.setFont(new Font("Courier", Font.BOLD, 15));
		jt.setForeground(Color.RED);

		jt.setVisible(false);
		resultDisplayPanel.add(jt);

	}

	private void loadStatusBar() {
		statusPanel = new JPanel();
		statusPanel.setBorder(new BevelBorder(BevelBorder.LOWERED));
		statusPanel.setPreferredSize(new Dimension(getWidth(), 16));
		statusPanel.setLayout(new BoxLayout(statusPanel, BoxLayout.X_AXIS));
		showMsgOnStatusBar("Please select search area.", SwingConstants.LEFT, statusPanel);
		getContentPane().add(statusPanel, BorderLayout.SOUTH);
	}

	private void loadPatternTool() {
		JPanel patternToolPanel = new JPanel();
		patternToolPanel.setPreferredSize(new Dimension(resultDisplayPanel.getWidth(), 40));
		patternToolPanel.setLayout(new FlowLayout());

		JButton cropBtn = new JButton("Crop");
		cropBtn.setBounds(0, 0, 5, 8);
		cropBtn.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {

			}
		});

		JButton startBtn = new JButton("Start");
		startBtn.setBounds(0, 0, 5, 8);
		startBtn.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {

				processQueue = new ArrayBlockingQueue<ImageData>(1);
				resultQueue = new ArrayBlockingQueue<ImageData>(10);

				final ExecutorService imageLoaderService = Executors.newSingleThreadExecutor();
				imageLoaderService.submit(new ImageLoaderThread(processQueue));

				final ExecutorService imageProcessorService = Executors.newSingleThreadExecutor();
				imageProcessorService.submit(new ImageProcessorThread(processQueue, resultQueue));

				final ExecutorService imageResultService = Executors.newSingleThreadExecutor();
				imageResultService.submit(new ImageResultThread(resultQueue));

				imageLoaderService.shutdown();
				imageProcessorService.shutdown();
				imageResultService.shutdown();
			}
		});

		patternToolPanel.add(startBtn);
		patternToolPanel.add(cropBtn);
		getContentPane().add(patternToolPanel, BorderLayout.NORTH);
	}

	private static void showMsgOnStatusBar(String msg, int position, JPanel statusPanel) {
		JLabel statusLabel = new JLabel(msg);
		statusLabel.setHorizontalAlignment(position);
		statusPanel.add(statusLabel);
	}

	public void draggedScreen() throws Exception {
		int w = c1 - c3;
		int h = c2 - c4;
		w = w * -1;
		h = h * -1;

		Robot robot = new Robot();
		Rectangle rect = new Rectangle(c1 + 5, c2 + 5, w - 5, h - 5);
		if (searchArea == null) {
			searchArea = rect;
		} else {
			tempArea = rect;
			BufferedImage img = robot.createScreenCapture(tempArea);
			File save_path = new File("template.jpg");
			ImageIO.write(img, "JPG", save_path);
			System.out.println("Cropped image saved successfully.");
		}

	}

	@Override
	public void mouseClicked(MouseEvent arg0) {
	}

	@Override
	public void mouseEntered(MouseEvent arg0) {
	}

	@Override
	public void mouseExited(MouseEvent arg0) {
	}

	@Override
	public void mousePressed(MouseEvent arg0) {
		c1 = arg0.getX();
		c2 = arg0.getY();
	}

	@Override
	public void mouseReleased(MouseEvent arg0) {
		// repaint();
		if (drag_status == 1) {
			c3 = arg0.getX();
			c4 = arg0.getY();
			try {
				int a = JOptionPane.showConfirmDialog(mainFrame, "Are you sure?");
				statusPanel.removeAll();
				if (a == JOptionPane.YES_OPTION && searchArea == null) {
					String msg = "Search Area (" + c1 + "," + c2 + "), (" + c3 + "," + c4 + ")";
					showMsgOnStatusBar(msg, SwingConstants.RIGHT, statusPanel);
					statusPanel.updateUI();
					draggedScreen();
					searchMatch = true;
				} else if (a == JOptionPane.YES_OPTION && tempArea == null) {
					String msg = "Temp Area (" + c1 + "," + c2 + "), (" + c3 + "," + c4 + ")";
					showMsgOnStatusBar(msg, SwingConstants.RIGHT, statusPanel);
					statusPanel.updateUI();
					draggedScreen();
					tempMatch = true;	
				} else {
					c1 = 0;
					c2 = 0;
					c3 = 0;
					c4 = 0;
				}

//				repaint();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}

	@Override
	public void mouseDragged(MouseEvent arg0) {
		drag_status = 1;
		c3 = arg0.getX();
		c4 = arg0.getY();
		repaint();
	}

	@Override
	public void mouseMoved(MouseEvent arg0) {
	}

	@Override
	public void paint(Graphics g) {
		super.paint(g);
		int w = c1 - c3;
		int h = c2 - c4;
		w = w * -1;
		h = h * -1;
		if (w < 0)
			w = w * -1;
		if (searchArea == null ) {
			g.setColor(Color.RED);
			g.drawString("SEARCH", c1, c2-5);
		} else if (tempArea == null || tempMatch) {
			g.setColor(Color.GREEN);
			g.drawString("MATCH", c1, c2-5);
		}

		g.drawRect(c1, c2, w, h);
	}
}
