import cv2
import numpy
import keyboard

file = open("idcolor","rb")
identifiedColors = numpy.load(file)
file.close()

colors = [[51,153,255]                                             # list of possible drawn colors
          ,[255,0,255]
           ,[0,0,255]]

drawnPoints = []                                                   # list of all points on canvas

fps = 240

def empty(a):
    pass

def drawOnCanvas(Points,colors,radius,result):
    for point in Points:
        cv2.circle(result,(point[0],point[1]),radius,colors[point[2]],cv2.FILLED)


def getContours(original,result):
    contours,hierarchy = cv2.findContours(original,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1500:
            cv2.drawContours(result,contour,-1,(0,255,0),2)
            perimeter = cv2.arcLength(contour,closed=True)
            approx = cv2.approxPolyDP(contour,0.02*perimeter,closed=True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+(w//2),y,result


def findColor(original,radius,result):
    HSVimg = cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
    newPoints = []

    for color in identifiedColors:    
        lower = numpy.array(color[0:3])
        upper = numpy.array(color[3:6])
        drawColor = color[6]
        mask = cv2.inRange(HSVimg,lower,upper)

        x,y,result = getContours(mask,result)

        if x != 0 and y != 0:
           newPoints.append([x,y,drawColor])

    return newPoints,result  

def main():
    frameHeight = 640
    frameWidth = 480
   
   
    cam = cv2.VideoCapture(0)
    cam.set(3, frameWidth)
    cam.set(4, frameHeight)  
   
    cv2.namedWindow("options")
    cv2.resizeWindow("options",400,100)
    cv2.createTrackbar("fps","options",240,500,empty)
    cv2.createTrackbar("thickness","options",0,50,empty)
     
   
    while True:
           ret,frame = cam.read()
           if ret:
               fps = cv2.getTrackbarPos("fps","options")
               if fps == 0:
                   fps = 1
               radius = cv2.getTrackbarPos("thickness","options")
               result = frame.copy()   
   
               newPoints,result = findColor(frame,radius,result)
               wait = int((1/fps)*1000.00)
   
               if len(newPoints)!=0:
                   for point in newPoints:
                       drawnPoints.append(point)
   
               if len(drawnPoints)!=0:
                   drawOnCanvas(drawnPoints,colors,radius,result) 
   
   
               cv2.imshow("RESULT",result)
               if cv2.waitKey(wait) and keyboard.is_pressed('q'):
                   break
               
           else:
               break 
    
if __name__ == '__main__':
    main()
