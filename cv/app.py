import cv2
from DigitRecognizer import DigitRecognizer


#image = cv2.imread("C:/Users/TLAP/source/repos/ZHAW/3ES/cv/testImages/white_with_watermark.jpg")
#image = cv2.imread("C:/Users/TLAP/source/repos/ZHAW/3ES/cv/testImages/small_nrs.png")
#image = cv2.imread("C:/Users/TLAP/source/repos/ZHAW/3ES/cv/testImages/kanti_img1.jpg")
image = cv2.imread("C:/Users/TLAP/source/repos/ZHAW/3ES/cv/testImages/kanti_img2.jpg")
#image = cv2.imread("C:/Users/TLAP/source/repos/ZHAW/3ES/cv/testImages/corner_outside_frame.jpg",1)


recognizer = DigitRecognizer()
#cv2.imshow('image', image)
finishedImage = recognizer.recognize_digits_in_photo(image)
cv2.imshow('finishedImage',finishedImage)

cv2.waitKey(0)