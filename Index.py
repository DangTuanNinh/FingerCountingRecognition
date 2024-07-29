import cv2
import time
import os
import hand as htm

pTime = 0
cap = cv2.VideoCapture(0)
FolderPath = "Fingers"
lst = os.listdir(FolderPath)
lst_2 = []
for i in lst:
    img = cv2.imread(f"{FolderPath}/{i}")
    lst_2.append(img)

detector = htm.handDetector(detectionCon=1)
finger_id = [4,8,12,16,20]

while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lsList = detector.findPosition(frame,draw=False)
    print(lsList)

    if len(lsList) !=0:
        fingers = []

        if lsList[finger_id[0]][1] < lsList[finger_id[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for i in range(1,5):
            if lsList[finger_id[i]][2] < lsList[finger_id[i]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
    count_finger = fingers.count(1)
    print(count_finger)

    h, w, c = lst_2[count_finger-1].shape
    frame[0:h,0:w] = lst_2[count_finger-1]

    cv2.rectangle(frame,(0,200),(150,400),(0,255,0),-1)
    cv2.putText(frame,str(count_finger),(20,390),cv2.FONT_ITALIC,5,(255,0,0),5)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(frame,f"FPS: {int(fps)}", (150,70),cv2.FONT_ITALIC,2,(255,0,0),2)

    cv2.imshow("Window",frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyWindow()