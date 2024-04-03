# FlappyLingo
Teaching ASL with FlappyBird
![](https://github.com/Jix0u/FlappyLingo/blob/main/FLAPPYLINGOGIF2.gif)

# How it works
Similar to Duolingo, it teaches users a new language (ASL) but with the addition of flappy bird. Users must demonstrate the correct hand sign to pass each flappy bird pillar, if not the flappy bird will fall, lifelessly to the ground, forcing users to restart. This makes the learning process much more enjoyable and interactive.

# How we built it
- Mediapipe API to draw hand skeleton and recognize gestures
- Pygame to create the application interface and flappy bird
- Sklearn to import the K-Nearest Neighbour (K-NN) model to train the sign language model
- Pickle to compile custom made data

# Challenges we ran into
- Errors when syncing gestures to the flappy bird (pygame failed to categorize)
- Pickle files often corrupted and would not compile the code properly (all pictures must be retaken)
- K-NN model would not import properly
- Flappy bird would fly out of screen due to poorly written screen constraints
- Not enough sign language phrases

# Accomplishments that we're proud of
- Being able train a mediapipe model with KNN to recognize hand signs
- Integrating these hand gestures into flappy bird
- Learning basic ASL

# What we learned
- How to train with KNN
- How to use pygame
- ASL
- importing and using sprites
- Compiling code with pickle

# What's next for FlappyLingo
- IOS application
- Better user interface
- Levels/Stages/Exp/Coins
- More phrases to learn
- Maybe a different game other than flappy bird
