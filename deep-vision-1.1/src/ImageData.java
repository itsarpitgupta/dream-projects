import java.awt.Rectangle;
import java.awt.image.BufferedImage;

public class ImageData {

	private String imgName;
	private boolean isPass;
	private boolean isHighLoad;
	private String path;
	private BufferedImage img;
	private double matchPercentage;

	public double getMatchPercentage() {
		return matchPercentage;
	}

	public void setMatchPercentage(double matchPercentage) {
		this.matchPercentage = matchPercentage;
	}

	public BufferedImage getImg() {
		return img;
	}

	public void setImg(BufferedImage img) {
		this.img = img;
	}

	public String getPath() {
		return path;
	}

	public void setPath(String path) {
		this.path = path;
	}

	public String getImgName() {
		return imgName;
	}

	public void setImgName(String imgName) {
		this.imgName = imgName;
	}

	public boolean isPass() {
		return isPass;
	}

	public void setPass(boolean isPass) {
		this.isPass = isPass;
	}

	public boolean isHighLoad() {
		return isHighLoad;
	}

	public void setHighLoad(boolean isHighLoad) {
		this.isHighLoad = isHighLoad;
	}

	@Override
	public String toString() {
		return "ImageData [imgName=" + imgName + ", isPass=" + isPass + ", isHighLoad=" + isHighLoad + ", path=" + path
				+ "]";
	}

}
