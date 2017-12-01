#!/usr/bin/env python
# Title : intercom_demo.py
# Author : Kyna Mowat-Gosnell
# Date : 09/10/17
# Version : 1.0

import rospy, qi, argparse
import sys
import time
import naoqi
from naoqi import *
from diagnostic_msgs.msg import KeyValue # message type /iot_updates uses
from std_msgs.msg import Empty

def callback(data):
	print("inside callback")

def iot_callback(data):
    if(data.key == "Hall_Intcm" and data.value == "ON"): # Button pressed
		intcm_ring()

def intcm_ring():
    tabletProxy.showImage("http://198.18.0.1/apps/dragone-51a938/Dragone.jpg") # image loaded onto Pepper via Choregraphe
    animatedProxy.say("Hello, your friend Mauro is at the door, you have agreed to go for a walk together this afternoon.") # message Pepper says after intercom ring
    time.sleep(5)
    animatedProxy.say("You're welcome.")
    time.sleep(5)
    tabletProxy.hideImage() # must hide image to unload from tablet

def listener():
    rospy.init_node('intcm_listener', anonymous=True) # initialise node to subscribe to topic
    rospy.Subscriber("/devices/bell", Empty, callback) # subscribe to topic where intercom ring is published
    rospy.Subscriber("/iot_updates", KeyValue, iot_callback) # subscribe to topic /iot_updates
    rospy.spin() # keeps python from exiting until node is stopped


if __name__ == '__main__':
    from naoqi import ALProxy
    broker = ALBroker("pythonBroker", "192.168.1.129", 9999, "pepper.local", 9559) # Create a local broker, connected to the remote naoqi
    animatedProxy = ALProxy("ALAnimatedSpeech", "pepper.local", 9559) # initialise animated speech proxy
    tabletProxy = ALProxy("ALTabletService", "pepper.local", 9559) # initialise tablet proxy
    tabletProxy.getWifiStatus() # check wifi status
    print tabletProxy.getWifiStatus() # print wifi status "CONNECTED" if connected
    postureProxy = ALProxy("ALRobotPosture", "pepper.local", 9559) # initialise posture proxy
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position

    while True:
        listener() #does not break out of loop until manually stopped on the terminal
