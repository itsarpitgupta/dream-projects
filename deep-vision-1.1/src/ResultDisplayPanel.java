import java.awt.Color;
import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.JPanel;

public class ResultDisplayPanel extends JPanel {

	BufferedImage img;
	ImageData image = null;
	public void loadImage(ImageData image) {
		String filePath = image.getPath() + "\\" + image.getImgName();
		File imageFile = new File(filePath);
		try {
			img = ImageIO.read(imageFile);
			this.image = image;
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	protected void paintComponent(Graphics g) {  
		super.paintComponent(g);

		if(image!= null && image.getImg()!=null) {
			// g.setColor(Color.GREEN);
			// g.drawRect(image.getRectangle().x,image.getRectangle().y,image.getRectangle().width,image.getRectangle().height);
 			g.drawImage(image.getImg(), 0, 0, 800, 600, this);
		}else {
			g.drawImage(img, 0, 0, 800, 600, this);
		}
		
		setVisible(true);
	}

	
}
