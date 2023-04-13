import cv2
import base64
import numpy as np
from DocumentSegmentationCV import DocumentSegmentationCV
from DocumentSegmentationCNN import DocumentSegmentationCNN
from imutils import contours as imutils_contours

class DigitRecognizer:
    def __init__(self):
        # initialize any variables
        pass
    
    def recognize_digits_in_frame(self, video_stream):
        """
        Recognize handwritten digits in a video frame.

        Parameters:
        todo.
        """

        # convert the base64-encoded frame to a numpy array
        frame = cv2.imdecode(np.frombuffer(base64.b64decode(frame), dtype=np.uint8), cv2.IMREAD_COLOR)
        
        pass
    
    def recognize_digits_in_photo(self, photo):
        """
        Recognize handwritten digits in a photo.

        Parameters:
        Photo:
        """
        if(True):
            segmentation = DocumentSegmentationCNN()
        else:
            segmentation = DocumentSegmentationCV()

        aligned_photo = segmentation.align_document(photo)

        self.find_grid_in_image(aligned_photo)

        # TODO: return dict with boolean and numbers for found digits.
        return aligned_photo


    def find_grid_in_image(self, image):
        #Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        #Blur the image
        blur = cv2.GaussianBlur(gray, (5,5), 0)

        #Apply adaptive threshold so we have independent illumination
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

        #Find the largest contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        best_cnt = self.find_largest_contours(contours)

        #Find mask
        mask = np.zeros((gray.shape),np.uint8)
        cv2.drawContours(mask,[best_cnt],0,255,7)
        cv2.drawContours(mask,[best_cnt],0,255,-1)

        #Apply mask to copy of original image
        out = np.zeros_like(gray)
        out[mask == 255] = gray[mask == 255]


        self.get_yatzy_grid(out)

        
    def find_largest_contours(self, contours):
        max_area = 0
        best_cnt = 0
        c = 0
        for i in contours:
                area = cv2.contourArea(i)
                if area > 1000:
                        if area > max_area:
                            max_area = area
                            best_cnt = i
                c+=1
        return best_cnt
    
    def get_yatzy_grid(self, img_binary_sheet):
        """ Returns a binary image with a grid and the input image containing only horizontal/vertical lines.
        Args:
            img_binary_sheet ((rows,col) array): binary image
        Returns:
            img_binary_grid: an image containing painted vertically and horizontally lines
            img_binary_sheet_only_digits: an image containing only(mostly) handwritten digits
        """
        height, width = img_binary_sheet.shape

        img_binary_sheet_morphed = img_binary_sheet.copy()

        # Now we have the binary image with adaptive threshold.
        # We need to do some morphylogy operations in order to strengthen thin lines, remove noise, and also handwritten stuff.
        # We only want the horizontal / vertical pixels left before we start identifying the grid. See http://homepages.inf.ed.ac.uk/rbf/HIPR2/morops.htm

        # CLOSING: (dilate -> erode) will fill in background (black) regions with White. Imagine sliding struct element
        # in the background pixel, if it cannot fit the background completely(touching the foreground), fill this pixel with white

        # OPENING: ALL FOREGROUND PIXELS(white) that can fit the structelement will be white, else black.
        # Erode -> Dilate

        # Erosion: If the structuring element can fit inside the forground pixel(white), then keep white, else set to black
        # Dilation: For every background pixel(black), if one of the foreground(white) pixels are present, set this background (black) to foreground.

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        img_binary_sheet_morphed = cv2.morphologyEx(img_binary_sheet_morphed, cv2.MORPH_DILATE, kernel)

        cv2.imshow("morph", img_binary_sheet_morphed)
        cv2.waitKey(0)

        sheet_binary_grid_horizontal = img_binary_sheet_morphed.copy()
        sheet_binary_grid_vertical = img_binary_sheet_morphed.copy()

        # We use relative length for the structuring line in order to be dynamic for multiple sizes of the sheet.
        structuring_line_size = int(width / 5.0)

        # Try to remove all vertical stuff in the image,
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (structuring_line_size, 1))
        sheet_binary_grid_horizontal = cv2.morphologyEx(sheet_binary_grid_horizontal, cv2.MORPH_OPEN, element)

        # Try to remove all horizontal stuff in image, Morph OPEN: Keep everything that fits structuring element i.e vertical lines
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, structuring_line_size))

        sheet_binary_grid_vertical = cv2.morphologyEx(sheet_binary_grid_vertical, cv2.MORPH_OPEN, element)

        # Concatenate the vertical/horizontal lines into grid
        img_binary_sheet_morphed = cv2.add(
            sheet_binary_grid_vertical, sheet_binary_grid_horizontal)

        cv2.imshow("morph_keep_only_horizontal_lines", sheet_binary_grid_horizontal)
        cv2.waitKey(0)

        # cv_utils.show_window("morph_keep_only_horizontal_lines",
        #                     sheet_binary_grid_horizontal)
        # cv_utils.show_window("morph_keep_only_vertical_lines", sheet_binary_grid_vertical)
        # cv_utils.show_window("concatenate_vertical_horizontal", img_binary_sheet_morphed)
        # """
        #     Time to get a solid grid, from what we see  above, the grid is still not fully filled (sometimes)
        #     since the paper is not fully straight on the table etc. For this we use Hough Transform
        #     Hough transform identifies points (x,y) on the same line. 
        # """

        # We ideally should choose np.pi / 2 for the Theta accumulator, since we only want lines in 90 degrees and 0 degrees.
        rho_accumulator = 1
        angle_accumulator = np.pi / 2
        # Min vote for defining a line
        threshold_accumulator_votes = int(width/2)

        # Find lines in the image according to the Hough Algorithm
        grid_lines = cv2.HoughLines(img_binary_sheet_morphed, rho_accumulator,
                                    angle_accumulator, threshold_accumulator_votes)

        img_binary_grid = np.zeros(
            img_binary_sheet_morphed.shape, dtype=img_binary_sheet_morphed.dtype)

        # Since we can have multiple lines for same grid line, we merge nearby lines
        grid_lines = self.merge_nearby_lines(grid_lines)

        self.draw_lines(grid_lines, img_binary_grid)

        # Since all sheets does not have outerborders. We draw a rectangle around the
        outer_border = np.array([
            [1, height-1],  # Bottom Left
            [1, 1],  # Top Left
            [width-1, 1],  # Top Right
            [width-1, height-1]  # Bottom Right
        ])
        cv2.drawContours(img_binary_grid, [outer_border], 0, (255, 255, 255), 3)

        # Remove the grid from the binary image an keep only the digits.
        img_binary_sheet_only_digits = cv2.bitwise_and(img_binary_sheet, 255 - img_binary_sheet_morphed)

        cv2.imshow("yatzy_grid_binary_lines", img_binary_grid)
        cv2.waitKey(0)
        
        return img_binary_grid, img_binary_sheet_only_digits

    def draw_lines(self, lines, img):
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 10000*(-b)), int(y0 + 10000*(a)))
                pt2 = (int(x0 - 10000*(-b)), int(y0 - 10000*(a)))
                cv2.line(img, pt1, pt2,
                        (255, 255, 255), 2)
        
        
    def merge_nearby_lines(self, lines, rho_distance=30, degree_distance=20):
        """ Merges nearby lines with the specified rho and degree distance.
        Args:
            lines (list): A list of lines (rho, theta), see OpenCV HoughLines
            rho_distance (int): Distance in rho for lines to merge (default is 30)
            degree_distacne (int): Distance in degrees for lines to merge (default is 20)
        Returns:
            list: a list of estimated lines
        """

        lines = lines if lines is not None else []
        estimated_lines = []
        for line in lines:
            if line is False:
                continue

            estimated_line = self.get_merged_line(
                lines, line, rho_distance, degree_distance)
            estimated_lines.append(estimated_line)

        return estimated_lines

    def get_merged_line(self, lines, line_a, rho_distance, degree_distance):
        """ Merges all line in lines with the distance to line_a iteratively.
        Returns:
            list: a list of estimated lines
        """
        for i, line_b in enumerate(lines):
            if line_b is False:
                continue
            if self.__should_merge_lines(line_a, line_b, rho_distance, degree_distance):
                # Update line A on every iteration
                line_a = self.merge_lines(line_a, line_b)
                # Don't use B again
                lines[i] = False

        return line_a



    def __should_merge_lines(self, line_a, line_b, rho_distance, theta_distance):
        rho_a, theta_a = line_a[0].copy()
        rho_b, theta_b = line_b[0].copy()
        if(rho_b == rho_a and theta_b == theta_b):
            return False

        # Use degree for more intuitive user format
        theta_b = int(180 * theta_b / np.pi)
        theta_a = int(180 * theta_a / np.pi)

        # In Q3 or Q4, See merge_lines method
        if rho_b < 0:
            theta_b = theta_b - 180

        # In Q3 or Q4, See merge_lines method
        if rho_a < 0:
            theta_a = theta_a - 180

        rho_a = np.abs(rho_a)
        rho_b = np.abs(rho_b)

        diff_theta = np.abs(theta_a - theta_b)
        rho_diff = np.abs(rho_a - rho_b)

        if(rho_diff < rho_distance and diff_theta < theta_distance):
            return True

        return False