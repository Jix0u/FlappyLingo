#Heavily referenced https://google.github.io/mediapipe/solutions/hands#python-solution-api 

import cv2
import time
import gest as gd
import numpy as np
import pickle


if __name__ == "__main__":
    buffer_size = int(5 / 0.05) 
    hand = gd.MH(buffer_size=100)

    picAR = {}
    pics = 220
    #choose hand_shape
    hand_shape = "C"
    pause_time = 5
    picAR[hand_shape] = []

    try:
        #open cam
        cap = cv2.VideoCapture(0)
        print(f"Make the pose for {hand_shape}")
        time.sleep(pause_time)
        while cap.isOpened():
            #if successfully openned
            success, image = cap.read()
            if not success:
                print("EMPTY")
                continue
            w, h, _ = image.shape

            #run mediapipe
            results = hand.run(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            #append to pics array
            try:
                picAR[hand_shape].append(hand.his[-1])
            except IndexError:
                continue

            #draw mediapipe line
            img = hand.drawlol2(image, results)            
            cv2.imshow('Generator', img)
            if cv2.waitKey(5) & 0xFF == 27:
                break

            print(len(picAR[hand_shape]))
            if len(picAR[hand_shape]) == pics:
                raise AssertionError
            else:
                time.sleep(0.05)
    except:  
        data_array = np.asarray(picAR[hand_shape])
        with open(f"data_{hand_shape}.p", 'wb') as f:
            pickle.dump(data_array, f)
        hand.close()
        cap.release()
        raise