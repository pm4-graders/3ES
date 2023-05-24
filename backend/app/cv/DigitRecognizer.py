import cv2
import base64
import numpy as np
from imutils import contours as imutils_contours

from cv.Models.mobilenet import MobileNet
import cv.Models.utils as utils
from cv.DocumentSegmentationCV import DocumentSegmentationCV
from cv.DocumentSegmentationCNN import DocumentSegmentationCNN
from cv.TextRecognizer import TextRecognizer
import core.cv_result as cv_res

class DigitRecognizer:
    
    global DEBUG_MODE

    def __init__(self, debug_mode=False):
        # initialize any variables
        global DEBUG_MODE
        DEBUG_MODE = debug_mode
        self.text_recognizer = TextRecognizer(debug_mode)
        pass
    
    def recognize_digits_in_photo(self, photo):
        """
        Recognize handwritten digits in a photo.

        Parameters:
        Photo: cv2.imread or similarly parsed photo object
        """
        global DEBUG_MODE
        
        if(DEBUG_MODE):
            self.debug_display_image('original',photo)
        
        if(True):
            segmentation = DocumentSegmentationCNN()
        else:
            segmentation = DocumentSegmentationCV()

        aligned_photo = segmentation.align_document(photo)
        
        if(DEBUG_MODE):
            self.debug_display_image('aligned',aligned_photo)
        
        recognized_text = self.text_recognizer.recognize_text(aligned_photo)

        print(recognized_text)

        grid_mask, grid = self.find_grid_in_image(aligned_photo)

        if(DEBUG_MODE):
            self.debug_display_image("grid_mask", grid_mask)

        grid_cells, column_count = self.get_grid_cells(grid, grid_mask)
        
        print(f"We have {str(len(grid_cells))} grid cells total")

        model = MobileNet()
        model.compile()
        model.load_weights('cv/Models/MobileNet.h5')
        class_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        exercises = []
        total_score = 0
        total_score_confidence = 0
        
        #Go through the grid cells column by column
        for index in range(int(len(grid_cells) / 3)):
            
            header_cell = grid_cells[index]
            points_cell = grid_cells[index + column_count]
            result_cell = grid_cells[index + 2*column_count]

            if(index % column_count == 0):
                #print("First, 'Erreichte Punkte text'")
                #TODO: OCR over header_cell, points_cell and result_cell and check that they say the right thing.
                pass

            if(index % column_count > 0 and index % column_count < column_count-1):
                #print("Handwritten Cell")
                
                if DEBUG_MODE and index == 1:
                    self.debug_display_image("cell", result_cell)
                
                pred_class_label, pred_confidence = self.predict_handwritten_cell(result_cell, class_labels, model)

                exercises.append(cv_res.Exercise(index, pred_class_label, pred_confidence, 0))  # TODO replace 0 with max_score
            elif(index % column_count != 0):
                #print("Last Handwritten Cell, 'Total'")

                total_score, total_score_confidence = self.predict_double_number(result_cell, class_labels, model)

        exam = cv_res.Exam(2023, "Mathematik", total_score, total_score_confidence, exercises)  # TODO replace year & subject & add exam id from recognized_text[1]

        return cv_res.CVResult(cv_res.Candidate(recognized_text[0], recognized_text[2]), exam=exam) 


    def predict_double_number(self, original_cell, class_labels, model):
        blur = cv2.GaussianBlur(original_cell, (3,3), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        #Find the largest contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        found_numbers = []
        for contour in contours:
            #Filter out very small contours (noise)
            if(cv2.contourArea(contour) < 100):
                continue

            (x,y,w,h) = cv2.boundingRect(contour)
            res = thresh[y:y+h, x:x+w]
            totalHeight = h + 40
            widthToAdd = int((totalHeight - w) / 2)
            res = cv2.copyMakeBorder(res, 20, 20, widthToAdd, widthToAdd, cv2.BORDER_CONSTANT, value=(0,0,0))
            class_label, class_confidence = self.predict_handwritten_cell(res, class_labels, model, False)

            #cv2.imshow("Handwritten Digit", res)
            #cv2.waitKey(0)
            found_numbers.append((class_label, class_confidence))
        
        if(found_numbers == 0):
            return 0, 0

        result = ""
        confidence_sum = 0
        for number, confidence in found_numbers:
            result += str(number)
            confidence_sum += confidence

        confidence_average = confidence_sum/len(found_numbers)

        return int(result), confidence_average

    def predict_handwritten_cell(self, original_cell, class_labels, model, do_thresh=True):
            if(do_thresh):
                #Apply adaptive threshold so we have independent illumination
                _, tcell = cv2.threshold(original_cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            else:
                tcell = original_cell
            
            tcell = cv2.resize(tcell, (28,28))

            if(DEBUG_MODE):
                cv2.imshow("show", tcell)
                cv2.waitKey(0)

            tcell = np.expand_dims(tcell, axis=(0, -1))
            tcell = utils.normalize_images(tcell)

            prediction = model.predict(tcell, verbose=0)
            #print(prediction)

            # Get the index of the highest probability
            predicted_class_index = np.argmax(prediction)

            # Get the corresponding class label
            predicted_class_label = class_labels[predicted_class_index]

            # Print the predicted class label
            #print("The predicted class is:", predicted_class_label)

            return int(predicted_class_label), prediction[0][predicted_class_index]

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

        #Resize the grid to scale to our wanted reference
        width = out.shape[1]
        wanted_width = 2000
        scale_percent = wanted_width / width

        out = cv2.resize(out, (int(out.shape[1] * scale_percent), int(out.shape[0] * scale_percent)))

        if(DEBUG_MODE):
            self.debug_display_image("Grid, perspective fixed and resized", out)

        #Out is already crayscale so we don't need to convert to grey but we need to blur it
        blur = cv2.GaussianBlur(out, (7,7), 0)

        #Apply adaptive threshold so we have independent illumination
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        
        horizontal = self.get_lines(thresh.copy(), (70,1), 80)
        vertical = self.get_lines(thresh.copy(), (1, 50), 70, False)

        eroded = cv2.bitwise_or(horizontal, vertical)

        if DEBUG_MODE:
            self.debug_display_image("grid mask, before blur", eroded)

        #Blur the result a little bit so the lines are more prevalent
        cv2.blur(eroded, (7,7), eroded)
        _, eroded = cv2.threshold(eroded, 100, 255, cv2.THRESH_BINARY) #we can take anything that isn't really black.

        if DEBUG_MODE:
            self.debug_display_image("grid mask, after blur", eroded)

        return eroded, out

    def get_grid_cells(self, grid, grid_mask):
        
        def zoom_border(image, zoom):
            h, w = [ zoom * i for i in image.shape ]
                
            cx, cy = w/2, h/2
            
            image = cv2.resize( image, (0, 0), fx=zoom, fy=zoom)
            image = image[ int(round(cy - h/zoom * .5)) : int(round(cy + h/zoom * .5)),
                        int(round(cx - w/zoom * .5)) : int(round(cx + w/zoom * .5))]
            return image
        
        #Get vertical lines only
        vert = self.get_lines(grid_mask.copy(), (1, 50), 70, False)
        
        #Zoom into the image so the outer borders are gone
        vert = zoom_border(vert, 1.1)

        contours, _ = cv2.findContours(vert, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        column_count = len(contours)+1

        result_cells = []
        invert = 255 - grid_mask

        if(DEBUG_MODE):
            self.debug_display_image("inverted", invert)

        #Find contours of inverted 
        contours, _ = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Sort by top to bottom and each row by left to right
        (contours, _) = imutils_contours.sort_contours(contours, method="top-to-bottom")

        grid_rows = []
        row = []
        for (i, c) in enumerate(contours, 1):
            area = cv2.contourArea(c)
            if area > 3000:
                row.append(c)
                if i % column_count == 0:  
                    (conts, _) = imutils_contours.sort_contours(row, method="left-to-right")
                    grid_rows.append(conts)
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
                
                x,y,w,h = cv2.boundingRect(c)
                result = result[y:y+h, x:x+w]

                #self.debug_display_image("cell result", result)
                result_cells.append(result)

        return result_cells, column_count

    def get_lines(self, mat, kernel, min_line_size, is_horizontal = True):
        #Create structure element for extracting horizontal / vertical lines through morphology operations
        structure = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
        mat = cv2.erode(mat, structure)

        #The horizontal / vertical structures have to be wide enough to be a line.
        contours, _ = cv2.findContours(mat, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if is_horizontal and w < min_line_size:
                cv2.drawContours(mat, [c], -1, (0,0,0), -1)
            if not is_horizontal and h < min_line_size:
                 cv2.drawContours(mat, [c], -1, (0,0,0), -1)
        
        if(DEBUG_MODE):
            self.debug_display_image("eroded structures",mat)

        mat = cv2.dilate(mat, structure, iterations=50)

        if(DEBUG_MODE):
            self.debug_display_image("dilated structures",mat)

        mat = cv2.dilate(mat, cv2.getStructuringElement(cv2.MORPH_RECT, (2,2)))

        if(DEBUG_MODE):
            self.debug_display_image("'blurred', dilated structures",mat)
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