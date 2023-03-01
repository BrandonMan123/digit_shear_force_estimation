#!/usr/bin/env python
import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from geometry_msgs.msg import WrenchStamped
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import message_filters
import rosbag



class sub_and_pub():
    """ Class that synchronizes f/t sensor readings, image and optical flow readings then
    publish to two separate nodes """
    def __init__(self):
        print ("Intializing sub and pub")
        # initialize publishers to publish synchronized messages
        self.pub_img = rospy.Publisher('sync_img_data', numpy_msg(Image), queue_size=10)
        self.pub_force = rospy.Publisher('sync_force_data', WrenchStamped, queue_size=10)
        self.magnitude = rospy.Publisher('sync_magnitude_data', Float64, queue_size=10)
        print ("Finished intializing sub and pub")
        # subscribers to get synchronized messages
        self.image_sub = message_filters.Subscriber("digit_img", numpy_msg(Image))
        self.force_sub = message_filters.Subscriber("/forque/forqueSensor", WrenchStamped)
        self.magnitude_sub = message_filters.Subscriber("digit_forces", Float64)

        ts = message_filters.ApproximateTimeSynchronizer(
            [self.image_sub, self.force_sub, self.magnitude_sub],slop=1, queue_size=10, allow_headerless=True)
        print ("Initilaized filter")
        ts.registerCallback(self.callback_sync)
        print ("Registered callback")

    def callback_sync(self, img, force, digit_force):
        self.pub_img.publish(img)
        self.pub_force.publish(force)
        self.magnitude.publish(digit_force)



def listener():

    rospy.init_node('listener', anonymous=True)
    a = sub_and_pub()
    rospy.spin()

if __name__ == '__main__':
    listener()
