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

![33-Landmarks-detected-on-the-human-body-using-MediaPipe](https://user-images.githubusercontent.com/81562297/226096970-d9c774f7-151b-48e6-9bbb-68bced138a94.png)

- `threshold`: the limitation of range that you move your hand as well as body, the bigger threshold the more range of your action must be occured

### 2. After running this, let's open any website of game that containing `SubwaySuffer` game (or you could use [this weblink of SubwaySuffer](https://www.trochoi.net/tr%C3%B2+ch%C6%A1i/subway-surfers.html))
- When the code is running and webcame is auto appearing, let's SWING hand if you playing hand mode or body if you're playing body mode for first detection.
- After that change your window into the game, and CLAP your hand (keep for 1-2 seconds) for starting the game.
- Move your partition of body into identified area to moving character in the game.


## Architecture Designed

![Web capture_18-3-2023_165718_app diagrams net](https://user-images.githubusercontent.com/81562297/226098767-6cb7eff3-5dfc-472d-b1a3-8854f557f243.jpeg)

