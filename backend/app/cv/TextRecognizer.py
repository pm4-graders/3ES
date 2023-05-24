from easyocr import Reader
import argparse
import cv2
import time
from dateutil import parser


class TextRecognizer:

    def __init__(self, debug_mode=False):
        # initialize any variables
        global DEBUG_MODE
        DEBUG_MODE = debug_mode
        pass

    def recognize_text(self, image):
        """
        Recognizes exam info text in a photo.

        Parameters:
        Image: cv2.imread or similarly parsed image object

        Returns:
        The recognized text fields as string array
        """
        
        #Cut off top half of image
        image = image[:int(image.shape[0]/2), :]

        #Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #Resize the grid to scale to our wanted reference
        width = gray.shape[1]
        wanted_width = 2000
        scale_percent = wanted_width / width

        gray = cv2.resize(gray, (int(gray.shape[1] * scale_percent), int(gray.shape[0] * scale_percent)))

        reader = Reader(["de"], gpu=0)
        results = reader.readtext(gray, min_size=100, width_ths=1)

        recognized = [None] * 3

        for result in results:
            text = result[1]
            if("Prüf. " in text):
                recognized[0] = int(''.join(filter(str.isdigit, text)))
            if("Kand. " in text):
                recognized[1] = int(''.join(filter(str.isdigit, text)))
            if("Geb. " in text or "Dat." in text):
                date = parser.parse(text, fuzzy=True, dayfirst=True)
                recognized[2] = date

        return recognized

