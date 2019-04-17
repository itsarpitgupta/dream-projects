import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.InputStream;

import javax.imageio.ImageIO;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Core.MinMaxLocResult;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
 
public class TemplateMatching {
	
	private final static String templateImagePath = "D:\\github-repos\\dream-projects\\deep-vision-1.1\\template.jpg";
 
	public TemplateMatching() {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
    public void startMatch(ImageData imageData) {
        try {
        	Mat source=null;
        	Mat template=null;

        	//Load image file
        	source=Imgcodecs.imread(imageData.getPath()+"\\"+imageData.getImgName());
        	template=Imgcodecs.imread(templateImagePath);
        	
        	int result_cols = source.cols() - template.cols() + 1;
            int result_rows = source.rows() - template.rows() + 1;
            Mat result = new Mat(result_rows, result_cols, CvType.CV_32FC1);
            
        	
            int machMethod=Imgproc.TM_CCOEFF_NORMED;
        	//Template matching method
        	Imgproc.matchTemplate(source, template, result, machMethod);
        	
        	MinMaxLocResult mmr = Core.minMaxLoc(result);
            Point matchLoc=mmr.maxLoc;
            
            double threashhold = 0.40;
            if (mmr.maxVal > threashhold) {
            	Imgproc.rectangle(source, matchLoc, new Point(matchLoc.x + template.cols(),
                        matchLoc.y + template.rows()), new Scalar(0, 255, 0));
            	imageData.setPass(true);
            }else {
            	imageData.setPass(false);
            }
        	
        	 // Encoding the image
            MatOfByte matOfByte = new MatOfByte();
            Imgcodecs.imencode(".BMP", source, matOfByte);

            // Storing the encoded Mat in a byte array
            byte[] byteArray = matOfByte.toArray();

            // Displaying the image
            InputStream in = new ByteArrayInputStream(byteArray);
            BufferedImage bufImage = ImageIO.read(in);
            
        	imageData.setImg(bufImage);
        	imageData.setMatchPercentage((int)(mmr.maxVal*100));
        	imageData.setHighLoad(false);
        }catch(Exception e) {
        	e.printStackTrace();
        }
    }
 
}