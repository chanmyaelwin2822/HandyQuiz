import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
alpha = 0
imgtype = ['jpg','png','jpeg']
class MCQ(object):
    def __init__(self,data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None

    def update(self, cursor, bboxs):

        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

class CAT() :
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.userAns = None

    def update(self, cursor, bboxs):

        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

# Import csv file data
def read_csv(pathCSV):
    with open(pathCSV, newline='\n') as f:
        reader = csv.reader(f)
        dataAll = list(reader)[1:]
    return dataAll


pathCSV = "category.csv"
catData = read_csv(pathCSV)

# Create Object for each MCQ
catList = []
for c in catData:
    catList.append(CAT(c))

print("Total category Objects Created:", len(catList))
cNo = 0
cTotal = len(catData)
current_category = None
def setcsv(category) :
    if(category == 1):
        return 'Mcqs.csv'
    if(category == 2):
        return 'Mcqs1.csv'
    if (category == 2):
        return 'Mcqs1.csv'

def choice(catList,cNo,img,hands,detector):
    cat = catList[cNo]

    img, bbox = cvzone.putTextRect(img, cat.question, [100, 100], 2, 2, offset=50, border=5, colorR=(255, 255, 255), colorT=(0, 0, 0))
    img, bbox1 = cvzone.putTextRect(img, cat.choice1, [100, 250], 2, 2, offset=50, border=5, colorR=(220, 26, 91))
    img, bbox2 = cvzone.putTextRect(img, cat.choice2, [400, 250], 2, 2, offset=50, border=5, colorR=(220, 26, 91))
    img, bbox3 = cvzone.putTextRect(img, cat.choice3, [100, 400], 2, 2, offset=50, border=5, colorR=(220, 26, 91))

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
            cat.update(cursor, [bbox1, bbox2, bbox3])
            if cat.userAns is not None:
                current_category = cat.userAns
                return current_category

def answer(mcq,img,hands,detector):
    if (any(element in mcq.question for element in imgtype)):
        foreground = cv2.imread(mcq.question)
        width = 200
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
        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5)
    img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)
    img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)
    img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)
    img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)
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
            mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
            if mcq.userAns is not None:
                time.sleep(0.8)
                return mcq.userAns


mcqList = []
mcqData = None
qNo = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if current_category is None:
        current_category = choice(catList, cNo, img, hands,detector)
    else:
        if(mcqData is None):
            pathCSV = setcsv(current_category)
            mcqData = read_csv(pathCSV)
            for q in mcqData:
                mcqList.append(MCQ(q))
            print("Total MCQ Objects Created:", len(mcqList))
            qTotal = 4

        else:
            if qNo < len(mcqData):
                mcq = mcqList[qNo]
                useranswer = answer(mcq, img, hands, detector)
                if(useranswer is not None):
                    qNo += 1
            else:
                score = 0
                for mcq in mcqList:
                    if mcq.answer == mcq.userAns:
                        score += 1
                score = round((score / qTotal) * 100, 2)
                img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [500, 300], 2, 2, offset=50, border=5)

        # Draw Progress Bar
        # barValue = 150 + (950 // qTotal) * qNo
        # cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
        # cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
        # img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)
    cv2.imshow("Img", img)
    cv2.waitKey(1)