import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
import category as category
import utils as util
import mcq as m
from menu import *
from exit import *

import pygame
# Initialization
current_category = None
mcqData          = None
mcqList          = []
qNo              = 0
qTotal           = 0
running          = True
start            = None
alpha = 0

# Read csv data from category files
catData = util.read_csv(util.category_CSV)

# Open Webcam and define settings
cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

message_duration = 15
# Start time for the current message
message_start_time = time.time()

pygame.mixer.init()  # initialise the pygame


def play(message):
    if message == 'Try Hard':
        pygame.mixer.music.load("./resources/wronganswer.mp3")
    else:
        pygame.mixer.music.load("./resources/correct.mp3")
    pygame.mixer.music.play(loops=0)

# Main process
while running:
    message = None
    success, img = cap.read()

    cv2.namedWindow("img", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("img", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # Start
    # if start is None:
    #     start = choose_menu('start', img, hands,detector)
    # else:

    if current_category is None:
        current_category = category.choose_category(catData[0], img, hands,detector)
    else:
        if(mcqData is None):

            # Set and Read csv file on current_category
            pathCSV = util.setcsv(current_category)
            mcqData = util.read_csv(pathCSV)

            # Create MCQ objects
            for q in mcqData:
                mcqList.append(m.MCQ(q))
            # print("Total MCQ Objects Created:", len(mcqList))
            qTotal = len(mcqData)

        else:
            if qNo < qTotal:
                mcq = mcqList[qNo]
                useranswer = m.answer_mcq(mcq, img, hands, detector)
                if(useranswer is not None):
                    if useranswer == mcq.answer:
                        message = "You're great"

                    else:
                        message = "Try Hard"

                    play(message)
                    # Check if it's time to switch to the next message
                    qNo += 1


                    # time.sleep(2)  # Add a 2-second delay before showing the next question
            else:
                score = 0
                for mcq in mcqList:
                    if mcq.answer == mcq.userAns:
                        score += 1
                score = round((score / qTotal) * 100, 2)
                img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [200, 300], 2, 2, offset=50, border=5,  colorR=(255, 255, 255), colorT=(0, 0, 0))
                if (exit(MENU(), img, hands, detector)):
                    cv2.waitKey(1)
                    cv2.destroyWindow(img)

                

                #img, _ = cvzone.putTextRect(img, 'Exit', [800, 300], 2, 2, offset=50, border=5)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#         # Draw Progress Bar
#         # barValue = 150 + (950 // qTotal) * qNo
#         # cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
#         # cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
#         # img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)
    cv2.imshow("Img", img)
    cv2.waitKey(1)