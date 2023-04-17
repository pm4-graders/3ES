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
        
        self.debug_display_image('original',photo)
        
        if(True):
            segmentation = DocumentSegmentationCNN()
        else:
            segmentation = DocumentSegmentationCV()

        aligned_photo = segmentation.align_document(photo)
        
        self.debug_display_image('aligned',aligned_photo)
        
        grid = self.find_grid_in_image(aligned_photo)

        self.debug_display_image("grid_only", grid)

        grid_cells = self.get_grid_cells(grid)

        print(len(grid_cells))

        for cell in grid_cells:
            self.debug_display_image("cell", cell)

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
        #cv2.drawContours(mask,[best_cnt],0,255,2)
        cv2.drawContours(mask,[best_cnt],0,255,-1)

        #Apply mask to copy of original image
        out = np.zeros_like(gray)
        out[mask == 255] = gray[mask == 255]

        #The grid might be a bit warped so we want to fix this.
        out = self.fix_perspective(out, best_cnt)

        self.debug_display_image("out", out)

        #Out is already crayscale so we don't need to convert to grey but we need to blur it
        blur = cv2.GaussianBlur(out, (5,5), 0)

        #Apply adaptive threshold so we have independent illumination
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        
        horizontal = self.get_lines(thresh.copy(), (50,1), 100)
        vertical = self.get_lines(thresh.copy(), (1, 40), 80, False)

        eroded = cv2.bitwise_or(horizontal, vertical)

        #self.debug_display_image("beforeblur", eroded)

        #Blur the result a little bit so the lines are more prevalent
        cv2.blur(eroded, (7,7), eroded)
        _, eroded = cv2.threshold(eroded, 100, 255, cv2.THRESH_BINARY) #we can take anything that isn't really black.

        #self.debug_display_image("afterblur", eroded)

        return eroded

    def get_grid_cells(self, grid):
        
        def zoom_border(image, zoom):
            h, w = [ zoom * i for i in image.shape ]
                
            cx, cy = w/2, h/2
            
            image = cv2.resize( image, (0, 0), fx=zoom, fy=zoom)
            image = image[ int(round(cy - h/zoom * .5)) : int(round(cy + h/zoom * .5)),
                        int(round(cx - w/zoom * .5)) : int(round(cx + w/zoom * .5))]
            return image
        
        #Get vertical lines only
        vert = self.get_lines(grid.copy(), (1, 40), 80, False)
        
        #Zoom into the image so the outer borders are gone
        vert = zoom_border(vert, 1.1)
        
        contours, _ = cv2.findContours(vert, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        column_count = len(contours)+1

        result_cells = []
        invert = 255 - grid
        #self.debug_display_image("invert", invert)

        #Find contours of inverted 
        contours, _ = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Sort by top to bottom and each row by left to right
        (contours, _) = imutils_contours.sort_contours(contours, method="top-to-bottom")

        grid_rows = []
        row = []
        for (i, c) in enumerate(contours, 1):
            area = cv2.contourArea(c)
            if area > 4000:
                row.append(c)
                if i % column_count == 0:  
                    (contours, _) = imutils_contours.sort_contours(row, method="left-to-right")
                    grid_rows.append(contours)
                    row = []

        if len(grid_rows) != 3 or len(row) != 0:
            raise Exception("Grid cells not detected properly. There are not exactly three rows.")

        # Iterate through each box
        for row in grid_rows:
            for c in row:
                mask = np.zeros(grid.shape, dtype=np.uint8)
                cv2.drawContours(mask, [c], -1, (255,255,255), -1)
                result = cv2.bitwise_and(grid, mask)
                result[mask==0] = 255
                #self.debug_display_image("cell result", result)
                result_cells.append(result)

        return result_cells

    def get_lines(self, mat, kernel, min_line_size, is_horizontal = True):
        #Create structure element for extracting horizontal / vertical lines through morphology operations
        structure = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
        mat = cv2.erode(mat, structure)

        #self.debug_display_image("matuneroded",mat)

        #The horizontal / vertical structures have to be wide enough to be a line.
        contours, _ = cv2.findContours(mat, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if is_horizontal and w < min_line_size:
                cv2.drawContours(mat, [c], -1, (0,0,0), -1)
            if not is_horizontal and h < min_line_size:
                 cv2.drawContours(mat, [c], -1, (0,0,0), -1)

        #self.debug_display_image("matuneroded",mat)

        mat = cv2.dilate(mat, structure, iterations=4)
        return mat

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

    def fix_perspective(self, image, contours):
        
        def order_points(pts):
            '''Rearrange coordinates to order:
            top-left, top-right, bottom-right, bottom-left'''
            rect = np.zeros((4, 2), dtype='float32')
            pts = np.array(pts)
            s = pts.sum(axis=1)
            # Top-left point will have the smallest sum.
            rect[0] = pts[np.argmin(s)]
            # Bottom-right point will have the largest sum.
            rect[2] = pts[np.argmax(s)]
        
            diff = np.diff(pts, axis=1)
            # Top-right point will have the smallest difference.
            rect[1] = pts[np.argmin(diff)]
            # Bottom-left will have the largest difference.
            rect[3] = pts[np.argmax(diff)]
            # return the ordered coordinates
            return rect.astype('int').tolist()

        def find_dest(pts):
            (tl, tr, br, bl) = pts
            # Finding the maximum width.
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))
        
            # Finding the maximum height.
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))
            # Final destination co-ordinates.
            destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]
        
            return order_points(destination_corners)
        

        # Approximate the contour.
        epsilon = 0.02 * cv2.arcLength(contours, True)
        corners = cv2.approxPolyDP(contours, epsilon, True)
        # If our approximated contour has four points.
        if len(corners) != 4:
            raise Exception("Grid Contours not rectangular") 
        # Sorting the corners and converting them to desired shape.
        corners = sorted(np.concatenate(corners).tolist())
        # For 4 corner points being detected.
        corners = order_points(corners)
    
        destination_corners = find_dest(corners)
    
        # Getting the homography.
        M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))
        # Perspective transform using homography.
        final = cv2.warpPerspective(image, M, (destination_corners[2][0], destination_corners[2][1]),
                                    flags=cv2.INTER_LINEAR)

        return final

    def debug_display_image(self, name, image):
        cv2.imshow(name, cv2.resize(image, (int(image.shape[1]/3), int(image.shape[0]/3))))
        cv2.waitKey(0)