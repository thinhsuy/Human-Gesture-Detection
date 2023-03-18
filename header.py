import cv2
import math
import argparse
import pyautogui
import threading
import numpy as np
import pandas as pd
import mediapipe as mp
import tensorflow as tf
from keras.layers import LSTM, Dense,Dropout
from keras.models import Sequential
from sklearn.model_selection import train_test_split