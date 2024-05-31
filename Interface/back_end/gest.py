# Ref: https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/hands.py
"Model definition and Traning main runner"
import cv2
import collections
import numpy as np
import mediapipe as mp
import time
from sklearn import neighbors
from matplotlib import pyplot as plt 
import pickle
import os as o
from hands import MH
from sklearn.ensemble import RandomForestClassifier


class Train:
    """
    A class used to train a RandomForestClassifier model on hand gesture data.

    :param data_folder: The folder containing the training data.
    :type data_folder: str

    :ivar clf: The RandomForestClassifier used for training and prediction.
    :ivar lb: A list of labels corresponding to the training data.

    :method getshape: Predicts the shape/gesture of the given hand landmarks.
    """
    def __init__(self, data_folder):
        """
        Initializes the Train class with a RandomForestClassifier classifier and trains it with data from the given folder.

        :param data_folder: The folder containing the training data.
        :type data_folder: str
        """
        self.clf = neighbors.KNeighborsClassifier(15) 
        t_x = []  
        t_y = []  
        self.lb = []  

        for i, df in enumerate(o.listdir(data_folder)):
            with open(o.path.join(data_folder, df), 'rb') as f:
                d = pickle.load(f)
                #train path
                for h in d:
                    t_y.append(i)
                    t_x.append((h - h[0]).flatten())
                self.lb.append(df[5:-2])
        t_x = np.array(t_x)
        self.clf.fit(t_x, t_y)
        plt.switch_backend('Agg')


    def getshape(self, h):
        """
        Predicts the shape/gesture of the given hand landmarks.

        :param h: Hand landmarks.
        :type h: numpy.ndarray

        :return: Predicted label for the hand gesture.
        :rtype: str
        """
        pre = self.clf.predict(
            np.expand_dims((h - h[0]).flatten(), 0))
        return self.lb[int(pre[0])]

LM = mp.solutions.hands.HandLandmark

def check(h, a, w):
    """
    Checks if the given hand gesture matches the history of gestures within a specified window.

    :param h: The hand gesture to check.
    :type h: list
    :param a: The history of gestures.
    :type a: list
    :param w: The window size to consider in the history.
    :type w: int

    :return: True if the gesture matches the history, False otherwise.
    :rtype: bool
    """
    his = np.asarray(a)
    if type(h) != list:
        h = [h]
    return all(hand in h for hand in his[-int(w):])

class States:
    """
    A class to detect and manage gesture states.

    :param win: The window size for gesture history.
    :type win: int

    :ivar scrollh: A state variable for scroll gestures.
    :ivar state: Current gesture state.
    :ivar ic: A flag for a specific condition.
    :ivar his: A history of detected gestures.

    :method run: Updates the state based on the detected hand gesture and landmarks.
    """
    def __init__(self, win):
        """
        Initializes the States class with a specified window size for gesture history.

        :param win: The window size for gesture history.
        :type win: int
        """
        self.scrollh = -1 
        self.state = "none"
        self.ic = False
        self.his = collections.deque(maxlen=100)
        plt.switch_backend('Agg')

    def run(self, hand, landmarks, i_history):
        """
        Updates the state based on the detected hand gesture and landmarks.

        :param hand: The detected hand gesture.
        :type hand: list
        :param landmarks: The hand landmarks.
        :type landmarks: list
        :param i_history: The history of gestures.
        :type i_history: list
        """
        self.his.append(hand)


if __name__ == "__main__":
    #get mph
    mph = MH(buffer_size=int(0.5 / 0.05))
    stated = States(6)
    handd = Train("/Users/jillianxu/FlappyLingo/Interface/data_folder")
    #open cam
    try:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            #get res
            res = mph.run(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            hs=None
            if mph.his: 
                hs = handd.getshape(
                    mph.his[-1])
                stated.run(hs, mph.his[-1], mph.his)

            #draw
            img = mph.drawlol(image, res, handd)
            cv2.imshow('cemera hehe', img)
            if cv2.waitKey(5) & 0xFF == 27:
                break

            time.sleep(0.05)
    except:
        mph.close()
        cap.release()
        raise



