# Iot_Sonification_Gestured

How to run the code:

All the code is written in python and each model consists of 2 classes one class calls upon the api and does the heavy lifting whilst the other we use to carry out our functions:
Upper body pose:
PoseData Folder this is where you will place any mp4 videos, images etc.
Consists of 2 classes “weight_Lifting_Trainer” and “PoseModel”
Run “weight_Lifting_Trainer” class.

Simple Hand Pose:
Consists of 2 classes “gestureVolumeControl” and “HandtrackingModule”
Run “gestureVolumeControl” class.

Advanced Hand Pose:
Consists of 2 classes “gestureVolumeAdvancedControl” and HandtrackingAdvancedModule”
Run “gestureVolumeAdvancedControl” class

The following libs will be required all can be installed through the console or within the code itself:
import cv2

#For sending data to inflix db
from influxdb import InfluxDBClient
from datetime import datetime
#########################################
from playsound import playsound
import time
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
