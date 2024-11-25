import pygame
import sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

WINSIZEX = 640
WINSIZEY = 480

BOUNDRYINC = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

IMGSAVE = False

MODEL = load_model('Aikins_cnn_model.keras')

LABELS = {0: 'Zero', 1: 'One',
          2: 'Two', 3: 'Three',
          4: 'Four', 5: 'Five',
          6: 'Six', 7: 'Seven',
          8: 'Eight', 9: 'Nine'}

pygame.init()

FONT = pygame.font.Font("freesansbold.ttf", 18)
DISPLAYSURF = pygame.display.set_mode((WINSIZEX, WINSIZEY))

pygame.display.set_caption('Digit Board')

iswriting = False

number_xcord = []
number_ycord = []

img_count = 1

PREDICT = True

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEMOTION and iswriting:
            xcord, ycord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4, 0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)

        if event.type == MOUSEBUTTONDOWN:
            iswriting = True

        if event.type == MOUSEBUTTONUP:
            iswriting = False
            number_xcord = sorted(number_xcord)
            number_ycord = sorted(number_ycord)

            rect_min_x = max(number_xcord[0] - BOUNDRYINC, 0)
            rect_max_x = min(number_xcord[-1] + BOUNDRYINC, WINSIZEX)
            rect_min_y = max(number_ycord[0] - BOUNDRYINC, 0)
            rect_max_y = min(number_ycord[-1] + BOUNDRYINC, WINSIZEY)

            # Add padding to avoid boundary issues
            PAD = 20
            rect_min_x = max(rect_min_x - PAD, 0)
            rect_max_x = min(rect_max_x + PAD, WINSIZEX)
            rect_min_y = max(rect_min_y - PAD, 0)
            rect_max_y = min(rect_max_y + PAD, WINSIZEY)

            img_arr = pygame.surfarray.array2d(DISPLAYSURF)
            img_arr = img_arr[rect_min_x:rect_max_x, rect_min_y:rect_max_y].astype(np.float32)

            if IMGSAVE:
                cv2.imwrite(f'image_{img_count}.png', img_arr)
                img_count += 1

            if PREDICT:
                # Resize the image to 28x28 pixels
                image = cv2.resize(img_arr, (28, 28))

                # Normalize the pixel values to [0, 1]
                image = image / 255.0

                # Optional: Apply dilation to thicken the strokes
                kernel = np.ones((3, 3), np.uint8)
                try:
                    image = cv2.dilate(image, kernel, iterations=1)
                except cv2.error as e:
                    print(f"OpenCV error during dilation: {e}")
                    print(f"Image shape: {image.shape}")
                    pygame.quit()
                    sys.exit()
                
                image = image.reshape(1, 28, 28, 1)

                # Predict the digit
                prediction = MODEL.predict(image)
                print(f"Prediction Probabilities: {prediction}")  # Debugging line
                label = str(LABELS[np.argmax(prediction)])

                textSurface = FONT.render(label, True, RED, WHITE)
                textRecObj = textSurface.get_rect()
                textRecObj.left, textRecObj.top = rect_min_x, rect_max_y
                DISPLAYSURF.blit(textSurface, textRecObj)

            number_xcord = []
            number_ycord = []

        if event.type == KEYDOWN:
            if event.unicode == "n":
                DISPLAYSURF.fill(BLACK)

    pygame.display.update()
