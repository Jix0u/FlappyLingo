# FlappyLingo: Interactive ASL Learning with Flappy Bird
FlappyLingo combines language learning with the gaming, similar to Duolingo but with a twist of Flappy Bird. Users embark on a journey to learn American Sign Language (ASL) while navigating through the challenging obstacles of Flappy Bird. To progress in the game, users must accurately demonstrate the corresponding hand signs for each Flappy Bird pillar. Failure to do so results in the Flappy Bird falling lifelessly to the ground, prompting users to restart, thus infusing learning with fun and engagement.

## How it Works
1. **Hand Gesture Recognition**:
FlappyLingo utilizes the Mediapipe API to draw hand skeletons and recognize gestures. This enables the application to accurately detect and interpret the hand signs made by the user.

2. **Flappy Bird Integration:**
Pygame is employed to create the game interface and implement the mechanics of Flappy Bird. Users control the Flappy Bird character by demonstrating the correct ASL hand signs, guiding it through pillars representing language learning challenges.

3. **Machine Learning with Convolutional Networks(C-NN):**
Keras's CNN model is imported to train the sign language recognition system. By learning from custom-made data, the model becomes adept at identifying and categorizing hand gestures accurately.

4. **Data Compilation with Pickle**:
Pickle is utilized to compile custom-made data required for training the K-NN model. This facilitates the storage and retrieval of essential information necessary for accurate gesture recognition.

## Demo
![](https://github.com/Jix0u/FlappyLingo/blob/main/readme/flappylingomovie.gif)

## References
- Documentation for Mediapipe gesture recognition: https://mediapipe.readthedocs.io/en/latest/solutions/hands.html
- PyGame Flappy bird: https://www.pygame.org/project/4846

## Usage

1. **Installation**:
Install Python and dependencies listed in requirements.txt (ex. Mediapipe, Pygame, OpenCV) and clone FlappyLingo from the repository.
2. **Setup**:
Train the Mediapipe model with CNN for gesture recognition with custom data.
3. **Customize Data**:
Custom data generation script that compiles screenshots of gestures with Pickle, data_generation.py
Launch FlappyLingo by running launch.py
5. **Play**:
Control Flappy Bird by demonstrating accurate ASL signs for each obstacle.
