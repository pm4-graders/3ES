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

        self.reader = Reader(["de"], gpu=0)

        pass

    def recognize_text(self, image, config):
        """
        Recognizes exam info text in a photo.

        Parameters:
        Image: cv2.imread or similarly parsed image object

        Returns:
        The recognized text fields as string array
        """
        global DEBUG_MODE

        if DEBUG_MODE:
            cv2.imshow("orig", cv2.resize(image, (int(image.shape[1] / 3), int(image.shape[0] / 3))))
            cv2.waitKey(0)

        #Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #Resize the grid to scale to our wanted reference
        gray = cv2.resize(gray, (1400, 2000), interpolation = cv2.INTER_AREA)

        #Cut off top half of image as we don't need it
        gray = gray[:int(gray.shape[0]/2), :]

        recognized = [None] * 5

        for attribute, value in config.__dict__.items():

            x,y = value['top_left']
            x1,y1 = value['bottom_right']

            input = gray[y:y1,x:x1]

            if DEBUG_MODE:
                cv2.imshow("cut", cv2.resize(input, (int(input.shape[1]), int(input.shape[0]))))
                cv2.waitKey(0)

            results = self.reader.readtext(input, min_size=100, width_ths=1.3)
            
            for result in results:
                text = result[1]
            
                if attribute == "sticker":
                    if("Prüf. " in text):
                        recognized[0] = int(''.join(filter(str.isdigit, text)))
                    if("Kand. " in text):
                        recognized[1] = int(''.join(filter(str.isdigit, text)))
                    if("Geb. " in text or "Dat." in text):
                        try:
                            date = parser.parse(text, fuzzy=True, dayfirst=True)
                        except:
                            date = None
                        recognized[2] = date
                
                if attribute == "year_with_text":
                    if("Aufnahme" in text):
                        recognized[3] = int(''.join(filter(str.isdigit, text)))
                if attribute == "test_name":
                    if not("ohne" in text or "Tasch" in text or "rechner" in text):
                        recognized[4] = text

        return recognized

    def recognize_grid_number(self, image):
        """
        Recognizes a grid number.

        Parameters:
        Image: cv2.imread or similarly parsed image object

        Returns:
        The recognized text fields as string array
        """
        res = self.reader.readtext(image, min_size=10)
        if len(res) != 0:
            res = int(''.join(filter(str.isdigit, res[0][1])))
        else:
            res = None
        return res
