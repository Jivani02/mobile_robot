#! /usr/bin/env python3

import rospy
from stereo_msgs.msg import DisparityImage
import cv2
from cv_bridge import CvBridge

class disparity_viewer():
    def __init__(self):
        rospy.init_node("disparity_viewer")
        self.sub = rospy.Subscriber('/stereo_camera/disparity', DisparityImage, self.callback)
        self.bridge = CvBridge()

    def callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg.image)
        cv2.imshow("Disparity", cv_image)
        cv2.waitKey(1)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    node=disparity_viewer()
    node.run()
