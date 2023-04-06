import cv2
import base64
import numpy as np

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
        alignedPhoto = self.align_document(photo)

        # TODO: return dict with boolean and numbers for found digits.
        return alignedPhoto


    def align_document(self, img):

        # Resize image to workable size
        dim_limit = 2048
        max_dim = max(img.shape)
        if max_dim > dim_limit:
            resize_scale = dim_limit / max_dim
            img = cv2.resize(img, None, fx=resize_scale, fy=resize_scale)
        
        # Create a copy of resized original image for later use
        orig_img = img.copy()

        # Repeated Closing operation to remove text from the document.
        kernel = np.ones((5, 5), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=3)
        
        # GrabCut
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (20, 20, img.shape[1] - 20, img.shape[0] - 20)
        cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]
    
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)
        
        # Edge Detection.
        canny = cv2.Canny(gray, 0, 200)
        canny = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

        # Finding contours for the detected edges.
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # Keeping only the largest detected contour.
        page = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        
        # Blank canvas.
        # con = np.zeros_like(img)
        # con = cv2.drawContours(con, page, -1, (0, 255, 255), 3)
        # cv2.imshow('contours', con)
        
        # # Pause here 5 seconds.
        # k = cv2.waitKey(5000)

        # if k == 27:         # If escape was pressed exit
        #     cv2.destroyAllWindows()
        #     return


        # Detecting Edges through Contour approximation.
        # Loop over the contours.
        if len(page) == 0:
            return orig_img
        for c in page:
            # Approximate the contour.
            epsilon = 0.02 * cv2.arcLength(c, True)
            corners = cv2.approxPolyDP(c, epsilon, True)
            # If our approximated contour has four points.
            if len(corners) == 4:
                break
        
        # Sorting the corners and converting them to desired shape.
        corners = sorted(np.concatenate(corners).tolist())
        
        # For 4 corner points being detected.
        corners = self.order_points(corners)
    
        destination_corners = self.find_dest(corners)
    
        h, w = orig_img.shape[:2]
        
        # Getting the homography.
        M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))
        
        # Perspective transform using homography.
        final = cv2.warpPerspective(orig_img, M, (destination_corners[2][0], destination_corners[2][1]),
                                    flags=cv2.INTER_LINEAR)
        
        
        return final

    def order_points(self, pts):
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


    def find_dest(self, pts):
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
    
        return self.order_points(destination_corners)