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
        cv2.imshow('before',cv2.resize(aligned_photo, (700, 1000)))
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
        #cv2.drawContours(mask,[best_cnt],0,255,2)
        cv2.drawContours(mask,[best_cnt],0,255,-1)

        #Apply mask to copy of original image
        out = np.zeros_like(gray)
        out[mask == 255] = gray[mask == 255]

        #Out is already crayscale so we don't need to convert to grey but we need to blur it
        blur = cv2.GaussianBlur(out, (5,5), 0)

        #Apply adaptive threshold so we have independent illumination
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        
        horizontal = self.get_lines(thresh.copy(), (50,1), 100)
        vertical = self.get_lines(thresh.copy(), (1, 40), 80, False)

        out = cv2.bitwise_or(horizontal, vertical)

        cv2.imshow("out",cv2.resize(out, (700, 1000)))
        cv2.waitKey(0)


        #self.get_yatzy_grid(out)

    def get_lines(self, mat, kernel, min_line_size, is_horizontal = True):
        #Create structure element for extracting horizontal / vertical lines through morphology operations
        structure = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
        mat = cv2.erode(mat, structure)

        cv2.imshow("matuneroded",cv2.resize(mat, (700, 1000)))
        cv2.waitKey(0)

        #The horizontal / vertical structures have to be wide enough to be a line.
        contours, _ = cv2.findContours(mat, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if is_horizontal and w < min_line_size:
                cv2.drawContours(mat, [c], -1, (0,0,0), -1)
            if not is_horizontal and h < min_line_size:
                 cv2.drawContours(mat, [c], -1, (0,0,0), -1)

        cv2.imshow("matuneroded",cv2.resize(mat, (700, 1000)))
        cv2.waitKey(0)

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