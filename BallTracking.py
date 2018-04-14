/*****************************************************************************************
*  Name    : Fast object tracking using the OpenCV library                               *
*  Author  : Lior Chen &lt;chen.lior@gmail.com&gt;                                       *
*  Notice  : Copyright (c) Jun 2010, Lior Chen, All Rights Reserved                      *
*          :                                                                             *
*  Site    : http://www.lirtex.com                                                       *
*  WebPage : http://www.lirtex.com/robotics/fast-object-tracking-robot-computer-vision   *
*          :                                                                             *
*  Version : 1.0                                                                         *
*  Notes   : By default this code will open the first connected camera.                  *
*          : In order to change to another camera, change                                *
*          : CvCapture* capture = cvCaptureFromCAM( 0 ); to 1,2,3, etc.                  *
*          : Also, the code is currently configured to tracking RED objects.             *
*          : This can be changed by changing the hsv_min and hsv_max vectors             *
*          :                                                                             *
*  License : This program is free software: you can redistribute it and/or modify        *
*          : it under the terms of the GNU General Public License as published by        *
*          : the Free Software Foundation, either version 3 of the License, or           *
*          : (at your option) any later version.                                         *
*          :                                                                             *
*          : This program is distributed in the hope that it will be useful,             *
*          : but WITHOUT ANY WARRANTY; without even the implied warranty of              *
*          : MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               *
*          : GNU General Public License for more details.                                *
*          :                                                                             *
*          : You should have received a copy of the GNU General Public License           *
*          : along with this program.  If not, see &lt;http://www.gnu.org/licenses/&gt;  *
******************************************************************************************/
#!/usr/bin/python
from opencv.cv import *
from opencv.highgui import *
from threading import Thread
#import serial
class RobotVision:
    cvSize size
    cvImage hsv_frame, thresholded, thresholded2
    cvScalar hsv_min, hsv_max, hsv_min2, hsv_max2
    cvCapture capture;
    def InitBallTracking():
        globals size,  hsv_frame, thresholded, thresholded2, hsv_min, hsv_max, hsv_min2, hsv_max2, capture
        print "Initializing ball Tracking"
        size = cvSize(640, 480)
        hsv_frame = cvCreateImage(size, IPL_DEPTH_8U, 3)
        thresholded = cvCreateImage(size, IPL_DEPTH_8U, 1)
        thresholded2 = cvCreateImage(size, IPL_DEPTH_8U, 1)
        hsv_min = cvScalar(0, 50, 170, 0)
        hsv_max = cvScalar(10, 180, 256, 0)
        hsv_min2 = cvScalar(170, 50, 170, 0)
        hsv_max2 = cvScalar(256, 180, 256, 0)
        storage = cvCreateMemStorage(0)
        # start capturing form webcam
        capture = cvCreateCameraCapture(-1)
        if not capture:
            print &quot;Could not open webcam&quot;
            sys.exit(1)
            #CV windows
        cvNamedWindow( &quot;Camera&quot;, CV_WINDOW_AUTOSIZE )
    def TrackBall(i):
        t = Thread(target=TrackBallThread, args=(i,))
        t.start()
    def TrackBallThread(num_of_balls):
        globals size,  hsv_frame, thresholded, thresholded2, hsv_min, hsv_max, hsv_min2, hsv_max2, capture
        while 1:
            # get a frame from the webcam
            frame = cvQueryFrame(capture)
            if frame is not None:</p>
                # convert to HSV for color matching
                # as hue wraps around, we need to match it in 2 parts and OR together
                cvCvtColor(frame, hsv_frame, CV_BGR2HSV)
                cvInRangeS(hsv_frame, hsv_min, hsv_max, thresholded)
                cvInRangeS(hsv_frame, hsv_min2, hsv_max2, thresholded2)
                cvOr(thresholded, thresholded2, thresholded)
                # pre-smoothing improves Hough detector
                cvSmooth(thresholded, thresholded, CV_GAUSSIAN, 9, 9)
                circles = cvHoughCircles(thresholded, storage, CV_HOUGH_GRADIENT, 2, thresholded.height/4, 100, 40, 20, 200)
                # find largest circle
                maxRadius = 0
                x = 0
                y = 0>
                found = False
                for i in range(circles.total):
                    circle = circles[i]
                    if circle[2] &gt; maxRadius:
                        found = True
                        maxRadius = circle[2]
                        x = circle[0]
                        y = circle[1]
                cvShowImage( &quot;Camera&quot;, frame );
                if found:
                    print &quot;ball detected at position:&quot;,x, &quot;,&quot;, y, &quot; with radius:&quot;, maxRadius
                    if x &gt; 420:
                        # need to pan right
                        servoPos += 5
                        servoPos = min(140, servoPos)
                        servo(2, servoPos)
                    elif x &lt; 220:
                        servoPos -= 5
                        servoPos = max(40, servoPos)
                        servo(2, servoPos)
                    print &quot;servo position:&quot;, servoPos
                else:
                    print &quot;no ball&quot;
