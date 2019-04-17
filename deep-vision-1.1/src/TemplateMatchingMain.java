import org.opencv.core.Core;
import org.opencv.core.Core.MinMaxLocResult;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
 
public class TemplateMatchingMain {
 
    public static void main(String[] args) {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        Mat source=null;
        Mat template=null;
        String filePath="D:\\github-repos\\dream-projects\\deep-vision-1.1\\";
        //Load image file
        source=Imgcodecs.imread("D:\\Vision_Application\\hul_bad_230219\\Bad\\Image00126.BMP");
        template=Imgcodecs.imread(filePath+"template.jpg");
    
        int result_cols = source.cols() - template.cols() + 1;
        int result_rows = source.rows() - template.rows() + 1;
        Mat result = new Mat(result_rows, result_cols, CvType.CV_32FC1);
        
        // methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',  'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
        int machMethod=Imgproc.TM_CCOEFF_NORMED;
        //Template matching method
        Imgproc.matchTemplate(source, template, result, machMethod);
 
		// ! [normalize]
		// Core.normalize(result, result, 0, 1, Core.NORM_MINMAX, -1, new Mat());

		// Imgproc.threshold(result, result, 0.3, 1.0, Imgproc.THRESH_TOZERO);
    
        MinMaxLocResult mmr = Core.minMaxLoc(result);
        Point matchLoc=mmr.maxLoc;
        
        double threashhold = 0.40;
        if (mmr.maxVal > threashhold) {
        	Imgproc.rectangle(source, matchLoc, new Point(matchLoc.x + template.cols(),
                    matchLoc.y + template.rows()), new Scalar(0, 255, 0));
        }
        
        Imgcodecs.imwrite(filePath+"sonuc.jpg", source);
        System.out.println("Complated->" + mmr.maxVal);
    }
 
}