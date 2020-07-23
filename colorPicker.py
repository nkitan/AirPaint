import cv2
import numpy 

def empty(a):
     pass

fps = 30
wait = int((1/fps)*1000.00)
Results = []
Cid = 1

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cv2.namedWindow("OPTIONS")
cv2.resizeWindow("OPTIONS",400,290)

cv2.createTrackbar("Hue <","OPTIONS",0,179,empty)
cv2.createTrackbar("Hue >","OPTIONS",0,179,empty)
cv2.createTrackbar("Sat <","OPTIONS",0,255,empty)
cv2.createTrackbar("Sat >","OPTIONS",0,255,empty)
cv2.createTrackbar("Val <","OPTIONS",0,255,empty)
cv2.createTrackbar("Val >","OPTIONS",0,255,empty)

while True:
 ret,frame = cap.read()
 if ret:
    current = frame.copy()
    HSVimg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hmin = cv2.getTrackbarPos("Hue <","OPTIONS")
    hmax = cv2.getTrackbarPos("Hue >","OPTIONS")
    smin = cv2.getTrackbarPos("Sat <","OPTIONS")
    smax = cv2.getTrackbarPos("Sat >","OPTIONS")
    vmin = cv2.getTrackbarPos("Val <","OPTIONS")
    vmax = cv2.getTrackbarPos("Val >","OPTIONS")

    lower = numpy.array([hmin,smin,vmin])
    upper = numpy.array([hmax,smax,vmax])
    mask = cv2.inRange(HSVimg,lower,upper)

    result = cv2.bitwise_and(current,current,mask=mask)
    cv2.imshow("RESULT",result)
    values = numpy.concatenate((lower,upper,Cid),axis=None)
    
    if cv2.waitKey(wait) & 0xFF == ord('v'):
        print(values)
        Results.append(values)
        Cid += 1
       
    if cv2.waitKey(wait) & 0xFF == ord('s'):
        print("{} SAVED!".format(Results))
        file = open("idcolor","wb")
        numpy.save(file,Results)
        file.close()
       
    if cv2.waitKey(wait) & 0xFF == ord('q'):
        break

    