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
        cv2.drawContours(mask,[best_cnt],0,255,5)
        cv2.drawContours(mask,[best_cnt],0,255,-1)

        #Apply mask to copy of original image
        out = np.zeros_like(gray)
        out[mask == 255] = gray[mask == 255]

        #Apply same transformation to grid
        blur = cv2.GaussianBlur(out, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,57,5)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out all numbers and noise to isolate only boxes
        for c in contours:
            area = cv2.contourArea(c)
            # If area is really small, draw over it.
            if area < 1000:
                cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

        cv2.imshow('thresh', thresh)
        cv2.waitKey(0)

        # Fix horizontal and vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=6)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=6)

        cv2.imshow('thresh', thresh)
        cv2.waitKey(0)

        # Sort by top to bottom and each row by left to right
        invert = 255 - thresh
        cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        (cnts, _) = imutils_contours.sort_contours(cnts, method="top-to-bottom")

        sudoku_rows = []
        row = []
        for (i, c) in enumerate(cnts, 1):
            area = cv2.contourArea(c)
            if area < 50000:
                row.append(c)
                if i % 9 == 0:  
                    (cnts, _) = imutils_contours.sort_contours(row, method="left-to-right")
                    sudoku_rows.append(cnts)
                    row = []

        # Iterate through each box
        for row in sudoku_rows:
            for c in row:
                mask = np.zeros(image.shape, dtype=np.uint8)
                cv2.drawContours(mask, [c], -1, (255,255,255), -1)
                result = cv2.bitwise_and(image, mask)
                result[mask==0] = 255
                cv2.imshow('result', result)
                cv2.waitKey(0)


        cv2.imshow("Final Image", image)

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