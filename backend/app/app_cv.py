import cv2
import time
from cv.DigitRecognizer import DigitRecognizer

IMAGEDIR = "cv/testImages/"

images = []

images.append(cv2.imread(IMAGEDIR + "kanti_img1.jpeg"))
images.append(cv2.imread(IMAGEDIR + "kanti_img2.jpeg"))
images.append(cv2.imread(IMAGEDIR + "kanti_telegram_compressed_1.jpg"))
images.append(cv2.imread(IMAGEDIR + "kanti_telegram_compressed_2.jpg"))
images.append(cv2.imread(IMAGEDIR + "straight.jpg"))
images.append(cv2.imread(IMAGEDIR + "perspective.jpg"))
images.append(cv2.imread(IMAGEDIR + "crooked.jpg"))
images.append(cv2.imread(IMAGEDIR + "lighting.jpg"))
images.append(cv2.imread(IMAGEDIR + "mirror.jpg"))
images.append(cv2.imread(IMAGEDIR + "multiple.jpg"))
images.append(cv2.imread(IMAGEDIR + "rug.jpg"))
images.append(cv2.imread(IMAGEDIR + "wavy.jpg"))
images.append(cv2.imread(IMAGEDIR + "weird_bg.jpg"))
images.append(cv2.imread(IMAGEDIR + "crunched.jpg"))


recognizer = DigitRecognizer()

cv_result = recognizer.recognize_digits_in_photo(images[1])

#cv2.imshow('image', image)
for index, image in enumerate(images):
    start = time.time()
    try:
        cv_result = recognizer.recognize_digits_in_photo(image)
        print(', '.join([str(exercise.score) for exercise in cv_result.exam.exercises]) + " | Total: " + str(cv_result.exam.score))

        print("IMAGE " + str(index+1) + " PASSED")
    except Exception as e:
        print(e)
        print("IMAGE " + str(index+1) + " DID NOT PASS")
        pass
    end = time.time()
    print(end - start)
