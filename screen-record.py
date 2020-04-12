import sys
import time
import cv2
import mss
import numpy as np
import keyboard
from match import check_image
import pyautogui
# from mouse import moveMouse, mouseTo, withinGameBox

try:
    with mss.mss() as sct:
        # Part of the screen to capture
        # monitor = {"top": 0, "left": 0, "width": 640, "height": 480}
        monitor = {"top": 290, "left": 584, "width": 640, "height": 480}
        start_detect = False

        while "Screen capturing":
            last_time = time.time()

            if keyboard.is_pressed("m"):
                # get mouse position
                currentMouseX, currentMouseY = pyautogui.position()
                print(currentMouseX, currentMouseY)

            if keyboard.is_pressed("s"):
                start_detect = not start_detect
                print("s pressed", start_detect)

            if keyboard.is_pressed("q"):
                cv2.destroyAllWindows()
                break

            # Get raw pixels from the screen, save it to a Numpy array
            img_rgb = np.array(sct.grab(monitor))

            if start_detect:
                img_rgb = check_image(img_rgb, monitor)

            # Display the picture
            cv2.imshow("Screen Capture", img_rgb)
            cv2.waitKey(30)

            # print("fps: {}".format(1 / (time.time() - last_time)))

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
except KeyboardInterrupt:
    sys.exit()
