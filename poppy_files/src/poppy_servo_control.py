"""
Author: Sydney Awid
Used to control the robot servos
"""
import pypot.dynamixel
import time
import threading
import numpy


def goalPos(n):
    '''
    Takes input of goal position from Wizard.
    :param n:
    :return:
    '''
    return n - 180

class poppy_body_gesture():
    def __init__(self):
        super().__init__()
        self.dxl_io = pypot.dynamixel.DxlIO('COM7')
        self.emotion = ''
        self.servo_ids = {'torso_base': 33, 'chest_tilt_left_right': 35, 'chest_tilt_forward_backward': 34,
                          'neck_left_right': 68, 'neck_up_down': 69, 'left_inner_shoulder': 41,
                          'left_outer_shoulder': 42, 'left_bicep': 43, 'left_elbow': 44, 'right_inner_shoulder': 51,
                          'right_outer_shoulder': 52, 'right_bicep': 53, 'right_elbow': 54, 'right_ankle': 170,
                          'right_knee': 171, 'left_bottom_hip': 172, 'left_top_hip': 173, 'left_ankle': 180,
                          'left_knee': 181, 'right_bottom_hip': 182, 'right_top_hip': 183, 'right_bottom_pelvis': 184,
                          'left_bottom_pelvis': 174, 'forward_top_pelvis': 161, 'back_top_pelvis': 160}
        self.keys = [keys for keys in self.servo_ids]
        self.position_list = []

    def scan_all_servo_limit(self):
        """ Method: poppy_scan_position_limit
            servo I.D's are set
            scans every dynamixel servo and prints out the servo I.D and corresponding
            angle limit.
        """
        with self.dxl_io as io_connect:
            ids = io_connect.scan([33, 34, 35, 68, 69, 41, 42, 43, 44, 51, 52, 53, 54, 170, 171, 172, 173, 180, 181, 182, 183])
            id_angle_limit = io_connect.get_angle_limit(ids)

            keys = [keys for keys in self.servo_ids]

            for i in range(len(ids)):
                print(f'{keys[i]}: Angle Limit = {id_angle_limit[i]}')

    def move_servo(self, servo_id, servo_position, servo_speed):
        """
        Control single servo motor with speed and position
        :param servo_id: id number of servo or use self.servo_ids and index using keys
        :param servo_position: position in degrees
        :param servo_speed: speed at which servo moves; 0-250
        :return: nothing
        """
        self.dxl_io.set_moving_speed({servo_id: servo_speed})
        self.dxl_io.set_goal_position({servo_id: servo_position})

    def get_servo_position(self, servo_id):
        """
        Get position of one servo using its servo id
        :param servo_id:id number of servo or use self.servo_ids and index using keys
        :return: current position of servo in degrees, value used only on python
        """
        return self.dxl_io.get_present_position((servo_id,))[0]

    def get_all_servo_position(self, print_list):
        """
        Scan and get all current servo positions and print
        :param print_list: True = print or False = don't print;
        :return: a list of all current positions
        """
        for keys in self.servo_ids:
            # print(keys)
            servo_position = self.get_servo_position(self.servo_ids[keys])
            self.position_list.append(servo_position)
            if print_list:
                print(f"{keys}: Position = {servo_position}")
        return self.position_list

    def pose_generator(self):
        """
        Use to create new body functions by getting current positions and printing out exact code to use
        to put in new function for new body gesture.
        PROPER USAGE: Put robot in desired pose then call this function
        :return: Nothing
        """
        self.position_list = self.get_all_servo_position(False)
        keys = [keys for keys in self.servo_ids]
        print('use the following lines of code for new position')
        print('servo_speed = 100')

        for i in range(len(self.position_list)):
            print(f"self.move_servo(self.servo_ids['{keys[i]}'],{self.position_list[i]}, servo_speed)")

    def set_to_idle_position(self):
        """
        Set robots pose to idle
        :return: Nothing
        """
        self.emotion = 'neutral'
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], -137.02, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 2.24, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.31, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 12.26, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 59.82, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -0.13, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.34, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 0.04, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -86.46, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 0.57, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -74.68, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -0.4, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 83.03, servo_speed)

    def set_to_T_position(self):
        """
        Set robots body pose to T position. Also use when re-assembling robot
        :return: Nothing
        """
        self.emotion = 'neutral'
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], -137.02, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 0, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 12.26, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 59.82, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], 0, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 0, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 0, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], 0, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 0, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], 0, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], 0, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 0, servo_speed)

    def set_to_happy(self):
        """
        Set robots body pose to happy
        :return: Nothing
        """
        servo_speed = 100
        self.set_to_idle_position()
        time.sleep(1)

        self.move_servo(self.servo_ids['left_inner_shoulder'], -93.58, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 33.54, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.89, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 89.36, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -23.87, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -2.15, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
        time.sleep(.5)

        for _ in range(3):
            self.move_servo(self.servo_ids['left_elbow'], -110.02, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 114.86, servo_speed)
            time.sleep(.25)
            self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
            time.sleep(.25)
        self.set_to_neutral()

    def set_to_face_tracking(self):
        """
        Set robots pose for face tracking, does not use neck servos
        :return: Nothing
        """
        self.emotion = 'neutral'
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.31, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 2.95, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -3.03, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.16, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.45, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -25.98, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 2.59, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -82.77, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -1.63, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 19.3, servo_speed)

    def set_to_neutral(self):
        """
        Set robots pose to neutral
        :return: Nothing
        """
        self.emotion = 'neutral'
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], -137.02, servo_speed)  # Changed neutral from prior base value
        self.move_servo(self.servo_ids['chest_tilt_left_right'], .97, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], -.79, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 7.56, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], .35, servo_speed)  # 60.25
        self.move_servo(self.servo_ids['left_inner_shoulder'], -3.03, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.16, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.45, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], .44, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 2.59, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -82.77, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -1.63, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], .26, servo_speed)

    def set_to_sad(self):
        """
        Set robots pose to sad
        :return: Nothing
        """
        self.emotion = 'sad'
        servo_speed = 25
        self.move_servo(self.servo_ids['torso_base'], 0.4, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], -11.21, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], -0.04, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 8.75, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 30.2, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -13.05, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.87, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 19.47, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -19.82, 100)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 9.19, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -83.38, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -8.48, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 20.44, 100)

    def set_to_frightened(self):
        """
        Set robots pose to frightened
        :return: Nothing
        """
        self.emotion = 'frightened'
        servo_speed = 150

        self.move_servo(self.servo_ids['torso_base'], 0.4, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 21.58, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.84, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 35.03, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 64.66, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 78.29, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -96.75, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -40.4, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 99.21, servo_speed)

        self.move_servo(self.servo_ids['left_inner_shoulder'], -47.87, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 66.24, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 44.0, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -114.59, servo_speed)

        time.sleep(2)

        # reset arms
        servo_speed = 100
        self.move_servo(self.servo_ids['left_inner_shoulder'], -3.03, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.16, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.45, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -25.98, servo_speed)

        servo_speed = 75
        self.move_servo(self.servo_ids['torso_base'], 0.31, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 2.95, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 11.65, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 60.26, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 2.59, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -82.77, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -1.63, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 19.3, servo_speed)

    def set_to_wave_one_hand(self, right_hand, left_hand):
        servo_speed = 100

        if left_hand:
            self.move_servo(self.servo_ids['left_inner_shoulder'], -93.58, servo_speed)
            self.move_servo(self.servo_ids['left_outer_shoulder'], 33.54, servo_speed)
            self.move_servo(self.servo_ids['left_bicep'], 1.89, servo_speed)
            self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)
        if right_hand:
            self.move_servo(self.servo_ids['right_inner_shoulder'], 89.36, servo_speed)
            self.move_servo(self.servo_ids['right_outer_shoulder'], -23.87, servo_speed)
            self.move_servo(self.servo_ids['right_bicep'], -2.15, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
        time.sleep(1)

        for _ in range(3):
            if right_hand:
                self.move_servo(self.servo_ids['right_elbow'], 114.86, servo_speed)
                time.sleep(.25)
                self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
            if left_hand:
                self.move_servo(self.servo_ids['left_elbow'], -110.02, servo_speed)
                time.sleep(.25)
                self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)
            time.sleep(.25)
        self.set_to_neutral()

    def set_to_confused(self):
        """
        Set robots pose to confused
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 3.21, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 9.89, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], -8.92, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 71.87, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -30.64, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], -19.3, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -137.63, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.96, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.2, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], 40.57, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 139.82, servo_speed)
        servo_speed = 25
        self.move_servo(self.servo_ids['left_outer_shoulder'], 93.05, servo_speed)

        time.sleep(2)
        # shrug shoulders
        servo_speed = 50
        self.move_servo(self.servo_ids['right_inner_shoulder'], 27.21, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -92.7, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -41.01, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 76.0, servo_speed)
        time.sleep(0.25)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.96, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.2, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -30.64, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 93.05, servo_speed)
        time.sleep(0.5)

        self.set_to_neutral()

    def set_to_angry(self):
        """
        Set robots pose to angry
        :return: Nothing
        """
        self.emotion = 'angry'

        servo_speed = 125
        self.move_servo(self.servo_ids['torso_base'], 0.22, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], -2.33, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.75, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 22.81, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 51.91, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -7.6, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 22.2, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 82.33, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 14.55, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -24.04, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -93.58, servo_speed)

        time.sleep(0.25)
        servo_speed = 150
        self.move_servo(self.servo_ids['right_elbow'], 101.58, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -101.49, servo_speed)

        time.sleep(3)

        # reset arms
        servo_speed = 150
        self.move_servo(self.servo_ids['right_bicep'], -1.63, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.45, servo_speed)
        time.sleep(0.25)
        self.set_to_neutral()

    def set_to_sad_2(self):
        """
        Different variation of sad pose. Use to put robot to a different pose while sad
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], -11.91, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.13, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 9.19, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 58.77, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -13.14, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.69, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 19.21, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -20.09, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 9.19, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -83.3, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -8.31, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 19.91, servo_speed)

    def set_to_angry_2(self):
        """
        Different variation of angry pose. Use to put robot to a different pose while angry
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.4, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], -1.8, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 1.45, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 9.71, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 60.7, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -7.6, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 23.34, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 82.07, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -101.14, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 4.26, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -76.18, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -42.07, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 15.34, servo_speed)

    def set_to_frightened_2(self):
        """
        Different variation of frightened pose. Use to put robot to a different pose while frightened
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 23.43, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 1.54, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 15.78, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 49.98, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -22.99, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 89.27, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 28.0, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -125.76, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 31.34, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -107.03, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -66.42, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 116.62, servo_speed)

    def set_to_confused_2(self):
        """
        Different variation of confused pose. Use to put robot to a different pose while confused
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.75, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 3.82, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 10.77, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 7.34, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 68.62, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -8.66, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 72.92, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], -27.82, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -17.27, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.34, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.29, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], 40.31, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 122.68, servo_speed)

    def set_to_happy_no_neck(self):
        """
        Set robots body pose to happy
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['left_inner_shoulder'], -93.58, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 33.54, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.89, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 89.36, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -23.87, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -2.15, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
        time.sleep(1)

        for _ in range(3):
            self.move_servo(self.servo_ids['left_elbow'], -110.02, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 114.86, servo_speed)
            time.sleep(.25)
            self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
            time.sleep(.25)
        self.set_to_neutral()

    def set_to_confused_no_neck(self):
        """
        Set robots pose to confused
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 3.21, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 9.89, servo_speed)

        self.move_servo(self.servo_ids['left_inner_shoulder'], -30.64, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], -19.3, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -137.63, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.96, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.2, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], 40.57, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 139.82, servo_speed)
        servo_speed = 25
        self.move_servo(self.servo_ids['left_outer_shoulder'], 93.05, servo_speed)

        time.sleep(2)
        # shrug shoulders
        servo_speed = 50
        self.move_servo(self.servo_ids['right_inner_shoulder'], 27.21, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -92.7, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -41.01, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 76.0, servo_speed)
        time.sleep(0.25)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.96, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.2, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -30.64, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 93.05, servo_speed)
        time.sleep(0.5)

        self.set_to_neutral()




    '''
    New code beyond this point
    '''

    def set_right_leg_to_neutral(self):
        '''
        By: Nathan Borrego
        Set right leg to neutral position
        :param self:
        :return:
        '''
        servo_speed = 100
        self.move_servo(self.servo_ids['right_ankle'], -58.7, servo_speed)
        self.move_servo(self.servo_ids['right_knee'], -34.5, servo_speed)
        self.move_servo(self.servo_ids['right_bottom_hip'], -26.98, servo_speed)
        self.move_servo(self.servo_ids['right_top_hip'], -123.49, servo_speed) # This one is weird, if it is too far off, default angle does not work

    def set_left_leg_to_neutral(self):
        '''
        By: Nathan Borrego
        Set left leg to neutral position
        :param self:
        :return:
        '''
        servo_speed = 100
        self.move_servo(self.servo_ids['left_ankle'], -127.44, servo_speed)
        self.move_servo(self.servo_ids['left_knee'], -178.42, servo_speed)
        self.move_servo(self.servo_ids['left_bottom_hip'], -74.79, servo_speed)
        self.move_servo(self.servo_ids['left_top_hip'], -56.34, servo_speed)

    def set_legs_to_neutral(self):
        '''
        By: Nathan Borrego
        :return:
        '''
        servo_speed = 100
        self.move_servo(self.servo_ids['left_ankle'], -127.44, servo_speed)
        self.move_servo(self.servo_ids['right_ankle'], -58.7, servo_speed)
        self.move_servo(self.servo_ids['left_knee'], -178.42, servo_speed)
        self.move_servo(self.servo_ids['right_knee'], -34.5, servo_speed)
        self.move_servo(self.servo_ids['right_bottom_hip'], -26.98, servo_speed)
        self.move_servo(self.servo_ids['left_bottom_hip'], -74.79, servo_speed)
        self.move_servo(self.servo_ids['right_top_hip'], -123.49, servo_speed)  # This one is weird, if it is too far off, default angle does not work
        self.move_servo(self.servo_ids['left_top_hip'], -56.34, servo_speed)
        self.move_servo(self.servo_ids['right_bottom_pelvis'], -117.95, servo_speed)
        self.move_servo(self.servo_ids['left_bottom_pelvis'], -55.99, servo_speed)
        self.move_servo(self.servo_ids['forward_top_pelvis'], -34.01, servo_speed)
        self.move_servo(self.servo_ids['back_top_pelvis'], -77.43, servo_speed)

        #time.sleep(1)

    def set_right_leg_step(self):
        '''
        By: Nathan Borrego
        Start a step with the right leg
        :return:
        '''
        servo_speed = 50
        self.move_servo(self.servo_ids['right_bottom_hip'], 6.98, servo_speed)
        self.move_servo(self.servo_ids['left_knee'], -110, servo_speed)
        self.move_servo(self.servo_ids['left_ankle'], -100, servo_speed)
        time.sleep(2)
        self.move_servo(self.servo_ids['left_knee'], -178.43, servo_speed)
        time.sleep(2)
        self.move_servo(self.servo_ids['right_bottom_hip'], -26.8, servo_speed)
        time.sleep(3/4)
        self.move_servo(self.servo_ids['left_ankle'], -127.44, servo_speed)
        time.sleep(1)

    def set_left_leg_step(self):
        '''
        By: Nathan Borrego
        :return:
        '''
        servo_speed = 50
        self.move_servo(self.servo_ids['left_bottom_hip'], -108.75, servo_speed)
        self.move_servo(self.servo_ids['right_knee'], 28, servo_speed)
        self.move_servo(self.servo_ids['right_ankle'], 20, servo_speed)
        time.sleep(2)
        self.move_servo(self.servo_ids['right_knee'], -34.5, servo_speed)
        time.sleep(2)
        self.move_servo(self.servo_ids['left_bottom_hip'], -78.75, servo_speed)
        time.sleep(3/4)
        self.move_servo(self.servo_ids['right_ankle'], -58.7, servo_speed)
        time.sleep(1)

    def set_walk_cycle(self):
        '''
        By: Nathan Borrego
        :return:
        '''
        servo_speed = 150
        self.move_servo(self.servo_ids['right_ankle'], -65, servo_speed)
        self.move_servo(self.servo_ids['right_knee'], -10, servo_speed)
        self.move_servo(self.servo_ids['right_bottom_hip'], -10, servo_speed)
        self.move_servo(self.servo_ids['back_top_pelvis'], -70, servo_speed)
        self.move_servo(self.servo_ids['right_bottom_pelvis'], -120, servo_speed)
        self.move_servo(self.servo_ids['left_bottom_pelvis'], -65, servo_speed)
        #self.move_servo(self.servo_ids['chest_tilt_forward_backward'], -22, servo_speed)
        #print()
        #self.move_servo(self.servo_ids['left_outer_shoulder'], )
        #self.move_servo(self.servo_ids['right_outer_shoulder'], )
        time.sleep(1)

    def set_to_squat(self):
        '''
        By: Nathan Borrego
        :return:
        '''
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], goalPos(42.80), servo_speed)
        #self.move_servo(self.servo_ids['left_inner_shoulder'], goalPos(139.31), servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], goalPos(181.58), servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], goalPos(180.18), servo_speed)
        #self.move_servo(self.servo_ids['right_inner_shoulder'], goalPos(218.14), servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], goalPos(178.07), servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], goalPos(179.91), servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], goalPos(187.03), servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], goalPos(179.91), servo_speed)
        self.move_servo(self.servo_ids['right_ankle'], goalPos(102.74), servo_speed)
        self.move_servo(self.servo_ids['right_knee'], goalPos(198.54), servo_speed)
        self.move_servo(self.servo_ids['left_bottom_hip'], goalPos(75.23), servo_speed)
        self.move_servo(self.servo_ids['left_top_hip'], goalPos(131.04), servo_speed)
        self.move_servo(self.servo_ids['left_ankle'], goalPos(37.53), servo_speed)
        self.move_servo(self.servo_ids['left_knee'], goalPos(47.37), servo_speed)
        self.move_servo(self.servo_ids['right_bottom_hip'], goalPos(185.63), servo_speed)
        self.move_servo(self.servo_ids['right_top_hip'], goalPos(56.25), servo_speed)
        self.move_servo(self.servo_ids['right_bottom_pelvis'], goalPos(63.02), servo_speed)
        self.move_servo(self.servo_ids['left_bottom_pelvis'], goalPos(124.31), servo_speed)  # goalPos(123.31)
        self.move_servo(self.servo_ids['back_top_pelvis'], goalPos(102.57), servo_speed)

        self.move_servo(self.servo_ids['left_inner_shoulder'], goalPos(201), servo_speed) # goalPos(197.14)
        self.move_servo(self.servo_ids['right_inner_shoulder'], goalPos(158.5), servo_speed) # goalPos(162.51)

        servo_speed = 80
        time.sleep(.5)
        self.move_servo(self.servo_ids['left_inner_shoulder'], goalPos(139.31), servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], goalPos(218.14), servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], goalPos(178.33), servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], goalPos(180.79), servo_speed)
        self.move_servo(self.servo_ids['forward_top_pelvis'], goalPos(129.08), servo_speed)

        time.sleep(1)
        #self.set_body_to_neutral()

    def set_body_to_neutral(self):
        '''
        By: Nathan Borrego
        :return:
        '''
        servo_speed = 100
        self.move_servo(self.servo_ids['left_ankle'], -125.8, servo_speed)  # -127.44
        self.move_servo(self.servo_ids['right_ankle'], -54.8, servo_speed)  # -58.7
        self.move_servo(self.servo_ids['left_knee'], -178.42, servo_speed)
        self.move_servo(self.servo_ids['right_knee'], -34.5, servo_speed)
        self.move_servo(self.servo_ids['right_bottom_hip'], -26.98, servo_speed)
        self.move_servo(self.servo_ids['left_bottom_hip'], -74.79, servo_speed)
        self.move_servo(self.servo_ids['right_top_hip'], -123.49, servo_speed)  # This one is weird, if it is too far off, default angle does not work
        self.move_servo(self.servo_ids['left_top_hip'], -49.34, servo_speed)
        self.move_servo(self.servo_ids['right_bottom_pelvis'], -117.95, servo_speed)
        self.move_servo(self.servo_ids['left_bottom_pelvis'], -55.99, servo_speed)
        self.move_servo(self.servo_ids['forward_top_pelvis'], -34.01, servo_speed)
        self.move_servo(self.servo_ids['back_top_pelvis'], -77.43, servo_speed)

        self.move_servo(self.servo_ids['torso_base'], -137.02, servo_speed)  # Changed neutral from prior base value
        self.move_servo(self.servo_ids['chest_tilt_left_right'], .97, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], -.79, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 7.56, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], .35, servo_speed)  # 60.25
        self.move_servo(self.servo_ids['left_inner_shoulder'], -3.03, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.16, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.45, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], .44, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 2.59, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -82.77, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -1.63, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], .26, servo_speed)

    def set_to_smooth_walk(self):
        '''
        By: Nathan Borrego
        :return:
        '''
        AMP = 30
        FREQ = 0.5
        t0 = time.time()
        servo_speed = 100

        while True:
            t = time.time()
            if (t - t0) > 20:  # how many seconds
                break

            pos = AMP * numpy.sin(2 * numpy.pi * FREQ * t)
            pos2 = 0 #AMP * numpy.sin(2 * numpy.pi * FREQ * t + numpy.pi/2)

            print("pos: " + str(pos) + " pos2: " + str(pos2) + " t = " + str(t) + " t0 = " + str(t0))

            if 29.99 < pos < 30:
                #self.move_servo(self.servo_ids['right_ankle'], -58.7, servo_speed)
                self.move_servo(self.servo_ids['right_knee'], -34.5, servo_speed)
                self.move_servo(self.servo_ids['right_bottom_hip'], -26.98, servo_speed)
                self.move_servo(self.servo_ids['right_top_hip'], -123.49, servo_speed)  # This one is weird, if it is too far off, default angle does not work
                time.sleep(1)
            elif -0.3 < pos < 0.3:
                '''
                t2 = time.time()
                while True:
                    t = time.time()
                    if (t - t2) > 1:
                        break
                '''
            else:
                self.move_servo(self.servo_ids['right_top_hip'], 1/4 * pos + -123.49, servo_speed)  # -123.49
                self.move_servo(self.servo_ids['right_bottom_hip'], .90 * pos + -26.98 + 1, servo_speed)  # -26.98
                self.move_servo(self.servo_ids['right_knee'], .70 * pos + -14.5, servo_speed)  # -34.5
                self.move_servo(self.servo_ids['right_ankle'], 1/2 * pos + -58.7, servo_speed)  # -58.7

                self.move_servo(self.servo_ids['left_top_hip'], 1/4 * pos2 + -56.34, servo_speed)  # -56.34
                self.move_servo(self.servo_ids['left_bottom_hip'], .90 * pos2 + -74.79 + 1, servo_speed)  # -74.79
                self.move_servo(self.servo_ids['left_knee'], .70 * -1 * pos2 + -178.42, servo_speed)  # -178.42 these must be negative due to servo rotation
                self.move_servo(self.servo_ids['left_ankle'], -1/2 * pos2 + -127.44, servo_speed)  # -127.44, these must be negative due to servo rotation

            '''
            elif pos > 0.5:
                self.move_servo(self.servo_ids['right_top_hip'], 1/4 * pos + -123.49, 100)  # -123.49
                self.move_servo(self.servo_ids['right_bottom_hip'], .70 * pos + -26.98, 100)  # -26.98
                self.move_servo(self.servo_ids['left_knee'], -1 * pos + -158.42, 100)  # -178.42
                self.move_servo(self.servo_ids['left_ankle'], -1/2 * pos + -127.44, 100)  # -127.44
                pos2 = pos2 * .20
                self.move_servo(self.servo_ids['left_top_hip'], -1/4 * pos2 + -56.34, 100)  # -56.34
                self.move_servo(self.servo_ids['left_bottom_hip'], -.70 * pos2 + -74.79, 100)  # -74.79
                self.move_servo(self.servo_ids['right_knee'], -1 * pos2 + -14.5, 100)  # -34.5
                self.move_servo(self.servo_ids['right_ankle'], -1/2 * pos2 + -58.7, 100)  # -58.7
            elif pos2 > 0.5:
                self.move_servo(self.servo_ids['left_top_hip'], -1/4 * pos2 + -56.34, 100)  # -56.34
                self.move_servo(self.servo_ids['left_bottom_hip'], -.70 * pos2 + -74.79, 100)  # -74.79
                self.move_servo(self.servo_ids['right_knee'], -1 * pos2 + -14.5, 100)  # -34.5
                self.move_servo(self.servo_ids['right_ankle'], -1/2 * pos2 + -58.7, 100)  # -58.7
                pos = pos * .20
                self.move_servo(self.servo_ids['right_top_hip'], 1/4 * pos + -123.49, 100)  # -123.49
                self.move_servo(self.servo_ids['right_bottom_hip'], .70 * pos + -26.98, 100)  # -26.98
                self.move_servo(self.servo_ids['left_knee'], -1 * pos + -158.42, 100)  # -178.42
                self.move_servo(self.servo_ids['left_ankle'], -1/2 * pos + -127.44, 100)  # -127.44
            '''

            '''
            elif pos > 0:
                pos = AMP * numpy.sin(2 * numpy.pi * FREQ * t)
                poppyMove.move_servo(self.servo_ids['right_top_hip'], 1/4 * pos + -123.49, 100)  # -123.49
                poppyMove.move_servo(self.servo_ids['right_bottom_hip'], .70 * pos + -26.98, 100)  # -26.98
                poppyMove.move_servo(self.servo_ids['left_knee'], -1 * pos + -158.42, 100)  # -178.42
                poppyMove.move_servo(self.servo_ids['left_ankle'], -1/2 * pos + -127.44, 100)  # -127.44
            elif pos < 0:
                pos = AMP * numpy.sin(2 * numpy.pi * FREQ * t - numpy.pi)
                poppyMove.move_servo(self.servo_ids['left_top_hip'], 1/4 * pos + -56.34, 100)  # -56.34
                poppyMove.move_servo(self.servo_ids['left_bottom_hip'], .70 * pos + -74.79, 100)  # -74.79
                poppyMove.move_servo(self.servo_ids['right_knee'], 1 * pos + -14.5, 100)  # -34.5
                poppyMove.move_servo(self.servo_ids['right_ankle'], 1/2 * pos + -58.7, 100)  # -58.7
            '''
            '''
            else:
                poppyMove.move_servo(self.servo_ids['left_top_hip'], 1/4 * pos + -56.34, 100)  # -56.34
                poppyMove.move_servo(self.servo_ids['left_bottom_hip'], 1/2 * pos + -78.75, 100)  # -74.79
                poppyMove.move_servo(self.servo_ids['right_knee'], 1/3 * pos + -34.5, 100)  # -34.5
                poppyMove.move_servo(self.servo_ids['right_ankle'], 1/2 * pos + -58.7, 100)  # -58.7

                poppyMove.move_servo(self.servo_ids['right_top_hip'], 1/4 * pos + -123.49, 100)  # -123.49
                poppyMove.move_servo(self.servo_ids['right_bottom_hip'], 1/2 * pos + -26.98, 100)  # -26.98
                poppyMove.move_servo(self.servo_ids['left_knee'], -1/3 * pos + -178.42, 100)  # -178.42
                poppyMove.move_servo(self.servo_ids['left_ankle'], -1/2 * pos + -127.44, 100)  # -127.44
            '''


if __name__ == '__main__':
    poppyMove = poppy_body_gesture()

    time.sleep(2)
    poppyMove.set_body_to_neutral()
    time.sleep(5)
    poppyMove.set_to_squat()
    time.sleep(1)
    #poppyMove.set_body_to_neutral()

    #poppyMove.set_left_leg_step()
    #poppyMove.set_to_T_position()
    #poppyMove.set_to_wave_one_hand(True, False)

    '''
    t1 = threading.Thread(target=poppyMove.set_to_wave_one_hand, args=(1, 0,))
    t2 = threading.Thread(target=poppyMove.set_to_squat, args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    '''

# To set values in python based on wizard
# Goal in wizard - 180 = Python value
# Exception is knee 181, because going to 356 in python rotates the wrong way, the servos rotate based on direction
# through all values until goal is met
