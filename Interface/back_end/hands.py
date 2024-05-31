#imports
import cv2
import collections
import numpy as np
import mediapipe as mp
import time
from sklearn import neighbors
from matplotlib import pyplot as plt 
import pickle
import os as o


class MH:
    """
    A class used for hand tracking and gesture recognition using MediaPipe.

    :param buffer_size: The size of the buffer to store hand landmarks history.
    :type buffer_size: int, optional

    :ivar hands: An instance of MediaPipe Hands for hand landmark detection.
    :ivar his: A deque to store the history of hand landmarks.
    :ivar tmt: Track missing threshold.
    :ivar tmn: Track missing number.

    :method run: Processes an image to detect hand landmarks.
    :method drawlol: Draws landmarks and bounding box on the image.
    :method close: Closes the MediaPipe Hands instance.
    """
    def __init__(self, buffer_size=None):
        """
        Initializes the MH class with MediaPipe Hands and a deque for hand landmarks history.

        :param buffer_size: The size of the buffer to store hand landmarks history.
        :type buffer_size: int, optional
        """
        self.hands = mp.solutions.hands.Hands(
             min_tracking_confidence=0.9,
             min_detection_confidence=0.75
        )
        self.his = collections.deque(maxlen=None)

        self.tmt= 3
        self.tmn= 0

    def run(self, img):
        """
        Processes an image to detect hand landmarks.

        :param img: The input image in which to detect hand landmarks.
        :type img: numpy.ndarray
        :return: The result of the hand landmarks detection.
        :rtype: mediapipe.python.solutions.hands.Hands
        """
        img_width, img_height, _ = img.shape
        inpi = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        inpi.flags.writeable = False
        res = self.hands.process(cv2.cvtColor(inpi, cv2.COLOR_BGR2RGB))

        if res.multi_hand_landmarks:
            self.tmn = 0
            res_arr = np.asarray([[pt.x, pt.y] for pt in res.multi_hand_landmarks[0].landmark])
            self.his.append(res_arr)
        elif self.tmn < self.tmt:
            self.tmn += 1
        else:
            self.his.clear()
            self.tmn = 0
        plt.switch_backend('Agg')

        return res

    def drawlol(self, image, res, model):
        """
        Draws landmarks and bounding box on the image.

        :param image: The input image on which to draw.
        :type image: numpy.ndarray
        :param res: The result from the hand landmarks detection.
        :type res: mediapipe.python.solutions.hands.Hands
        :param model: The model used for gesture recognition.
        :type model: object
        :return: The image with drawn landmarks and bounding box.
        :rtype: numpy.ndarray
        """
        image_width, image_height, _ = image.shape
        #flip img
        new_img = cv2.flip(image, 1) 
        #check for landmarks
        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:
                #draww
                mp.solutions.drawing_utils.draw_landmarks(
                    new_img,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS
                )
                #get x and y coordinate
                x = [landmark.x for landmark in hand_landmarks.landmark]
                y = [landmark.y for landmark in hand_landmarks.landmark]

                #get center
                center = np.asarray([np.mean(x)*image_width*1.87, np.mean(y)*image_height*0.65]).astype('int32')
                #draw circle and box
                cv2.circle(new_img, tuple(center), 10, (225,150,255), 3)  #for checking the center 
                cv2.rectangle(new_img, (center[0]-200,center[1]-200), (center[0]+200,center[1]+200), (255,255,255), 5)
                #put text
                if self.his:
                    hshape = model.getshape(self.his[-1])
                    cv2.putText(new_img,hshape,(center[0]-250,center[1]-209), cv2.FONT_HERSHEY_COMPLEX,3, (225, 150, 255), 9, cv2.LINE_AA)

        return new_img
    

    def close(self):
        """
        Closes the MediaPipe Hands instance.
        
        :return: None
        """
        self.hands.close()
