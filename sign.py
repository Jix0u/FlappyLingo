#Ref: https://google.github.io/mediapipe/solutions/hands.html

#imports
import cv2
import collections
import numpy as np
import mediapipe as mp
import time
from sklearn import neighbors
import matplotlib
from matplotlib import pyplot as plt 
import pickle
import os as o

#train data
class Train:
    #init
    def __init__(self, data_folder):
        
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

    #get certain shape
    def getshape(self, h):
        pre = self.clf.predict(
            np.expand_dims((h - h[0]).flatten(), 0))
        return self.lb[int(pre)]


class MH:
    #init
    def __init__(self, buffer_size=None):
        #get hands
        self.hands = mp.solutions.hands.Hands(
             min_tracking_confidence=0.9,
             min_detection_confidence=0.75
        )
        #get
        self.his = collections.deque(maxlen=100)

        #thresh & num hi
        self.tmt= 3
        self.tmn= 0

    #run img
    def run(self, img):
        #get img.shape
        img_width, img_height, _ = img.shape
        #input photo
        inpi = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        inpi.flags.writeable = False
        #set result
        res = self.hands.process(cv2.cvtColor(inpi, cv2.COLOR_BGR2RGB))

        #check result arr
        if res.multi_hand_landmarks:
            #set track missing num to 0
            self.tmn = 0
            res_arr = np.asarray([[pt.x, pt.y] for pt in res.multi_hand_landmarks[0].landmark])
            self.his.append(res_arr)
        #if track missing num smaller that track missing thresh
        elif self.tmn < self.tmt:
            self.tmn += 1
        #otherwise clear history
        else:
            self.his.clear()
            self.tmn = 0
        plt.switch_backend('Agg')

        return res

    #draw
    def drawlol(self, image, res):
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
                    hshape = Train("/Users/leonachen/downloads/flappylingo/data_folder").getshape(self.his[-1])
                    cv2.putText(new_img,hshape,(center[0]-250,center[1]-209), cv2.FONT_HERSHEY_COMPLEX,3, (225, 150, 255), 9, cv2.LINE_AA)

        return new_img
    def close(self):
        self.hands.close()

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
        self.ic = False
        #check fo specific gestures
        if check("what is up", self.his, 8):
            self.state = "what is up"
        elif check("hello", self.his, 8):
            self.state = "hello"
        elif check("nice to meet you", self.his, 8):
            self.state = "nice to meet you"
        elif check("you", self.his, 8):
            self.state ="you"
        if check("how are", self.his, 5):
            self.state = "how are"
        
     




