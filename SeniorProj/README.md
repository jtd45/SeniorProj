**arduinoSerial.py**

Class connects to the arduino Uno which was used to control the webcamera's servo motor

**discreteTest.py**

Test code testing different image filtering methods to determine what best to use

**manualControl.py**

Used to manually contron the webcamera through the arduino

**redObjects.py**

Contains 2 classes

1) Rect: defines the rectangles drawn around an object during the image test to visualize where objects are seen in the frame

2) RedObj: extends Rect, used to define red objects their speed and how long the object has been detected by the camera

**videoDiffTest.py**

Test code testing how to filter out everything but motion on a video

**videoTest.py**

Final test code showing how the program tracks a red frisbee as it passes by the camera

**webcamTest.py**

Test code used to open a laptop's webcam
