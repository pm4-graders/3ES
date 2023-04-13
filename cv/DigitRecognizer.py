import cv2
import base64
import numpy as np
from DocumentSegmentatorCV import DocumentSegmentatorCV
from DocumentSegmentatorCNN import DocumentSegmentatorCNN

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
            segmentator = DocumentSegmentatorCNN()
        else:
            segmentator = DocumentSegmentatorCV()

        alignedPhoto = segmentator.align_document(photo)

        # TODO: return dict with boolean and numbers for found digits.
        return alignedPhoto
