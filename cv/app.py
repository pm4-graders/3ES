import cv2
from DigitRecognizer import DigitRecognizer


image = cv2.imread("C:/Users/TLAP/source/repos/ZHAW/3ES/cv/testImages/white_with_watermark.jpg")
#image = cv2.imread("C:/Users/TLAP/source/repos/ZHAW/3ES/cv/testImages/small_nrs.png")
#image = cv2.imread("C:/Users/TLAP/source/repos/ZHAW/3ES/cv/testImages/kanti_img1.jpg")
#image = cv2.imread("C:/Users/TLAP/source/repos/ZHAW/3ES/cv/testImages/kanti_img2.jpg")


recognizer = DigitRecognizer()
cv2.imshow('image', image)
finishedImage = recognizer.recognize_digits_in_photo(image)
cv2.imshow('finishedImage',finishedImage)

# Pause here 5 seconds.
k = cv2.waitKey(5000)

if k == 27:         # If escape was pressed exit
    cv2.destroyAllWindows()

input("bitch")