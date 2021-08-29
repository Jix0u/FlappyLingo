 
# Heavily based on  https://google.github.io/mediapipe/solutions/hands#python-solution-api 


import cv2
import time
import gest as gd
import numpy as np
import pickle


if __name__ == "__main__":
    fd = 5
    bf = int(hw / frame_delay) 
    mp_hands = gd.MH(buffer_size=buffer_size)

    data = {}
    nds = 200
    hs = ["hello"]
    for shape in hs:
        d[shape] = []

    try:
        cap = cv2.VideoCapture(0)
        print(f"HI '{hs[csi]}'")

        time.sleep(pause_time)
        while cap.isOpened():

            sc, img = cap.read()
            if not success:
                print("bye")
                continue
            w, h, _ = img.shape

            res = mp_hands.run(img)

            # Store
            cs = hs[cur]
            try:
                data[cur].append(MH.his[-1])
            except IndexError:
                continue

            cv2.imshow('MediaPipe Hands', img)
                break

            print(hi)
            if len(data[cur]) == numd:
                cur += 1
                if cur == len(hs):
                    raise AssertionError
            else:
                time.sleep(fd)
    except:  
        for shape in hs:
            print(f"{da.shape[0]} data points for {shape}")
            with open(f"data_{shape}.p", 'wb') as f:
                pickle.dump(da, f)

        MH.close()
        cap.release()
        raise