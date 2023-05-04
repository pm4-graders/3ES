import cv2
from DigitRecognizer import DigitRecognizer
import time

images = []

images.append(cv2.imread("cv/testImages/kanti_img1.jpeg"))
images.append(cv2.imread("cv/testImages/kanti_img2.jpeg"))
images.append(cv2.imread("cv/testImages/kanti_telegram_compressed_1.jpg"))
images.append(cv2.imread("cv/testImages/kanti_telegram_compressed_2.jpg"))
images.append(cv2.imread("cv/testImages/straight.jpg"))
images.append(cv2.imread("cv/testImages/perspective.jpg"))
images.append(cv2.imread("cv/testImages/crooked.jpg"))


recognizer = DigitRecognizer(True)
#cv2.imshow('image', image)
for index, image in enumerate(images):
    start = time.time()
    try:
        exam = recognizer.recognize_digits_in_photo(image)
        print("IMAGE" + str(index+1) + "PASSED")
    except:
        print("IMAGE" + str(index+1) + "DID NOT PASS")
        pass
    end = time.time()
    print(end - start)
