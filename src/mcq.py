import utils as util
from cvzone.HandTrackingModule import HandDetector
import cvzone
import cv2
import time
alpha = 0

class MCQ(object):
    def __init__(self,data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None

    def update(self, cursor, bboxs, img):

        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

def answer_mcq(mcq,img,hands,detector):
    if (any(element in mcq.question for element in util.imgtype)):
        foreground = cv2.imread("./resources/"+mcq.question)
        width = 250
        height = 100
        foreground = cv2.resize(foreground, (width, height))
        # Create a mask of logo
        # New position for the overlay (top-left corner)
        top_left_row = 50
        top_left_col = 50

        # Calculate the bottom right corner based on the size of the foreground image
        bottom_right_row = top_left_row + foreground.shape[0]
        bottom_right_col = top_left_col + foreground.shape[1]

        # Apply the addWeighted function with the new position
        added_image = cv2.addWeighted(
            img[top_left_row:bottom_right_row, top_left_col:bottom_right_col, :], alpha, foreground, 1 - alpha,
            0)


        # Change the region with the result
        img[top_left_row:bottom_right_row, top_left_col:bottom_right_col, :] = added_image
        # # For displaying current value of alpha(weights)
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(img, 'alpha:{}'.format(alpha), (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.imshow(added_image)
    else:
        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5, colorR=(255, 255, 255), colorT=(0, 0, 0))
    img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5, colorR=(220, 26, 91))
    img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [500, 250], 2, 2, offset=50, border=5, colorR=(220, 26, 91))
    img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5, colorR=(220, 26, 91))
    img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [500, 400], 2, 2, offset=50, border=5, colorR=(220, 26, 91))
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
            mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4],img)
            if mcq.userAns is not None:
                time.sleep(0.8)
                return mcq.userAns

