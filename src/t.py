import cv2

cap = cv2.VideoCapture(0)
# Check if the capture properties were set correctly (optional)
cap.set(3, 1500)
cap.set(4, 864)
capture_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) #
capture_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) #
print(f"Capture width: {capture_width}, Capture height: {capture_height}")

while True:
    message = None
    success, img = cap.read()
    cv2.imshow("Img", img)
    cv2.waitKey(1)
