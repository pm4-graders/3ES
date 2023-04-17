import cv2
from DigitRecognizer import DigitRecognizer


#image = cv2.imread("cv/testImages/white_with_watermark.jpg")
#image = cv2.imread("cv/testImages/small_nrs.png")
image = cv2.imread("cv/testImages/kanti_img1.jpeg")
#image = cv2.imread("cv/testImages/kanti_img2.jpeg")
#image = cv2.imread("cv/testImages/corner_outside_frame.jpg",1)


recognizer = DigitRecognizer()
#cv2.imshow('image', image)
finishedImage = recognizer.recognize_digits_in_photo(image)
cv2.imshow('finishedImage',cv2.resize(finishedImage, (700, 1000)))

cv2.waitKey(0)