import cv2
import numpy as np
from matplotlib import pyplot as plt
from mouse import moveMouse, mouseTo, withinGameBox
from multiprocessing import Process

fruits_img = []

fruits = ["apple.png", "banana.png", "peach.png",
          "strawberry.png", "watermelon.png"]

for fruit in fruits:
    fruits_img.append(cv2.imread(fruit, 0))


def rotate_image(mat, angle):
    height, width = mat.shape[:2]  # image shape has 3 dimensions
    # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
    image_center = (width/2, height/2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat


def matchTemplate(img_gray, template, img_rgb, screen, game_box):
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.85
    loc = np.where(res >= threshold)
    a = np.array(loc)

    if a.size > 0:
        print('found', a.size)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        mouse_top_left = (top_left[0] / 2, top_left[1] / 2)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        mouse_bottom_right = (bottom_right[0] / 2, bottom_right[1] / 2)
        # cv2.rectangle(img_rgb, top_left, bottom_right, 255, 2)
        within = withinGameBox(game_box)
        if within:
            # mouseTo({"x":  screen["left"] + mouse_top_left[0],
            #          "y": screen["top"] + mouse_top_left[1]})
            moveMouse({"x": screen["left"] + mouse_top_left[0], "y": screen["top"] + mouse_top_left[1]},
                      {"x": screen["left"] + mouse_bottom_right[0], "y": screen["top"] + mouse_bottom_right[1]})
    return img_rgb


def check_image(img_rgb, screen):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    padding = 10
    game_box = {
        "x1": screen["left"] + padding,
        "y1": screen["top"] + padding,
        "x2": screen["left"] + screen["width"] + padding,
        "y2": screen["top"] + screen["height"] + padding
    }
    proc = []
    for template in fruits_img:
        p = Process(target=matchTemplate, args=(
            img_gray, template, img_rgb, screen, game_box))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()
    return img_rgb

# def check_image(img_rgb, screen):
#     img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
#     fruits = ["apple.png", "banana.png", "peach.png",
#               "strawberry.png", "watermelon.png"]
#     for fruit in fruits:
#         template = cv2.imread(fruit, 0)
#         res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # threshold = 0.85
    # loc = np.where(res >= threshold)
    # a = np.array(loc)

#         if a.size > 0:
#             w, h = template.shape[::-1]
#             print('found match', fruit)

    # game_box = {
    #     "x1": screen["left"],
    #     "y1": screen["top"],
    #     "x2": screen["left"] + screen["width"],
    #     "y2": screen["top"] + screen["height"]
    # }

#             for pt in zip(*loc[::-1]):
#                 cv2.rectangle(
#                     img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
#                 within = withinGameBox(game_box)
#                 if within:
#                     print(pt)
#                     print(screen["left"] + pt[0])
#                     print(screen["top"] + pt[1])

#                     # mouseTo({"x":  screen["left"] + (pt[1] / 2),
#                     #          "y":  screen["top"] + pt[0]})

    # moveMouse({"x": screen["left"] + pt[0], "y": screen["top"] + pt[1]},
    #           {"x": screen["left"] + pt[0] + w, "y": screen["top"] + pt[1] + h})

#     return img_rgb

# For more accurate detection, but slow down performance
# img_rgb = cv2.imread('full5.png')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# template = cv2.imread('apple.png', 0)

# for i in range(360):
#     rotated = rotate_image(template, i)
#     res = cv2.matchTemplate(img_gray, rotated, cv2.TM_CCOEFF_NORMED)
#     threshold = 0.85
#     loc = np.where(res >= threshold)
#     a = np.array(loc)

#     if a.size == 0:
#         continue
#     w, h = rotated.shape[::-1]
#     for pt in zip(*loc[::-1]):
#         cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
#     cv2.imshow('rotated', rotated)
#     cv2.imshow('res.png', img_rgb)
#     cv2.waitKey()
#     break
