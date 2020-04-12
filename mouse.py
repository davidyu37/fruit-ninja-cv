import pyautogui

# Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
screenWidth, screenHeight = pyautogui.size()
# Returns two integers, the x and y of the mouse cursor's current position.
currentMouseX, currentMouseY = pyautogui.position()
print(screenWidth, screenHeight, currentMouseX, currentMouseY)


def moveMouse(start, finish):
    pyautogui.mouseUp(button="left")
    pyautogui.moveTo(start["x"], start["y"])
    pyautogui.mouseDown()
    # pyautogui.moveTo(finish["x"], finish["y"])
    pyautogui.dragTo(finish["x"], finish["y"], 1, button='left')
    pyautogui.mouseUp(button="left")


def mouseTo(point):
    pyautogui.moveTo(point["x"], point["y"])


def withinGameBox(screen):
    currentMouseX, currentMouseY = pyautogui.position()
    if currentMouseX < screen['x1'] or \
       currentMouseY < screen['y1'] or \
       currentMouseX > screen['x2'] or \
       currentMouseY > screen['y2']:
        # Out of game box
        return False
    return True
