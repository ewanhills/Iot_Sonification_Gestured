from PoseVideos import PoseModule as pm
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




said_yeah = False
said_yeah2 = False
said_yeah3 = False
said_yeah4 = False
said_yeah5 = False
said_yeah6 = False
said_yeah7 = False
said_yeah8 = False
said_yeah9 = False

#Change here to alter the video or image
cap = cv2.VideoCapture("videocurl.mp4")
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
   # img = cv2.imread("test.jpg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        # Right Arm
        angle = detector.findAngle(img, 12, 14, 16)
        # # Left Arm
        #angle = detector.findAngle(img, 11, 13, 15,False)
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))
        # print(angle, per)



        # Check for the dumbbell curls
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)

        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

#Volume Controller
        #bar = int
        #reversed(bar)
        vol = np.interp(bar, [50, 300], [minVol, maxVol])
        volBar = np.interp(bar, [50, 300], [400, 150])
        volPer = np.interp(bar, [50, 300], [0, 100])
        print(int(bar), vol)
        vol = vol/2
        volume.SetMasterVolumeLevel(vol, None)





    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



#INFLUX DB SETUP CONFIG
#Alther here to add send data to influxdb
client = InfluxDBClient('localhose', 8086, 'test', 'password', 'iot_sonify_db')

sleep(3)
#Setup Payload
json_payload = []
data = {
    "measurement" : "IOT",
    "tags": {
        "volume": "VOL"
    },
    "time": datetime.now(),
    "fields": {
        'volume' : 21,
        'percentage' : 27,
        'count':2
    }
}
json_payload.append(data)

#SEND THE PAYLOAD


#Comment back in this and remove volume code above to play tones after a successful repitition
# Or if you like both can be left in, again the matching mp3 files show be in the data folder
client.write_points(json_payload)
print("sent values to influxDB Database")

'''
    if count == 1 and said_yeah == False:
        yeah = playsound('ring_5.mp3')
        said_yeah = True
    if count == 2 and said_yeah2 == False:
        yeah = playsound('ring_5.mp3')
        said_yeah2 = True
    if count == 3 and said_yeah3 == False:
        yeah = playsound('ring_5.mp3')
        said_yeah3 = True
    if count == 4 and said_yeah4 == False:
        yeah = playsound('ring_2.mp3')
        said_yeah4 = True
    if count == 5 and said_yeah5 == False:
        yeah = playsound('ring_2.mp3')
        said_yeah5 = True
    if count == 6 and said_yeah6 == False:
        yeah = playsound('ring_4.mp3')
        said_yeah6 = True
    if count == 7 and said_yeah7 == False:
        yeah = playsound('ring_4.mp3')
        said_yeah7 = True
    if count == 8 and said_yeah8 == False:
        yeah = playsound('ring_4.mp3')
        said_yeah8 = True
    if count == 9 and said_yeah9 == False:
        yeah = playsound('ring_4.mp3')
        said_yeah9 = True
'''''
