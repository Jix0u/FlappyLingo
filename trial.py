#Ref: https://google.github.io/mediapipe/solutions/hands.html
import cv2
# import pyautogui as pag
import mediapipe as mp
# import keyboard
# import speech_input
import gest
import matplotlib.pyplot as plt
import os
# from flask import Flask
showvid = True

def run():
    # print("ok")Hello.
    # plt.switch_backend('Agg')

    global showvid

    gg = gest.States(8)
    hands = gest.MH(buffer_size=100)
    plt.switch_backend('Agg')
    # if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    try:
        # print("hi bithc")
        cap = cv2.VideoCapture(0)
        # print("hi ok")
        while cap.isOpened():
            success, image = cap.read()            
            if not success:
                print("Ignoring empty")
                continue
            # print("hi sigh")
            res = hands.run(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            hshape = ""
            if hands.his:
                hshape = gest.Train("/Users/leonachen/downloads/flappylingo/data_folder").getshape(hands.his[-1])
                gg.run(hshape, hands.his[-1], hands.his)
                print(f"state={gg.state}, click={gg.ic}, shape={hshape}")


            if showvid:
                # Overlaying the mediapipe "skeleton"
                # print("hi lmfaooooo")
                img = hands.drawlol(image, res)
                cv2.imshow('KEK XD LMFAO', img)
                # print("hi bro sigh")

            if cv2.waitKey(5) & 0xFF == 27:
                break
    except:        
        cv2.destroyAllWindows()
        hands.close()
        cap.release()
        print("\n>>> Error caught. Program closed gracefully. <<<\n")
        raise


if __name__ == "__main__":
    run()
