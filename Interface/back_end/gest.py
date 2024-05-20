#Ref: https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/hands.py

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
from hands import MH

#train data
class Train:
    #init
    def __init__(self, data_folder):
        #KNN
        self.clf = neighbors.KNeighborsClassifier(15)
        #training x and y
        t_x = []
        t_y = []
        #label
        self.lb = []

        #look for data
        for i, df in enumerate(o.listdir(data_folder)):
            #get path
            with open(o.path.join(data_folder, df), 'rb') as f:
                #load file
                d = pickle.load(f)
                #train path
                for h in d:
                    t_y.append(i)
                    t_x.append((h - h[0]).flatten())
                #CHECK THIS
                self.lb.append(df[5:-2])
        t_x = np.array(t_x)
        self.clf.fit(t_x, t_y)
        plt.switch_backend('Agg')

    #get certain shape
    def getshape(self, h):
        pre = self.clf.predict(
            np.expand_dims((h - h[0]).flatten(), 0))
        return self.lb[int(pre[0])]

#get mp solution
LM = mp.solutions.hands.HandLandmark

#check function to determine what gesture
def check(h, a, w):
    his = np.asarray(a)
    if type(h) != list:
        h = [h]
    return all(hand in h for hand in his[-int(w):])

#gesture state detector
class States:
    #init
    def __init__(self, win):
        #set states
        self.scrollh = -1 
        self.state = "none"
        self.ic = False
        #get history
        self.his = collections.deque(maxlen=100)
        plt.switch_backend('Agg')

    #run and set the states
    def run(self, hand, landmarks, i_history):
        #add hand to history
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



