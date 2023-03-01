#!/usr/bin/env python
# PKG = 'collector'
# import roslib; roslib.load_manifest(PKG)
import rospy
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Float64
from digit_interface.digit import Digit
from digit_interface.digit_handler import DigitHandler
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from opticalFlow import OpticalReader
from vectorField import VectorField
from digit.srv import Tare, TareResponse
from digit.srv import ResetPoint, ResetPointResponse
from geometry_msgs.msg import Vector3
import cv2
import numpy



def talker():
    img_pub = rospy.Publisher('digit_img', numpy_msg(Image),queue_size=10)
    magnitude_pub = rospy.Publisher("digit_forces", Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    reset_service = rospy.Service('reset_point', ResetPoint, handle_reset)
    s = rospy.Service('tare', Tare, handle_tare)
    
    r = rospy.Rate(100) # 100hz
    digit = Digit("D20201")

    global is_tare
    is_tare = False
    global reset
    reset = False


    init_img = None
    curr_img = None
    viz = True
    digit.connect()
    bridge = CvBridge()
    flow = OpticalReader()
    tare_offset = 0
    while not rospy.is_shutdown():

        a = digit.get_frame()
        vField = None

        if init_img is None or reset:
            reset = False
            init_img = a 
        else:
            if is_tare:
                curr_img = a 
                vField = flow.computeOpticalFlow(init_img, curr_img, viz)
                tare_offset = vField.get_force_vector()
                is_tare = False
                print (tare_offset)
                print ("Tare successful")
            curr_img = a 
            vField = flow.computeOpticalFlow(init_img, curr_img, viz)
            # print(f"magnitude: {vField.get_magnitude() }")
            # vector = vField.get_force_vector()-tare_offset
            # msg = Vector3()
            # msg.x = vector[0]
            # msg.z = vector[1]
            # magnitude_pub.publish(msg)
            magnitude_pub.publish(vField.get_magnitude()-tare_offset)


        msg = bridge.cv2_to_imgmsg(a)
        msg.header.stamp = rospy.Time.now()
        img_pub.publish(msg)
        r.sleep()

def tare_server():
    rospy.init_node('tare_server')
    print ("Ready to tare")
    rospy.spin()

def handle_tare(req):
    global is_tare
    is_tare = True
    return TareResponse(True)

def reset_server():
    rospy.init_node('reset_server')
    print ("You can reset points now")
    rospy.spin()

def handle_reset(req):
    global reset 
    reset = True 
    return ResetPointResponse(True)




if __name__ == '__main__':
    
    talker()
    