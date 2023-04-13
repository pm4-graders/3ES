import cv2
import base64
import numpy as np
from DocumentSegmentationCV import DocumentSegmentationCV
from DocumentSegmentationCNN import DocumentSegmentationCNN

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
        cv2.drawContours(mask,[best_cnt],0,255,-1)
        cv2.drawContours(mask,[best_cnt],0,0,2)

        #Apply mask to copy of original image
        out = np.zeros_like(gray)
        out[mask == 255] = gray[mask == 255]

        #Apply same transformation to grid
        blur = cv2.GaussianBlur(out, (5,5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Define the aspect ratio range for small squares
        aspect_ratio_min = 0.6
        aspect_ratio_max = 1.2

        min_height = out.shape[0] / 6
        max_height = out.shape[0] / 2
        min_width = out.shape[1] / 15
        max_width = out.shape[1] / 10

        min_area = min_height * min_width
        max_area = max_height * max_width

        cv2.drawContours(out, contours, -1, (0,255,0), 3)
        cv2.imshow("contours", out)
        cv2.waitKey(0)

        # Iterate over each inner grid contour and extract the small square images
        for contour in contours:
                        
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            if cv2.contourArea(contour) < min_area or cv2.contourArea(contour) > max_area:
                continue

            # Extract the small square image
            square_img = out[y:y+h, x:x+w]
            # Do something with the small square image (e.g., save it to a file)
            cv2.imshow("square_image.jpg", square_img)
            cv2.waitKey(0)

            #Filter out contours that are less or more than defined minmax widthheights
            if (h < min_height or h > max_height) or (w < min_width or w > max_width):
                continue

            # Calculate the aspect ratio of the bounding box
            aspect_ratio = float(w) / h
            
            # Filter out contours that have an aspect ratio outside the range of small squares
            if aspect_ratio < aspect_ratio_min or aspect_ratio > aspect_ratio_max:
                continue
            
            # Extract the small square image
            square_img = out[y:y+h, x:x+w]
            
            # Do something with the small square image (e.g., save it to a file)
            cv2.imshow("square_image.jpg", square_img)
            cv2.waitKey(0)

        # foundSquares = [contour for contour in contours if cv2.contourArea(contour) > 10]
        
        # c = 0
        # for i in contours:
        #         area = cv2.contourArea(i)
        #         if area > 1000/2:
        #             cv2.drawContours(image, contours, c, (0, 255, 0), 3)
        #         c+=1


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