import cv2
import argparse

ap = argparse.ArgumentParser(description='Выбор диапазона по цвету')
ap.add_argument("-r", "--range", type = int, required = False, help="Определение параметров RGB.")
args = vars(ap.parse_args())

# Калибровка по цвету
def range(camera):

    def nothing(x):
        pass

    cap = cv2.VideoCapture(camera)
    cv2.namedWindow('result')

    cv2.createTrackbar('minb', 'result', 0, 255, nothing)
    cv2.createTrackbar('ming', 'result', 0, 255, nothing)
    cv2.createTrackbar('minr', 'result', 0, 255, nothing)

    cv2.createTrackbar('maxb', 'result', 0, 255, nothing)
    cv2.createTrackbar('maxg', 'result', 0, 255, nothing)
    cv2.createTrackbar('maxr', 'result', 0, 255, nothing)

    while(cap.isOpened()):
        _, frame = cap.read()
        #img = cv2.imread("1.jpg")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('hsv', hsv)

        minb = cv2.getTrackbarPos('minb', 'result')
        ming = cv2.getTrackbarPos('ming', 'result')
        minr = cv2.getTrackbarPos('minr', 'result')

        maxb = cv2.getTrackbarPos('maxb', 'result')
        maxg = cv2.getTrackbarPos('maxg', 'result')
        maxr = cv2.getTrackbarPos('maxr', 'result')

        mask = cv2.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))
        cv2.imshow('mask', mask)
        result = cv2.bitwise_and(frame, frame, mask = mask)
        cv2.imshow('result', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # запись границ оласти цвета в файл
            handle = open("color_range.py", "w")
            handle.write("MINB = " + str(minb) + "\n"
                        "MING = " + str(ming) + "\n"
                        "MINR = " + str(minr) + "\n"
                        "MAXB = " + str(maxb) + "\n"
                        "MAXG = " + str(maxg) + "\n"
                        "MAXR = " + str(maxr))
            handle.close()
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    if args["range"] is not None:
        range(args["range"])
