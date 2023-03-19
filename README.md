# Human Gesture Detection Game
## Introduction
Instead of using the mouse or keyboard buttons to control the games, vision-based interfaces for video games use gestures, to give the user a more natural interface, these interfaces must accommodate inadvertent movements and ongoing gestures.

The vision-based interface for video games offers chances for new interactions between computer and human. In the interface, gestures rather than key presses on a keyboard or mouse movements are utilized to control the games. The interface converts the user's intentions, which serve as the game's input, into images, which are motion photos taken of the user's gestures. For instance, in Decathlete, the user must run in order to make a computer character run (Freeman et al., 1998).

## Important Note
1. The videogame I go for this program's gesture game recognition is simply `Subway Suffer`, which could potentially be used with any type of gaming website.
2. Please make sure that your computer has been installed at least `Python` and `PIP` is available.

## Setting Up
**Here is step by step introduction for setting up libraries for all users (including non-IT users, so if you already know these steps, just skip it)**
1. Of course you have to download this set of folder by clicking on the green `Code` button above.
2. After downloading, obviously you have to extract it (unzip)
3. Let's open the Terminal Window from this file, if you don't know how to open it in window? Follow the link [here](https://www.thewindowsclub.com/how-to-open-command-prompt-from-right-click-menu).
(If you use other OS as Mac or Linux? Searching by yourself!)
4. Paste below line into that Terminal (Command Prompt) for installing needed libraries:
```
pip install -r setup.txt
```
And then all the requirements for this program are already installed and now you are able to run it.

## How to run?
### 1. To run the program, please insert below line into current Terminal in case you take too much attention on its parameters
```
python mainGame.py --playmode Hand --anchorpoint 15 --threshold 150
```
- `playmode`: the partition of yours for this detection of the game (including Body and Hand), change it if you want to play chosen mode.
- `anchorpoint`: the particular point of landmarks on your body for detection, incase you are playing Body Mode, this point would be default and constant at 11 and 12 (left and right shoulder). But if you are playing in mode of Hand, you could flexibily choose your anchor for moving character (the specific point of your body could learned from this image)
- `threshold`: the limitation of range that you move your hand as well as body, the bigger threshold the more range of your action must be occured

![33-Landmarks-detected-on-the-human-body-using-MediaPipe](https://user-images.githubusercontent.com/81562297/226096970-d9c774f7-151b-48e6-9bbb-68bced138a94.png)

### 2. After running this, let's open any website of game that containing `SubwaySuffer` game (or you could use [this weblink of SubwaySuffer](https://www.trochoi.net/tr%C3%B2+ch%C6%A1i/subway-surfers.html))
- When the code is running and webcame is auto appearing, let's SWING hand if you playing hand mode or body if you're playing body mode for first detection.
- After that change your window into the game, and CLAP your hand (keep for 1-2 seconds) for starting the game.
- Move your partition of body into identified area to moving character in the game.


## Architecture Designs and Methodology

This is my pipeline process for the operation:

![Web capture_18-3-2023_165718_app diagrams net](https://user-images.githubusercontent.com/81562297/226098767-6cb7eff3-5dfc-472d-b1a3-8854f557f243.jpeg)

- First of all, I selected to manually generate the data repairs for the training set, which meant the different kinds of actions would be made as samples.
- Once the data had been tagged, I would begin to push it through the modeling process, using the [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory) architecture as my training approach before extracting the model for the prediction stage. (In the event that you lack the time to carry out the training procedure, I have already done it for you with the set of pretrained data, which includes `SWING BODY` and `SWING HAND` with the weight result being stored in `model.h5`).

![Web capture_19-3-2023_143318_app diagrams net](https://user-images.githubusercontent.com/81562297/226160675-b3625ab4-814a-4bb7-9c4e-6a35d85dc6d4.jpeg)

- With the trained model, I continue using [OpenCV](https://docs.opencv.org/4.x/d1/dfb/intro.html) to predict human interaction while combining with [Mediapipe](https://google.github.io/mediapipe/) to identify human landmarks in to figure out the current short motion of the human and control the game character after CLAPPING (action to start the game) by several of the techniques below:

![asa](https://user-images.githubusercontent.com/81562297/226161816-77d7f91c-8929-465b-8fda-ea9029475023.png)

- For **BODY playmode**, I would detect a constant line of y axis depending on human's shoulders after you performing a CLAP. Every actions which makes your shoulders point higher or lower than that line (+/- threshold) would result into a correlated action (JUMP and SCROLL) for character. The same algorithm is applied for x axis related action (LEFT and RIGHT) of user as well as character.
	
![aczxcz](https://user-images.githubusercontent.com/81562297/226161823-1b9d260f-e4c3-4155-8a01-363be6e6f926.png)
	
- For **HAND playmode**, it is possible for player select their own landmark point on their hand for an anchor point, whenever you move that anchor point out of the middle x line and y line (+/- threshold), character would perform an action associated with the axis of that point (JUMP SCROLL LEFT RIGHT).
	
![Untitled](https://user-images.githubusercontent.com/81562297/226161827-86c0ed66-5dcf-4d5c-a425-9ab9c16a5f55.png)

- Perhaps more than with its former location, the character would be able to do any action related to the current position of the point (shoulder or hand) using the anchor point's axis.

![caa](https://user-images.githubusercontent.com/81562297/226162690-af4c3cff-ad15-4ef4-9ecc-577bc23b9891.png)

## Maintenance
This endeavor was developed just for personal purpose, which caused it unable to totally complete the code's logic and several mistakes. Once you have any interest in this project, let's work together to make it better. I'd always happy to share with you further project-related ideas.

## References
- [Developing a Long Short-Term Memory (LSTM) based model for predicting water table depth in agricultural areas](https://www.sciencedirect.com/science/article/abs/pii/S0022169418303184)
- [Recognition-based gesture spotting in video games](https://www.sciencedirect.com/science/article/abs/pii/S0167865504001576)
- [MiAI_Human_Activity_Recognition](https://github.com/thangnch/MiAI_Human_Activity_Recognition)
- [MiAI_Game_Control_by_Pose](https://github.com/thangnch/MiAI_Game_Control_by_Pose)
