OverView:
Senior Project from Pitt,which was designing a tripod that could automatically track a frisbee during ultimate frisbee games

My role was to program the image processing component using python and openCV to track a red frisbee as it passed by our webcam and tell the Arduino that to move the camera. I did this by looking for red objects moving in the frame

Steps to Run:
To run first pip install numpy, opencv.python and serial
  Then run 'videoTest.py'

Explanation:

The green rectangle/circle will surround all red objects that are currently on screen
  
  The yellow numbers next to this circle/rectangle show first the id of the red object and second if we can confirm that the red object is the frisbee (0 means it could    be, 1 means it probably is, 2 means it definately is and -1 means we thought it was but it turned out not to be)

The yellow numbers on the top left are the directions for the arduino and it's servo motor. Directions are given as a 2 integer array with x and y directions, x or y=9 means move the camera right or down, x or y = 1 means move the camera left or up.

The Blue rectangle is our 'region of interest' once the frisbee is found we want to make sure no other moving red objects are taken as the frisbee so we limit the search to around where the frisbee was last seen 
