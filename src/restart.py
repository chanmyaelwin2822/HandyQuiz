from cvzone.HandTrackingModule import HandDetector
import cvzone
import cv2
import pygame
class MENU(object) :
    def __init__(self):
        self.restart  = 'Restart'
        self.click = None

    def update(self, cursor, bboxs, img):

        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.click = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


def restart(menu, img,hands,detector):
    img, bbox = cvzone.putTextRect(img, menu.restart, [800, 900], 2, 2, offset=50, border=5, colorR=(255, 255, 255), colorT=(0, 0, 0))

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
            menu.update(cursor, [bbox], img)
            if menu.click is not None:
                pygame.mixer.music.load("./resources/click.mp3")
                pygame.mixer.music.play(loops=0)
                return True

