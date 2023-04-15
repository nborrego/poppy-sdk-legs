# Poppy Social Robotics SDK Legs
___
#### Team Members: Nathan Borrego, Miranda Goelz, Aleksander Thompson, James Gray, Helen Guerrero 
This is a continuation of the Poppy Social Robotics SDK by Colin Henson, Sydney Awid and Hannah Stent. This version contains functionality for legs. To see documentation concerning the head and face tracking please visit this [link](https://github.com/chenson399/poppy-sdk).
<br/>

While this project used the Poppy Social Robotics SDK code, this documentation will focus on the changes and updates made for the legs portion of the SDK.

## Project Overview
The purpose of this project was to modify the Poppy Social Robotics SDK to include functionality for a set of legs to work alongside the face tracking and gesturing of the upper torso completed by the Poppy Social Robotics SDK. Like the project before it, this project is based on the Poppy Project's Poppy robot. This project has made substitutions and changes to the materials and designs used in the original Poppy project. This project has been made for the University of Colorado at Colorado Springs.

## User Guide
This section will outline what tools were used and how they were used to work on this project. This is intended to help anyone who intends to use this code or will be working on Poppy in the future. 
### 0. Getting Started
To start, you will need the following software:<br/>

+ [Dynamixel Wizard 2.0](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/)

+ A Python 3 capable IDE 
  + PyCharm was used for this project.

This software allows the user to scan and configure Dynamixel Motors from Robotis.

You will also need the following hardware (which should still be with Poppy...).

+ [Dynamixel MX28T](https://www.robotis.us/dynamixel-mx-28t/) ([MX28 Series Manual](https://emanual.robotis.com/docs/en/dxl/mx/mx-28/))

+ [Dynamixel MX28AT](https://www.robotis.us/dynamixel-mx-28at/)

+ [Dynamixel MX64T](https://www.robotis.us/dynamixel-mx-64t/) ([MX64 Series Manual](https://emanual.robotis.com/docs/en/dxl/mx/mx-64/))

+ [Dynamixel MX64AT](https://www.robotis.us/dynamixel-mx-64at/)

+ [Robotis U2D2](https://www.robotis.us/u2d2/)

+ [12V 5A 60W Power Supply](https://www.robotis.us/smps-12v-5a-ps-10-us-110v/)

+ [U2D2 Power Hub Board Set](https://www.robotis.us/u2d2-power-hub-board-set/) or [SMPS2Dynamixel](https://www.robotis.us/smps2dynamixel/)

+ [TTL Cables](https://www.robotis.us/robot-cable-xl320-convertible-130mm-10pcs/) 

+ [TTL Cables Convertible](https://www.robotis.us/robot-cable-x3p-180mm-convertible-10pcs/) 
  + Please note that the U2D2 and Power Hub have white connectors while the servos have beige connectors. Beige TTL connectors ***will not*** fit white TTL connectors. You will need beige TTL to white TTL cables for these instances.

+ [TTL Hubs](https://www.robotis.us/3p-extension-pcb/)

+ And of course, you should have Poppy itself.

All this hardware is what was used during this project.

### 1. Using Dynamixel Wizard
The Dynamixel Wizard allows you to scan for servos on a USB COM port. To start, make sure you have the [Robotis U2D2](https://www.robotis.us/u2d2/) connected to your computer via USB. From here, connect a TTL cable from the U2D2 to a servo. Also, connect the power brick to the [U2D2 Power Hub Board Set](https://www.robotis.us/u2d2-power-hub-board-set/) and connect the U2D2 Power Hub Board Set TTL to the servo as well. With the U2D2 and the Power Hub both connected by TTL to the servo, you will be able to scan the servo on the Wizard.

First, click scan on the Wizard. The Wizard will scan all servo IDs and all baud rates to start with. You can change what IDs and baud rates to scan under Options > Scan. If you have a servo connected, once the scan is complete, you will see the servo and its ID show up on the left on the Wizard. You can click on the servo to see all the information and options for that servo. It is important to remember that each servo has a unique ID and a set baud rate.

It is important to note that servos with the *same* ID **cannot** be displayed in the Wizard at the same time. All servo IDs **must** be unique to be scan-able and usable. **If you are integrating new servos into the system, you *MUST* scan in each new servo individually into the Wizard and change its ID to a new and unique ID before trying to use these servos together with existing or other new servos. All servos start with an ID of 1, so set it to something else and do not set it to an existing ID. A list of all used IDs for this project can be found below. Note that this can be tedious to do, and you may have to set temporary IDs on a servo in order to get it to what you want especially when swapping the IDs of servos.**
<br/><br/>
#### 1.1 Important Notes about Dynamixel Wizard and Servos
It is important to understand how the Dynamixel Wizard controls the servos so here are a few notes to be aware of. 

+ The servos in the Wizard operate on a 0&deg; to 360&deg; system. 

+ The middle and right pane of Dynamixel Wizard are interactable and allow you to change some values if you so desire. We found this to be unclear when first starting to use the Wizard. When interacting with a servo in joint mode, the red line is the goal position of the servo, while the green line is the actual position of the servo. The backing grey "circle" is the allowed limits on the angles of the servo. These angle limits can be changed, you will see them listed in the middle pane of the Wizard. It may prove useful to set angle limits so that you can more readily see where the servo can be, but be warned that they can also be misleading based to how the actual physical system works.

+ The servos ***will not*** cross the 360&deg; -> 0&deg; boundary and vice versus. This means that a servo trying to go from a postion of 26&deg; to 354&deg; ***will not*** take the short path by crossing 0&deg;. This can cause erratic behavior in the physical system if you are not careful with the initial positioning of servos when the system is built. It is important to make sure that the servos will never cross this boundary on their desired swinging path.

+ When the torque on a joint servo is **on**, the servo is locked and cannot freely swing. Click the torque **off** will alow the servo to freely swing. This can be controlled by code which will be covered.

+ There are alarms at the bottom of the Wizard which can alert you to issues that the motors may be having. The most important one is the "overload" alarm. If this is red and counting up then the servo will no longer respond to commands and power **must** be disconnected and reconnected to reset the motor.

### 2. Controlling Servos with Python
This project uses the [pypot.dynamixel library](https://github.com/poppy-project/pypot) to control the Dynamixel servos. 

To get started, you will want to import the library with:

```python
import pypot.dynamixel
```

Then, you will need to create a dxl.io object using:

```python
dxl_io = pypot.dynamixel.DxlIO('COM7')
```

The name "dxl_io" can be anything you want. COM7 referes to the USB communication port, be aware that COM7 is what was used during this project and may be different in the future as COM7 was not used by the previous team and had to be changed.

This "dxl_io" object allows you to access any of the functions that these servos have that can be controlled through the Dynamixel Wizard. This section will cover the ones that were used during the project, but there are more than that.

To set the speed of the servo use this method where servo_id is the ID of the servo as it corresponds to the Wizard, and servo_speed is from 0-250.
```python
dxl_io.set_moving_speed({servo_id: servo_speed})
```

To set the position of the servo, use this method where servo_id is the ID of the servo as it corresponds to the Wizard.

Servo positioning in python code requires a bit more explanation.
```python
dxl_io.set_goal_position({servo_id: servo_position})
```

In the Dynamixel Wizard, the servos operate on 0&deg; to 360&deg;, with 0&deg; starting at the bottom of the presented circle in the Wizard and going counter clock-wise until 360&deg; is reach on the opposite side of the bottom of the circle. The boundary that the servos cannot cross is at the bottom of this circle. When controlling the servos with pypot, you will not be using 0&deg; to 360&deg;, instead the pypot library uses +180&deg; to -180&deg; with 0&deg; being the top of the circle in the Wizard. The left hemisphere of the circle is 0&deg; to +180&deg; and the right hemisphere is 0&deg; to -180&deg;. This means that if you want to take an angle position value from the Wizard and use it to set the position using pypot, you must subtract the Wizard angle value by 180&deg;.

For example, if we want to set a servo to position 137.65&deg; in the Wizard, and move it, there we would do the following in the code:

```python
servo_position = 137.72-180  # 137.72-180 = -42.28
servo_speed = 50  # Example speed
dxl_io.set_moving_speed({servo_id: servo_speed})
dxl_io.set_goal_position({servo_id: servo_position})
```

Another command that was used was the ability to disable the torque and allow the motor to freely swing from the Python code.

```python
dxl_io.disable_torque([servo_id1, servo_id2, ...])
```

The preceding example demonstrates that the functions you can do with the Wizard can be done in Python as well. It is worth your time to go through [pypot.dynamxiel.io.io.py](https://github.com/poppy-project/pypot/blob/master/pypot/dynamixel/io/io.py) and [pypot.dynamixel.io.abstract_io.py](https://github.com/poppy-project/pypot/blob/master/pypot/dynamixel/io/abstract_io.py) to learn what functions are available to use and how to use them. The ```dxl_io``` object is created using the ```DxlIO``` class from io.py which inherits from the ```AbstractDxlIO``` class in abstract_io.py.

## Documentation
### 0. Setup
Though it is useful to understand the underlying structure behind this code, the team before us has written code to streamline the programming of the servos. This section will cover how we controlled the servos using the previous teams code. We will start with a brief overview of the previous team's functions and how we used them. For documentation of the previous team's code, please visit this [link](https://github.com/chenson399/poppy-sdk).

We made full use of the suite of functions written by the previous team in [poppy_servo_control.py](https://github.com/nborrego/poppy-sdk-legs/blob/master/src/poppy_servo_control.py) during development. To start, we created a Poppy object with following code:

```python
import pypot.dynamixel
poppyMove.poppy_body_gesture()
```

This ```poppyMove``` object is used to be able to run functions in main.

The poppy_body_gesture class is the class written by the Poppy Social Robotics SDK team. This class initializes the USB COM port as well as a dictionary of servo IDs corresponding to a descriptive name of its physical position on Poppy for easier calling in functions. It is recommended that any new servos are added to this dictionary as they are integrated One of the most used functions within this class is the ```move_servo``` function. This streamlines the process of moving a servo at a certain speed to a certain position. Here is an example of usage within the class as well as using the dictionary for servo IDs:

```python
servo_speed = 50
self.move_servo(self.servo_ids['left_shoulder'], -45, servo_speed)
```

This is how all the movement of the servos is done. Writing these line by line can take a lot of time and can be tedious. Thanks to the last team, however, there is a function to streamline this process. We made use of the ```pose_generator()``` function they made which will print to console these ```self.move_servo()``` lines with the servo IDs and current position of the servo filled in, as well as a servo_speed placeholder. Using this function, all we needed to do was to set Poppy to the desired position with physical or Wizard manipulation of the servos, and then while holding Poppy in that postion, call ```poppyMove.pose_generator()``` to get a print out of the required code to reach the desired position. This allowed us to rapidly try out different positions of Poppy.

### 1. New Functions in Poppy SDK Legs
This SDK contains many new functions focused on legs functionality for Poppy. The new functions are found in **poppy_sero_control.py**.

#### ```goalPos(n)```

This is a simple function to quickly convert angles between the Wizard and Python without having to do the math yourself. ```n``` is the goal position in the Wizard, and the function will return the converted angle that will work in Python.

#### ```set_right_leg_to_neutral(self)```

This function sets the right leg of Poppy to a neutral, standing straight up position.

#### ```set_left_leg_to_neutral(self)```

This function sets the left leg of Poppy to a neutral, standing straight up position.

#### ```set_legs_to_neutral(self)```

This function sets both of Poppy's legs to neutral at the same time.

#### ```set_to_squat(self)```

This function runs a squat routine for Poppy.

#### ```set_body_neutral(self)```

This function sets the entirety of Poppy to a neutral, standing straight up position with arms at its sides. This is the default position for Poppy, all movements begin from this position.

#### ```main```

The main in poppy_servo_control.py **is not** the true main for the overall SDK. This main should only be used to test and develop movement of the servos.

### 2. Common Issues Troubleshooting and Tips
This section will cover some common issues we ran into and their solution.

+ Sometimes, you may find that a servo no longer responds. This _usually_ happens when a motor is trying to move to a position and gets blocked, usually by a cord or a piece of Poppy. Generally a motor will screech to tip you off when this is happening but not always. If a motor gives out and no longer responds (the motor is swinging freely), then the motor is more than likely overloaded. You can confirm this by connecting to the motor in the Dynamixel Wizard, clicking on the offending motor, and checking the alarms at the bottom of the Wizard. If you see the "Overload" alarm lit up red and counting up then this is your issue. To solve this issue, you need to disconnect and reconnect the power to the servo. We did this by just unplugging the power brick from the [SMPS2Dynamixel](https://www.robotis.us/smps2dynamixel/) and replugging it. Of course this kills power to all the servos causing them to go free, so be ready to catch Poppy!
  + We commonly had this issue with the old knees due to the weight of the upper body bearing down on the knee MX28 servos causing them to buckle and stop responding. This issue also appeared when incorrectly inputting angles to set servos to, causing them to go just slightly too far which caused resistance. The servos are not very good when met with resistance and like to get overloaded and go free.
  + This is the most common issue we had during the project.
+ When you input an angle and go to test the servo, you may observe that the servo begins moving in the expected direction, but suddenly switches direction and goes the other way. This is likely due to the servos inability to cross between 0&deg; and 360&deg; (based on the Wizard). When adding new servos to Poppy, you should try to pay attention to how much room you need the servo to swing, and within the swing path, make sure that the boundary will not be in that path. Unfortunately, we did not realize this initially so a few existing servos may run into this issue, sorry!
+ If you are trying to upload code to the servos but are getting permission errors, you probably did not click the disconnect button in the Wizard. You cannot have the Wizard connected to the motors at the same time you try to upload code from a Python IDE. You will likely forget about this when going back and forth between the two, and it will annoy you.


