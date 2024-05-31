# referenced https://google.github.io/mediapipe/solutions/hands#python-solution-api

import cv2
import time
import gest as gd
import numpy as np
import pickle

if __name__ == "__main__":
    buffer_size = int(5 / 0.05)  # Set buffer size for the hand gesture module
    hand = gd.MH(buffer_size=100)  # Initialize the hand gesture module

    picAR = {}  # Dictionary to store hand gesture data
    pics = 220  # Number of pictures to capture for each hand shape
    hand_shape = "C"  # Specify the hand shape to capture
    pause_time = 5  # Pause time before starting to capture
    picAR[hand_shape] = []  # Initialize list for the specified hand shape

    try:
        # Open the camera
        cap = cv2.VideoCapture(0)
        print(f"Make the pose for {hand_shape}")
        time.sleep(pause_time)  # Wait for the user to get ready
        
        while cap.isOpened():
            # If the camera is successfully opened
            success, image = cap.read()
            if not success:
                print("EMPTY")
                continue
            
            w, h, _ = image.shape

            # Run Mediapipe hand detection
            results = hand.run(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Append the detected hand landmarks to the picture array
            try:
                picAR[hand_shape].append(hand.his[-1])
            except IndexError:
                continue

            # Draw Mediapipe landmarks on the image
            img = hand.drawlol2(image, results)            
            cv2.imshow('Generator', img)
            if cv2.waitKey(5) & 0xFF == 27:
                break

            print(len(picAR[hand_shape]))
            if len(picAR[hand_shape]) == pics:
                raise AssertionError  # Stop capturing when the desired number of pictures is reached
            else:
                time.sleep(0.05)
    except:  
        # Save the captured data to a file
        data_array = np.asarray(picAR[hand_shape])
        with open(f"data_{hand_shape}.p", 'wb') as f:
            pickle.dump(data_array, f)
        hand.close()
        cap.release()
        raise
