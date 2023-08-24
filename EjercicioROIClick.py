"""
Tarea dada el 03/08
Se tiene que seleccioanr una parte de la camara con el mouse, y se muestra
un roi en video de esa parte seleccionada

"""
import cv2
def select_roi(event, x, y, flags, param):
    global roi_selected, start_x, start_y, end_x, end_y

    if event == cv2.EVENT_LBUTTONDOWN:
        roi_selected = False
        start_x, start_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        end_x, end_y = x, y
        roi_selected = True

    elif event == cv2.EVENT_RBUTTONUP:
        start_x=start_y = end_x = end_y = -1
        roi_selected = False

cap = cv2.VideoCapture(0)
cv2.namedWindow("Video")
cv2.setMouseCallback("Video", select_roi)

roi_selected = False
start_x, start_y, end_x, end_y = -1, -1, -1, -1
while(True):
    _,frame = cap.read()



    cv2.imshow("Video", frame)


    if roi_selected and end_x>start_x and end_y>start_y:
        pt1 = (start_x, start_y)
        pt2= (end_x, end_y)
        roi = frame[start_y: end_y, start_x:end_x]
        cv2.imshow("roi", roi)
    elif cv2.getWindowProperty("roi", cv2.WND_PROP_VISIBLE) == 1:
        cv2.destroyWindow("roi")





    if cv2.waitKey(1) & 0xFF==ord('r'):
        roi = cv2.selectROIs("roi", frame)
        continue


    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()