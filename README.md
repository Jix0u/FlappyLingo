# FlappyLingo
Teaching ASL with FlappyBird

Here is the [Devpost] (https://devpost.com/software/flappylingo)

https://youtu.be/fG-f8DWmzY4

# Inspiration
As of the recent pandemic, interacting and communicating with marginalized communities has become even more difficult. This is especially true for those who are hearing-impaired, as they primarily communicate through lipreading (masks are a barrier) and writing (social distancing guidelines & risk of spreading germs or the virus). Therefore, many deaf/hard of hearing people at hospitals/other institutions are unable to consistently communicate with doctors/staff. Even ASL interpreters are unable to be there in-person as a result of covid-19 restrictions, and remote interpreters often face audio, camera and other technical issues, making it extremely stressful for those hard of hearing. That is why we have created FlappyLingo, a fun, interactive application for people of all ages to learn American Sign Language (ASL) and communicate with those who are hearing-impaired. Helping the future generation learn about and appreciate those with a hearing disability, making it easier for deaf people to communicate with those around them

# What it does
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
