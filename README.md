# digit_shear_force_estimation
A ROS Package that enables shear force estimation with Facebooks DIGIT Tactile sensors

# demo

https://drive.google.com/file/d/1lFl928FAtotZ-w2F6MqtwLAZmR1IUUmk/view

Required dependencies:
OpenCV
Digit
PRMessages



How to run:

1. Clone the repo (this repo is a workspace)
2. Run `catkin build`
2. Run `source devel/setup.bash` from the root directory
3. Run `roscore`
4. Run `roslaunch digit digit.launch`
5. Run `rostopic echo \magnitude` to get magnitudes
6. Optionally, run `rosservice call /tare false` to tare values to zero, or `rosservice call /resetPoints false` to reset which points optical flow tracks

How to do data collection:
1. Run steps 1-3 from the previous section
4. Make sure both the f/t sensor and the digit sensor are connected to the computer
5. Run `roslaunch digit collect.launch`
6. Optionally, run `rosservice call wireless_ft/reset_bias` to tare and `rosservice call /tare false` to tare the digit sensor
7. Run `rostopic echo \forque\forqueSensor` to get F/T sensor readings
8. Run `rosbag record -a` to collect data. The data is published to topics `/sync_force_data`, `/sync_img_data` and `/sync_magnitude_data`.