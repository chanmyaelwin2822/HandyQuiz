from cvzone.HandTrackingModule import HandDetector
import cvzone
import cv2
import time
import pygame
class CAT(object) :
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.userAns = None

    def update(self, cursor, bboxs, img):

        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


def choose_category(catData,img,hands,detector):
    cat = CAT(catData)
    img, bbox = cvzone.putTextRect(img, cat.question, [100, 100], 2, 2, offset=50, border=5, colorR=(255, 255, 255), colorT=(0, 0, 0))
    img, bbox1 = cvzone.putTextRect(img, cat.choice1, [100, 250], 2, 2, offset=50, border=5, colorR=(220, 26, 91))
    img, bbox2 = cvzone.putTextRect(img, cat.choice2, [650, 250], 2, 2, offset=50, border=5, colorR=(220, 26, 91))
    img, bbox3 = cvzone.putTextRect(img, cat.choice3, [950, 250], 2, 2, offset=50, border=5, colorR=(220, 26, 91))

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        index = []
        index.append(lmList[8][0])
        index.append(lmList[8][1])

        middle = []
        middle.append(lmList[12][0])
        middle.append(lmList[12][1])

        length, info = detector.findDistance(index, middle)
        print(length)
        if length < 35:
            cat.update(cursor, [bbox1, bbox2, bbox3], img)
            if cat.userAns is not None:
                current_category = cat.userAns
                pygame.mixer.music.load("./resources/click.mp3")
                pygame.mixer.music.play(loops=0)
                time.sleep(0.8)
                return current_category
