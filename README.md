# digit_shear_force_estimation
A ROS Package that enables shear force estimation with Facebooks DIGIT Tactile sensors

Required dependencies:
OpenCV
Digit
PRMessages


How to run:

1. Run `catkin build`
2. Run `source devel/setup.bash` from the root directory
3. Run `roscore`
4. Make sure both the f/t sensor and the digit sensor are connected to the computer
5. On separate terminals, run `roslaunch tams_wireless_ft ft.launch`, `roslaunch digit digit.launch` and `roslaunch collector collect.launch` in that order
6. Optionally, run `rosservice call wireless_ft/reset_bias` to tare
7. In the rosbag directory, run `rosbag record -a` to collect data
8. Run `rostopic echo \forque\forqueSensor` to get F/T sensor readings
9. Rune `rostopic echo \magnitude` to get magnitudes
