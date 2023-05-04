import cv2
from DigitRecognizer import DigitRecognizer

#image = cv2.imread("cv/testImages/white_with_watermark.jpg")
#image = cv2.imread("cv/testImages/small_nrs.png")
image = cv2.imread("cv/testImages/kanti_img1.jpeg")
#image = cv2.imread("cv/testImages/kanti_img2.jpeg")
#image = cv2.imread("cv/testImages/corner_outside_frame.jpg",1)


recognizer = DigitRecognizer()
#cv2.imshow('image', image)
exam = recognizer.recognize_digits_in_photo(image)